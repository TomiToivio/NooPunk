"""Drones (SRD 3.8.x): every value asserted here is read from the SRD table or the rule text."""

from __future__ import annotations

import unittest

from src.rules import cwn_drones as d


class DroneCatalogTests(unittest.TestCase):
    """SRD 3.8.1 table, transcribed."""

    def test_the_catalog_has_every_srd_entry(self) -> None:
        self.assertEqual(
            set(d.DRONES),
            {"Mouse", "Roach", "Hummingbird", "Sunfish", "Pitbull",
             "Javelin", "Kerberos", "Kraken", "Shrike"},
        )

    def test_table_values(self) -> None:
        for name, cost, ac, tt, hp, fittings, move, rate, hardpoints, enc in (
            ("Mouse", 500, 13, 6, 1, 0, "ground", 5, 0, 1),
            ("Roach", 1_000, 13, 6, 8, 3, "ground", 10, 0, 3),
            ("Hummingbird", 2_000, 15, 6, 5, 2, "fly", 10, 0, 3),
            ("Sunfish", 1_000, 15, 6, 8, 3, "swim", 10, 0, 3),
            ("Pitbull", 5_000, 15, 8, 15, 5, "ground", 20, 1, 5),
            ("Javelin", 10_000, 16, 6, 12, 5, "fly", 20, 1, 6),
            ("Kerberos", 15_000, 18, 8, 25, 6, "ground", 20, 3, None),
            ("Kraken", 10_000, 16, 8, 20, 5, "swim", 15, 2, None),
            ("Shrike", 25_000, 18, 8, 20, 6, "fly", 30, 2, None),
        ):
            with self.subTest(drone=name):
                x = d.DRONES[name]
                self.assertEqual(
                    (x.cost, x.armor_class, x.trauma_target, x.hit_points,
                     x.fittings, x.mode, x.move_rate, x.hardpoints, x.encumbrance),
                    (cost, ac, tt, hp, fittings, move, rate, hardpoints, enc),
                )

    def test_non_portable_drones_are_the_encumbrance_dash_entries(self) -> None:
        self.assertEqual({n for n, x in d.DRONES.items() if not x.portable},
                         {"Kerberos", "Kraken", "Shrike"})


class MountingTests(unittest.TestCase):
    """SRD 3.8.1: encumbrance decides the largest weapon class."""

    def test_three_or_less_is_pistol_sized(self) -> None:
        for name in ("Mouse", "Roach", "Hummingbird", "Sunfish"):
            with self.subTest(drone=name):
                self.assertEqual(d.mount_class(d.DRONES[name]), "pistol")

    def test_larger_man_portable_is_rifle_sized(self) -> None:
        self.assertEqual(d.mount_class(d.DRONES["Pitbull"]), "rifle")
        self.assertEqual(d.mount_class(d.DRONES["Javelin"]), "rifle")

    def test_non_portable_can_mount_heavy(self) -> None:
        for name in ("Kerberos", "Kraken", "Shrike"):
            with self.subTest(drone=name):
                self.assertEqual(d.mount_class(d.DRONES[name]), "heavy")


class ControlTests(unittest.TestCase):
    """SRD 3.8.4."""

    def test_a_control_board_drives_exactly_one(self) -> None:
        self.assertEqual(d.command_capacity("board", drive_skill=5), 1,
                         "a control board drives one drone regardless of skill")

    def test_a_remote_control_unit_drives_one_plus_drive_skill(self) -> None:
        self.assertEqual(d.command_capacity("remote_control_unit", drive_skill=0), 1)
        self.assertEqual(d.command_capacity("remote_control_unit", drive_skill=1), 2)
        self.assertEqual(d.command_capacity("remote_control_unit", drive_skill=4), 5)

    def test_a_control_board_costs_two_unless_you_have_a_cranial_jack(self) -> None:
        self.assertEqual(d.control_penalty("board"), -2)
        self.assertEqual(d.control_penalty("board", cranial_jack=True), 0)
        self.assertEqual(d.control_penalty("remote_control_unit"), 0)

    def test_range_has_three_tiers_not_two(self) -> None:
        self.assertEqual(d.range_status(0), "safe")
        self.assertEqual(d.range_status(1_000), "safe")
        self.assertEqual(d.range_status(1_001), "hijackable")
        self.assertEqual(d.range_status(8_000), "hijackable")
        self.assertEqual(d.range_status(8_001), "out_of_range")


class OperatorTests(unittest.TestCase):
    """SRD 3.8.4.1-3.8.4.2."""

    def test_skills_are_capped_by_drive(self) -> None:
        # "a master infiltrator with Sneak-4 ... with Drive-0 they can exert only Sneak-0"
        self.assertEqual(d.skill_through_drone(4, 0), 0)
        self.assertEqual(d.skill_through_drone(4, 2), 2)
        self.assertEqual(d.skill_through_drone(1, 3), 1)

    def test_gunnery_uses_better_of_drive_or_program_and_int_or_dex(self) -> None:
        bonus = d.gunnery_bonus(base_attack_bonus=3, drive_skill=1, program_skill=2,
                                int_modifier=0, dex_modifier=1)
        self.assertEqual(bonus, 3 + 2 + 1)

    def test_autonomous_drones_use_a_flat_plus_two(self) -> None:
        self.assertEqual(
            d.gunnery_bonus(base_attack_bonus=9, drive_skill=9, program_skill=9,
                            int_modifier=2, dex_modifier=2, autonomous=True),
            2,
        )

    def test_one_attack_is_directed_and_the_rest_fire_at_plus_two(self) -> None:
        self.assertEqual(d.drone_attack_bonuses(weapons=3, directed_bonus=6), (6, 2, 2))
        self.assertEqual(d.drone_attack_bonuses(weapons=1, directed_bonus=6), (6,))
        self.assertEqual(d.drone_attack_bonuses(weapons=0, directed_bonus=6), ())
        self.assertEqual(
            d.drone_attack_bonuses(weapons=2, directed_bonus=4),
            (4, 2),
            "exactly one attack is directed",
        )


class UpkeepTests(unittest.TestCase):
    """SRD 3.8.0 and 3.8.4.3."""

    def test_charging_is_one_hour_per_encumbrance_capped_at_six(self) -> None:
        self.assertEqual(d.charge_hours(d.DRONES["Mouse"]), 1)
        self.assertEqual(d.charge_hours(d.DRONES["Roach"]), 3)
        self.assertEqual(d.charge_hours(d.DRONES["Shrike"]), 6)
        self.assertEqual(d.charge_hours(d.DRONES["Kerberos"]), 6)

    def test_parts_cost_a_quarter_of_base_price(self) -> None:
        self.assertEqual(d.parts_cost(d.DRONES["Mouse"]), 125)
        self.assertEqual(d.parts_cost(d.DRONES["Pitbull"]), 1_250)

    def test_zero_hit_points_is_destruction_not_damage(self) -> None:
        self.assertTrue(d.is_destroyed(0))
        self.assertTrue(d.is_destroyed(-3))
        self.assertFalse(d.is_destroyed(1))


class BatteryRuleTests(unittest.TestCase):
    def test_battery_hours_constant(self) -> None:
        self.assertEqual(d.BATTERY_HOURS, 1)
        self.assertEqual(d.SAFE_CONTROL_METERS, 1_000)
        self.assertEqual(d.MAX_CONTROL_METERS, 8_000)
        self.assertEqual(d.FLYING_ALTITUDE_METERS, 1_000)


if __name__ == "__main__":
    unittest.main()
