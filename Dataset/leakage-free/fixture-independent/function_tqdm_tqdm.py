from tqdm import tqdm


def f_tqdm(data):
    result = []
    for element in tqdm(data):
        result.append(element)
    return result