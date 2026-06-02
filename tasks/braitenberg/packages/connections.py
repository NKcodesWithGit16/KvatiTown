from typing import Tuple
import numpy as np


# Fraction of image height to ignore at the bottom (road surface / lane markings)
_ROAD_MASK_FRACTION = 0.4


def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    """Left motor weight matrix: highest in middle-left, zero on road (bottom rows).

    Braitenberg avoidance wiring: ipsilateral excitatory connection.
    A duck on the LEFT activates the LEFT motor → robot turns RIGHT (away).
    The bottom _ROAD_MASK_FRACTION rows are zeroed to ignore yellow lane markings.
    """
    H, W = shape
    row = np.linspace(0.0, 1.0, H)[:, None]   # 0 at top, 1 at bottom
    col = np.linspace(1.0, 0.0, W)[None, :]   # 1 at left, 0 at right
    matrix = row * col
    # Zero out road/lane-marking region at the bottom
    cutoff = int(H * (1.0 - _ROAD_MASK_FRACTION))
    matrix[cutoff:, :] = 0.0
    return matrix


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    """Right motor weight matrix: highest in middle-right, zero on road (bottom rows).

    Braitenberg avoidance wiring: ipsilateral excitatory connection.
    A duck on the RIGHT activates the RIGHT motor → robot turns LEFT (away).
    The bottom _ROAD_MASK_FRACTION rows are zeroed to ignore yellow lane markings.
    """
    H, W = shape
    row = np.linspace(0.0, 1.0, H)[:, None]   # 0 at top, 1 at bottom
    col = np.linspace(0.0, 1.0, W)[None, :]   # 0 at left, 1 at right
    matrix = row * col
    # Zero out road/lane-marking region at the bottom
    cutoff = int(H * (1.0 - _ROAD_MASK_FRACTION))
    matrix[cutoff:, :] = 0.0
    return matrix
