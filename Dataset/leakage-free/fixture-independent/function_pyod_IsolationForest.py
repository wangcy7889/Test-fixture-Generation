from pyod.models.iforest import IForest
import numpy as np

def detect_outliers_isolation_forest(data, contamination=0.1):
    model = IForest(contamination=contamination)
    model.fit(data)
    return model.labels_

data = np.array([[1, 2], [2, 3], [3, 4], [10, 10], [3, 3]])
outliers = detect_outliers_isolation_forest(data)
print("Outlier labels:", outliers)
