import numpy as np
from xgboost import XGBRegressor

def xgboost(features: np.ndarray, target: np.ndarray, test_features: np.ndarray) -> np.ndarray:
    xgb = XGBRegressor(verbosity=0, random_state=42, tree_method='exact', base_score=0.5)
    xgb.fit(features, target)
    predictions = xgb.predict(test_features)
    predictions = predictions.reshape(len(predictions), 1)
    return predictions