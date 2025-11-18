import soundfile as sf
import numpy as np
import logging

def boost_audio(path, gain=2.0):
    if not isinstance(gain, (int, float)):
        raise TypeError("Error: gain must be a number")
    try:
        data, rate = sf.read(path)
        data = np.clip(data * gain, -1.0, 1.0)
        sf.write(path, data, rate)
        print(f"The audio has been processed：{path}")
    except Exception as e:
        logging.error(f"Error: Error in handling audio：{e}")
        raise e
