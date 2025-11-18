from pyod.models.knn import KNN
import numpy as np

def detect_outliers_KNN(data, contamination=0.1):

    knn_model = KNN(contamination=contamination)
    
    knn_model.fit(data)
    
    outliers = knn_model.predict(data)
    
    return outliers
