from tqdm import tqdm
import time


def progress_with_mininterval(mininterval_value):
    results = []
    for i in tqdm(range(10), mininterval=mininterval_value):
        time.sleep(0.1)
        results.append(i)
    return results