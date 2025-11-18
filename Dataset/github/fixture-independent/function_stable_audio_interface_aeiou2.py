import numpy as np

def power_to_db(spec, *, amin=1e-10):
    magnitude = np.asarray(spec)
    log_spec = 10.0 * np.log10(np.maximum(amin, magnitude))
    log_spec -= 10.0 * np.log10(np.maximum(amin, 1))
    log_spec = np.maximum(log_spec, log_spec.max() - 80)
    return log_spec