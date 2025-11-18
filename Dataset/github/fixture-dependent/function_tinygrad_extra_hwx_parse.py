from macholib import MachO

def get_macho(fn):
    dat = open(fn, 'rb').read()
    dat = b'\xcf\xfa\xed\xfe' + dat[4:]
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(delete=False) as f:
        f.write(dat)
        f.close()
    return MachO.MachO(f.name)