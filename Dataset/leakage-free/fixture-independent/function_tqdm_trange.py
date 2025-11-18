from tqdm import trange


def f_trange(start, stop, step, desc='General trange loop', ascii=True, miniters=None, maxinterval=None, mininterval=None):
    results = []
    for i in trange(start, stop, step, desc=desc, ascii=ascii, miniters=miniters, maxinterval=maxinterval, mininterval=mininterval):
        result = i * 2
        results.append(result)
    return results