import config as cfg

def cleaner_aws(f):
    f = f.replace('_', '-')
    f = f.replace('@4x', '')
    f = f.replace('@5x', '')
    f = f.replace('2.0', '2-0')
    f = f.replace('-light-bg4x', '')
    f = f.replace('-light-bg', '')
    for p in cfg.FILE_PREFIXES['aws']:
        if f.startswith(p):
            f = f[len(p):]
            break
    return f.lower()