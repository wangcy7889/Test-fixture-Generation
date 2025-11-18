import pandas as pd

def calculate_mean():
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]
    }
    df = pd.DataFrame(data)
    mean_values = df.mean()
    return f"success: {mean_values.to_dict()}"
