VERSION = (0, 0, 1)

def get_version(version=None):
    "Returns a PEP 386-compliant version number from VERSION."
    if version is None:
        version = VERSION
    else:
        assert len(version) == 3

    return ".".join(map(str, version))
