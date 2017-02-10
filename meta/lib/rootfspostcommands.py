import os

def sort_file(filename, mapping):
    """
    Sorts a passwd or group file based on the numeric ID in the third column.
    If a mapping is given, the name from the first column is mapped via that
    dictionary instead (necessary for /etc/shadow and /etc/gshadow). If not,
    a new mapping is created on the fly and returned.
    """
    new_mapping = {}
    with open(filename, 'rb+') as f:
        lines = f.readlines()
        # No explicit error checking for the sake of simplicity. /etc
        # files are assumed to be well-formed, causing exceptions if
        # not.
        for line in lines:
            entries = line.split(b':')
            name = entries[0]
            if mapping is None:
                id = int(entries[2])
            else:
                id = mapping[name]
            new_mapping[name] = id
        # Sort by numeric id first, with entire line as secondary key
        # (just in case that there is more than one entry for the same id).
        lines.sort(key=lambda line: (new_mapping[line.split(b':')[0]], line))
        # We overwrite the entire file, i.e. no truncate() necessary.
        f.seek(0)
        f.write(b''.join(lines))
    return new_mapping

def sort_passwd(sysconfdir):
    """
    Sorts passwd and group files in a rootfs /etc directory by ID.
    """
    for suffix in '', '-':
        for main, shadow in (('passwd', 'shadow'),
                             ('group', 'gshadow')):
            filename = os.path.join(sysconfdir, main + suffix)
            if os.path.exists(filename):
                mapping = sort_file(filename, None)
                filename = os.path.join(sysconfdir, shadow + suffix)
                if os.path.exists(filename):
                    sort_file(filename, mapping)
