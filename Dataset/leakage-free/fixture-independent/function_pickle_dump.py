import pickle


def f_dump(data, file):
    try:
        pickle.dump(data, file)
        return True
    except Exception:
        return False