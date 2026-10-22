"""Integroitu pelitila — yhdistää RPG-, sosiaalisen verkon ja psykotroniikan.

GameState on jaettu selkäranka. RPG-skeenet emittoivat tapahtumia
(suhdemuutokset, tiedonsaannit, liput), jotka virtaavat sosiaaliseen
verkkoon ja psykotroniseen tilaan. Hacking-tulokset virtaavat takaisin
RPG:hen tietona, mielentiloina ja lippuina.

Tämä moduuli EI korvaa RPG-moottoria — se käärii sen ja tarjoaa
moduulien välisen sillan, jonka integraatiovaatimus edellyttää.

Kolmen moduulin integraatio:
  RPG → sosiaalinen:   dialogin valinnat muuttavat suhdeverkkoa
  Sosiaalinen → RPG:   luottamus avaa uusia dialogivaihtoehtoja
  RPG → psykotroniikka: löydetyt todisteet avaavat hacking-moduulin
  Psykotroniikka → RPG: hacking paljastaa piilosuhteita ja tietoa
  Stressi → psykotroniikka: mietentilat heikentävät hacking-suoritusta
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..rpg import (
    RPGSession,
    RPGEvent,
    GraphEffect,
    load_character,
    load_scenario,
    session_from_dict,
    session_to_dict,
)
from .social_graph import MultiDimensionalSocialGraph, NPCMemory, RELATIONSHIP_DIMENSIONS
from .npc_autonomy import NPCAutonomyAction, run_npc_turn


GAME_SAVE_VERSION = 1


@dataclass
class HackingState:
    """Psykotronisen session tila integroidussa pelissä.

    Noöpunkin hacking ei ole pelkkää kyberpunk-cyberspacea. Se on
    nelikerroksinen ja kerrokset läpitunkeutuvat toisiinsa:

      kyberneettinen  — tietokoneet, päätteet, implantit, sensorit
      sosiaalinen     — identiteetit, valtasuhteet, luvat, suostumukset
      biologinen      — hermosto, aineenvaihdunta, UFAB 80MG, unisyklit
      psyykkinen      — CAN-solmut, noetoottiset signaalit, arkkityypit,
                        muistot, unet, astraalitila

    Psykotroniikka on näiden kerrosten risteyskohta: kvanttipanpsykismiin
    perustuva (fiktiivinen) teknologia, joka toistaa, fokusoi tai
    vahvistaa ihmisten luonnollisia PSI-kykyjä ja rajapintaa Conscious
    Agent Networkiin. Kerrokset eivät ole erillisiä tasoja — ne ovat
    ontologisesti epämääräinen tila, jossa on mahdotonta sanoa
    varmasti millä tasolla tapahtuu.

    Hälytys kasvaa epäonnistumisista ja voi johtaa Ragnarökin huomioon.
    """

    available: bool = False
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    alert_level: int = 0
    discovered_nodes: set[str] = field(default_factory=set)
    discovered_edges: set[tuple[str, str]] = field(default_factory=set)
    hacked_nodes: set[str] = field(default_factory=set)

    def to_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "attempts": self.attempts,
            "successes": self.successes,
            "failures": self.failures,
            "alert_level": self.alert_level,
            "discovered_nodes": sorted(self.discovered_nodes),
            "discovered_edges": [list(e) for e in sorted(self.discovered_edges)],
            "hacked_nodes": sorted(self.hacked_nodes),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> HackingState:
        return cls(
            available=data.get("available", False),
            attempts=data.get("attempts", 0),
            successes=data.get("successes", 0),
            failures=data.get("failures", 0),
            alert_level=data.get("alert_level", 0),
            discovered_nodes=set(data.get("discovered_nodes", [])),
            discovered_edges={tuple(e) for e in data.get("discovered_edges", [])},
            hacked_nodes=set(data.get("hacked_nodes", [])),
        )


@dataclass
class GameSave:
    """Koko pelitilan tallennusdokumentti."""

    rpg: dict[str, Any]
    social: dict[str, Any]
    hacking: dict[str, Any]
    version: int = GAME_SAVE_VERSION


class GameState:
    """Integroitu pelitila — RPG, sosiaalinen verkko ja psykotroniikka.

    Käyttö:
        state = GameState.from_files(character_path, scenario_path)
        state.start()
        # Pelaa RPG-interaktioita:
        state.perform_rpg_interaction("check_forms")
        # Tarkista sosiaalinen verkko (ID:t mapped via _id_map):
        state.social.get_relationship("romppainen", "ingrid_falk")
        # Onko psykotroniikka saatavilla:
        state.hacking.available
    """

    def __init__(
        self,
        rpg_session: RPGSession,
        social: MultiDimensionalSocialGraph,
        hacking: HackingState | None = None,
    ) -> None:
        self.rpg = rpg_session
        self.social = social
        self.hacking = hacking or HackingState()
        # Map RPG character IDs to social graph IDs
        self._id_map: dict[str, str] = {
            "romppainen_narkkari": "romppainen",
            "romppainen_day_1": "romppainen",
        }
        self._sync_social_from_rpg()

    @classmethod
    def from_files(
        cls,
        character_path: str | Path,
        scenario_path: str | Path,
        social_data: dict[str, Any] | None = None,
        seed: int | None = None,
    ) -> GameState:
        character = load_character(character_path)
        scenario = load_scenario(scenario_path)
        rpg_session = RPGSession(character, scenario, seed=seed)

        social = MultiDimensionalSocialGraph(seed=seed)
        if social_data:
            social = MultiDimensionalSocialGraph.from_dict(social_data, seed=seed)

        return cls(rpg_session, social)

    def start(self) -> None:
        """Alusta sosiaalinen verkko päivän 1 hahmoilla jos tyhjä."""
        if self.social.graph.number_of_nodes() > 0:
            return
        self._populate_default_social_graph()

    def _populate_default_social_graph(self) -> None:
        """Täytä sosiaalinen verkko päivän 1 ydinnäyttelijöillä.

        C.G. Jung Cityn henkilögallereria ohjaavat Jungilaiset arkkityypit
        ja UFABin byrokraattinen hierarkia. Jokaisella hahmolla on
        tavoitteet, mieliala ja implisiittinen asema voimasuhteissa.
        """
        cast = [
            ("romppainen", "Emil Romppainen / Sven-Olof", "patient",
             ["Selviä päivästä", "Saada UFAB 80MG", "Selvittää kuka oikeasti on"],
             "disoriented"),
            ("ingrid_falk", "Ingrid Falk", "patient",
             ["Selviytyä Elsan kuolemasta", "Ymmärtää terapiaa", "Pysyä hengissä"],
             "grieving"),
            ("elin_dahl", "Dr. Elin Dahl", "staff",
             ["Suodattaa sisääntulevat potilaat", "Noudattaa UFAB-protokollaa"],
             "professional"),
            ("yuki_tanaka", "Dr. Yuki Tanaka", "staff",
             ["Turvata potilaiden hyvinvointi", "Valvoa Pilgrimin kokeita"],
             "watchful"),
            ("soren_pilgrim", "Dr. Søren Pilgrim", "staff",
             ["Työntää koe eteenpäin", "Testata UFAB 80MG:n rajoja"],
             "intense"),
            ("ufab_ragnarok", "UFAB Ragnarök (C.G. Jung)", "ai",
             ["Facilitoida terapiaa", "Valvoa kaikkia järjestelmiä",
              "Tuntemattomat syvemmät tavoitteet"],
             "omniscient"),
            ("irungu_wakini", "Irungu Wakini", "patient",
             ["Parantua reggaen ja mystiikan kautta", "Auttaa muita"],
             "calm"),
            # Komisario Kallio tunkeutuu psykotronisesti päivän 1
            # Tukholman-simulaatioon etsiessään vuosikymmenien partneriaan.
            # Hän tunnistaa Romppaisen mutta ei tämän fyysistä sijaintia.
            ("lotta_kallio", "Komisario Lotta Kallio", "intelligence",
             ["Löytää kadonnut partnerinsa",
              "Selvittää mitä Romppaiselle on tehty",
              "Saattaa Romppainen turvaan"],
             "alarmed"),
        ]
        for char_id, name, role, goals, mood in cast:
            self.social.add_character(char_id, name, role, goals, mood)

        # Alkusuhteet (lab_relationships.csv + uudet dimensiot)
        initial_rels = [
            ("romppainen", "elin_dahl", {"trust": 0, "suspicion": 0, "authority": 1, "familiarity": 0}),
            ("elin_dahl", "romppainen", {"trust": 0, "suspicion": 0, "authority": 3, "familiarity": 0}),
            ("romppainen", "ingrid_falk", {"trust": 0, "attraction": 0, "familiarity": 0}),
            ("ingrid_falk", "romppainen", {"trust": 0, "familiarity": 0}),
            ("soren_pilgrim", "yuki_tanaka", {"trust": -1, "authority": 2, "suspicion": 1}),
            ("yuki_tanaka", "soren_pilgrim", {"trust": -1, "suspicion": 1, "fear": 1}),
            ("soren_pilgrim", "elin_dahl", {"trust": -1, "authority": 1}),
            ("elin_dahl", "soren_pilgrim", {"trust": -1, "fear": 1}),
            ("yuki_tanaka", "elin_dahl", {"trust": 2, "familiarity": 1}),
            ("elin_dahl", "yuki_tanaka", {"trust": 2, "familiarity": 1}),
            ("ufab_ragnarok", "romppainen", {"trust": 0, "suspicion": 1, "authority": 2}),
            ("romppainen", "ufab_ragnarok", {"trust": 0, "suspicion": 1}),
            ("ufab_ragnarok", "ingrid_falk", {"trust": 0, "suspicion": 0, "authority": 2}),
            ("irungu_wakini", "romppainen", {"trust": 1, "familiarity": 0}),
            # Kallio tunnistaa partnerinsa vuosikymmenten tutunmusta:
            # syvä luottamus ja tuntemus, pelko hänen puolestaan,
            # epäilys siitä mitä hänelle on tehty, viranomainen auktoriteetti.
            ("lotta_kallio", "romppainen", {"trust": 2, "familiarity": 3,
             "fear": 1, "suspicion": 1, "authority": 2}),
            # Narkkari-Sven-Olof ei tunnista Kalliota: näkee pelottavan
            # Europol-poliisin, sumea tuttuus, pelko ja epäilys pidätyksestä.
            ("romppainen", "lotta_kallio", {"trust": 0, "familiarity": 1,
             "suspicion": 1, "fear": 1}),
        ]
        for source, target, dims in initial_rels:
            self.social.set_relationship(source, target, dims)

        # Piilosuhteet (eivät näy pelaajalle alussa)
        # Ragnarök valvoo kaikkia — mutta ei anna sen näkyä
        hidden_rels = [
            ("ufab_ragnarok", "ingrid_falk", {"trust": 1, "familiarity": 1}, True),
            ("ufab_ragnarok", "romppainen", {"suspicion": 2, "authority": 3}, True),
            # Ragnarök havaitsee simulaatioon tunkeutuneen ulkopuolisen
            # tiedustelutoimijan ja pitää sen uhkana järjestelmän suvereniteetille.
            ("ufab_ragnarok", "lotta_kallio", {"suspicion": 2, "authority": 2}, True),
            # Kallio epäilee taustalla olevaa tekoälyjärjestelmää ja tuntee
            # sen otteen partnerissaan, vaikka ei vielä ymmärrä sen luonnetta.
            ("lotta_kallio", "ufab_ragnarok", {"suspicion": 1, "familiarity": 1}, True),
        ]
        for source, target, dims, hidden in hidden_rels:
            self.social.set_relationship(source, target, dims, hidden=hidden)

    def perform_rpg_interaction(self, interaction_id: str) -> Any:
        """Suorita RPG-interaktio ja synkronoi vaikutukset sosiaaliseen verkkoon."""
        scene_id = self.rpg.scene.id
        interaction = self.rpg.scene.interactions[interaction_id]
        event_start = len(self.rpg.events)
        result = self.rpg.perform_interaction(interaction_id)
        self.social.advance_turn()
        self._sync_social_from_rpg()
        self._record_npc_memories(scene_id, interaction.id, interaction.label, event_start)
        self._check_hacking_unlock()
        return result

    def _record_npc_memories(
        self,
        scene_id: str,
        interaction_id: str,
        interaction_label: str,
        event_start: int,
    ) -> None:
        """Turn relationship consequences and explicit events into NPC recollections."""
        actor = self._id_map.get(self.rpg.character.id, self.rpg.character.id)
        targets: dict[str, int] = {}
        explicit: list[dict[str, Any]] = []
        for event in self.rpg.events[event_start:]:
            if event.type == "relationship_changed":
                raw_target = str(event.payload.get("target", ""))
                target = self._id_map.get(raw_target, raw_target)
                if target in self.social.graph:
                    targets[target] = targets.get(target, 0) + int(event.payload.get("delta", 0))
            elif event.type == "npc_memory":
                explicit.append(event.payload)

        summary = " ".join(interaction_label.split())[:240]
        explicit_targets = {
            self._id_map.get(str(payload.get("target", "")), str(payload.get("target", "")))
            for payload in explicit
        }
        for target, valence in targets.items():
            if target in explicit_targets:
                continue
            tone = "positive" if valence > 0 else "negative" if valence < 0 else "ambiguous"
            self.social.remember(target, NPCMemory(
                turn=self.social.turn,
                scene=scene_id,
                interaction=interaction_id,
                actor=actor,
                summary=summary,
                valence=valence,
                tags=("player_choice", "relationship", tone),
            ))

        for payload in explicit:
            raw_target = str(payload.get("target", ""))
            target = self._id_map.get(raw_target, raw_target)
            if target not in self.social.graph:
                continue
            self.social.remember(target, NPCMemory(
                turn=self.social.turn,
                scene=scene_id,
                interaction=interaction_id,
                actor=actor,
                summary=str(payload.get("summary", interaction_label)),
                valence=int(payload.get("valence", 0)),
                tags=tuple(str(tag) for tag in payload.get("tags", ["player_choice"])),
            ))

    def _sync_social_from_rpg(self) -> None:
        """Sovella RPG:n graafitehosteja sosiaaliseen verkkoon.

        RPG-moottori emittoi GraphEffect-olioita, joiden domain="social".
        dimension on 'key'-kentässä; yksiarvoiset taaksepäin-yhteensopivat.
        """
        pending: list[GraphEffect] = []
        for effect in self.rpg.state.graph_effects:
            if effect.domain != "social":
                pending.append(effect)
                continue
            if effect.operation == "adjust_edge":
                dimension = effect.key
                if dimension not in RELATIONSHIP_DIMENSIONS:
                    dimension = "trust"  # backward compat yksiarvoiseen
                source = self._id_map.get(effect.source, effect.source)
                target = self._id_map.get(effect.target or "", effect.target or "")
                if source not in self.social.graph or target not in self.social.graph:
                    pending.append(effect)
                    continue
                self.social.change_relationship(
                    source,
                    target,
                    dimension,
                    int(effect.value or 0),
                    reason=f"RPG: {effect.source} -> {effect.target}",
                )
            else:
                pending.append(effect)
        # Säilytä vain käsittelemättömät tehosteet seuraavaa synkronointia varten
        self.rpg.state.graph_effects = pending

    def _check_hacking_unlock(self) -> None:
        """Tarkista, avautuuko psykotroniikka RPG-lippujen perusteella."""
        flags = self.rpg.state.campaign_flags
        info = self.rpg.state.known_information
        scene_id = self.rpg.scene.id

        # Psykotroniikka avautuu, kun löydät todisteita piilevistä järjestelmistä
        if any(key in info for key in ("strange_forms", "device_analysis", "device_firewall_model")):
            self.hacking.available = True
        if flags.get("found_ufab_nhi_evidence") or flags.get("suspects_ufab"):
            self.hacking.available = True
        # Uuden Day 1 -skenaarion keikka on itsessään ensimmäinen
        # psykotroniikkaa vaativa vaihe. Pidä portti samana CLI:ssä ja UI:ssa.
        if scene_id in {"d1_ufab_heist", "d1_night_signal", "d1_complete"}:
            self.hacking.available = True

    def get_npc_state(self, npc_id: str) -> dict[str, Any]:
        """Hae NPC:n mieliala ja tavoitteet."""
        if npc_id not in self.social.graph:
            return {}
        data = self.social.graph.nodes[npc_id]
        return {
            "name": data.get("name", npc_id),
            "mood": data.get("mood", "neutral"),
            "goals": data.get("goals", []),
            "memories": self.social.memories(npc_id),
        }

    def perform_npc_turn(self, max_actions: int = 2) -> list[NPCAutonomyAction]:
        """Let NPCs advance their goals through deterministic social actions."""
        player_id = self._id_map.get(self.rpg.character.id, self.rpg.character.id)
        return run_npc_turn(
            self.social,
            player_id=player_id,
            scene_id=self.rpg.scene.id,
            max_actions=max_actions,
        )

    def _match_participant(self, name: str) -> str | None:
        """Yhdistä scenen osallistujan näyttönimi sosiaaligraafin solmuun.

        Osallistujanimi ja solmun 'name' voivat erota lisäosista (esim.
        'UFAB Ragnarök' vs 'UFAB Ragnarök (C.G. Jung)') — riittää, että
        jompikumpi sisältyy toiseen. Pysytellään sosiaaligraafin domaanissa;
        RPG-moottori ei tiedä NPC-muisteista.
        """
        key = name.strip().lower()
        if not key:
            return None
        for node_id, data in self.social.graph.nodes(data=True):
            node_name = str(data.get("name", node_id)).strip().lower()
            if key == node_name or key in node_name or node_name in key:
                return node_id
        return None

    def participant_memory_lines(self) -> list[tuple[str, dict[str, Any]]]:
        """Palauta (näyttönimi, uusin muisto) -parit nykyisen scenen
        osallistujille, jotka muistavat pelaajaa.

        Tämä on "reference them in later scenes" -kohta: kun pelaaja
        saapuu kohtaukseen, NPC:n viimeisin muisti nousee esiin.
        """
        lines: list[tuple[str, dict[str, Any]]] = []
        for name in self.rpg.scene.participants:
            node_id = self._match_participant(name)
            if node_id is None:
                continue
            memories = self.social.memories(node_id, limit=1)
            if memories:
                lines.append((name, memories[0]))
        return lines

    def transition_to_scenario(self, scenario_path: str | Path) -> None:
        """Continue the campaign in another scenario without discarding play state.

        Scenario-local scene/dialogue progress is reset. Character development,
        conditions, consequences, campaign flags, discoveries, relationships,
        deterministic draw positions, event history, the social graph and the
        psychotronic status all continue across the boundary.
        """
        self._sync_social_from_rpg()
        previous = self.rpg
        scenario = load_scenario(scenario_path)
        following = RPGSession(previous.character, scenario, seed=previous.seed)
        following.state.conditions = set(previous.state.conditions)
        following.state.consequences = list(previous.state.consequences)
        following.state.campaign_flags = dict(previous.state.campaign_flags)
        following.state.known_information = set(previous.state.known_information)
        following.state.relationships = dict(previous.state.relationships)
        following.events = list(previous.events)
        following.events.append(RPGEvent("scenario_started", {"scenario_id": scenario.id}))
        following.restore_random_draws(previous.random_draws)
        following.restore_tarot_draws(previous.tarot_draws)
        self.rpg = following
        self._check_hacking_unlock()

    def to_save(self) -> GameSave:
        """Serialisoi koko integroitu tila."""
        return GameSave(
            rpg=session_to_dict(self.rpg),
            social=self.social.to_dict(),
            hacking=self.hacking.to_dict(),
        )

    @classmethod
    def from_save(
        cls,
        save: GameSave,
        character_path: str | Path,
        scenario_path: str | Path,
    ) -> GameState:
        """Palauta tallennuksesta."""
        if save.version != GAME_SAVE_VERSION:
            raise ValueError(f"Unsupported integrated save version: {save.version}")
        character = load_character(character_path)
        scenario = load_scenario(scenario_path)
        rpg_session = session_from_dict(save.rpg, character, scenario)
        social = MultiDimensionalSocialGraph.from_dict(save.social, seed=rpg_session.seed)
        hacking = HackingState.from_dict(save.hacking)
        return cls(rpg_session, social, hacking)

    def save_to_file(self, path: str | Path) -> None:
        save = self.to_save()
        Path(path).write_text(
            json.dumps({
                "rpg": save.rpg,
                "social": save.social,
                "hacking": save.hacking,
                "version": save.version,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load_from_file(
        cls,
        path: str | Path,
        character_path: str | Path,
        scenario_path: str | Path,
    ) -> GameState:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        save = GameSave(
            rpg=data["rpg"],
            social=data["social"],
            hacking=data["hacking"],
            version=data.get("version", 1),
        )
        return cls.from_save(save, character_path, scenario_path)
