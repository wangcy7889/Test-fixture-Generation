import soundfile as sf
import numpy as np
import logging

def normalize_audio(path):

    try:
        data, rate = sf.read(path)
        max_amp = np.max(np.abs(data))
        if max_amp == 0:
            logging.warning("Error: The audio is empty or muted and no normalization is required")
            return
        normalized = data / max_amp
        sf.write(path, normalized, rate)
        print(f"The audio has been normalized：{path}")
    except Exception as e:
        logging.error(f"Error: Normalization failed：{e}")
        raise e
