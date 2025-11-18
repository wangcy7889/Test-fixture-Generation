import numpy as np

def angle_to_vector(self) -> None:
    pitch, yaw = self.normalized_gaze_angles
    self.normalized_gaze_vector = -np.array([np.cos(pitch) * np.sin(yaw), np.sin(pitch), np.cos(pitch) * np.cos(yaw)])