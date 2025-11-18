import multiprocessing as mp
import numpy as np
import pyaudio
RATE = 16000
CHUNK = 1600

def listener(q: mp.Queue, event: mp.Event):
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
        did_print = False
        while True:
            data = stream.read(CHUNK)
            if event.is_set():
                if not did_print:
                    print('listening')
                    did_print = True
                q.put((np.frombuffer(data, np.int16) / 32768).astype(np.float32) * 3)
            else:
                did_print = False
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()