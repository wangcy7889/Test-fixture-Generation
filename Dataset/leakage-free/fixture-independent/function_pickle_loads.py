import pickle


def f_loads(data):
    serialized_data = pickle.dumps(data)
    return pickle.loads(serialized_data)