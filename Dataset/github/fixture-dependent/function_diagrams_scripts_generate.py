import config as cfg

def up_or_title(pvd: str, s: str) -> str:
    if s in cfg.UPPER_WORDS.get(pvd, ()):
        return s.upper()
    if s in cfg.TITLE_WORDS.get(pvd, {}):
        return cfg.TITLE_WORDS[pvd][s]
    return s.title()