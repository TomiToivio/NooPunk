extends RefCounted
const Noosphere = preload("res://mods/noopunk/noosphere.gd")
func _eq(name: String, value: Variant, expected: Variant) -> Array:
    return [name, value == expected, "got %s expected %s" % [str(value), str(expected)]]
func run() -> Array:
    var rows: Array = []
    var m = Noosphere.new()
    rows.append(_eq("emotion is descriptive", m.choose_emotion("scared"), true))
    rows.append(_eq("unknown emotion refused", m.choose_emotion("omniscient"), false))
    rows.append(_eq("emotion has no attributes", m.to_dict().has("attribute_modifiers"), false))
    rows.append(_eq("unsupported psychic access refused",
        m.open_mind("psychic", true, false).get("reason"), "psi_capability_required"))
    rows.append(_eq("risky cyber operation delegates to core",
        m.open_mind("cybernetic", true, false, true).get("engine"), "cwn"))
    rows.append(_eq("contact does not grant powers",
        m.open_mind("psychic", true, true).get("grants_power"), false))
    rows.append(_eq("record physical observation",
        m.record_perception({"id":"a", "channel":"physical", "source":"lab", "observation":"trace"}),true))
    rows.append(_eq("record cyber observation",
        m.record_perception({"id":"b", "channel":"cybernetic", "source":"sensor", "observation":"log"}),true))
    rows.append(_eq("triangulation uses independent channels",
        m.triangulate(["a","b"])["independent_channels"],2))
    rows.append(_eq("interpretation belongs to player",m.interpret("a","possibly mundane"),true))
    rows.append(_eq("adding interpretation does not change evidence",
        m.evidence["a"].has("hypothesis"),false))
    rows.append(_eq("create threat clock",m.add_clock("nhi","NHI cell","disclosure"),true))
    rows.append(_eq("no arbitrary ticks",
        m.change_clock("nhi",1,"").get("reason"),"grounded_trigger_required"))
    rows.append(_eq("clock advances for documented event",
        m.change_clock("nhi",1,"verified leak").get("stage"),1))
    rows.append(_eq("countermeasure reverses progress",
        m.change_clock("nhi",-1,"credible public correction","secure corroboration").get("stage"),0))
    rows.append(_eq("player choice retained",
        m.record_choice("choice01","refused order"),true))
    rows.append(_eq("identity is not rolled",
        m.to_dict().has("roll"),false))
    return rows
