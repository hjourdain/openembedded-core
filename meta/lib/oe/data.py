import oe.maketype

def typed_value(key, d):
    """Construct a value for the specified metadata variable, using its flags
    to determine the type and parameters for construction."""
    var_type = d.getVarFlag(key, 'type')
    flags = d.getVarFlags(key)
    if flags is not None:
        flags = dict((flag, d.expand(value))
                     for flag, value in list(flags.items()))
    else:
        flags = {}

    try:
        return oe.maketype.create(d.getVar(key) or '', var_type, **flags)
    except (TypeError, ValueError) as exc:
        bb.msg.fatal("Data", "%s: %s" % (key, str(exc)))
