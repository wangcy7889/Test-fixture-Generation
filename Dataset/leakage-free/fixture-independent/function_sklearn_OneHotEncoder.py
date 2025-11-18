
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def one_hot_encoding(data):

    if not isinstance(data, np.ndarray):
        raise TypeError("Input data must be a numpy array.")
    if len(data.shape) < 2 or data.shape[1] < 2:
        raise IndexError("The input data has incorrect structure.")

    try:
        categorical_data = data[:, :-1]
        numeric_data = data[:, -1].reshape(-1, 1)
    except IndexError:
        raise IndexError("Data structure is incorrect. Maybe missing categorical or numeric part.")

    encoder = OneHotEncoder()
    encoded_categorical_data = encoder.fit_transform(categorical_data)
    final_data = np.concatenate((numeric_data, encoded_categorical_data.toarray()), axis=1)
    return final_data