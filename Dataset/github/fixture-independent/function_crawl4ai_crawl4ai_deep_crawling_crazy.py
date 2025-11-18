from __future__ import annotations
import numpy as np

def calculate_quantum_batch_size(depth: int, max_depth: int, frontier_size: int, visited_size: int) -> int:
    φ = (1 + 5 ** 0.5) / 2
    depth_factor = (max_depth - depth) / max_depth if depth < max_depth else 0
    harmonic = sum((1 / k for k in range(1, depth + 2)))
    batch_size = int(np.ceil(φ ** (depth_factor * 2) * np.log2(visited_size + 2) * (1 / harmonic) * max(1, min(20, frontier_size / 10))))
    return max(1, min(100, batch_size))