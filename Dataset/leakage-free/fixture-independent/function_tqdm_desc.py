from tqdm import tqdm


def f_desc(data, desc_text):
    results = []
    for element in tqdm(data, desc=desc_text):
        processed_element = element * 2
        results.append(processed_element)
    return results