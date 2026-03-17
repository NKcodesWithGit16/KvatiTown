import cv2
import numpy as np
from typing import Tuple


def get_yellow_mask(image_rgb: np.ndarray, hsv_config: dict) -> np.ndarray:
    """
    Detect yellow duck pixels using HSV color thresholding.

    Args:
        image_rgb: RGB image (H x W x 3)
        hsv_config: dict with keys lower_h, lower_s, lower_v, upper_h, upper_s, upper_v

    Returns:
        Binary mask (H x W), 255 where yellow detected, 0 elsewhere
    """
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)

    lower = np.array([
        hsv_config['lower_h'],
        hsv_config['lower_s'],
        hsv_config['lower_v'],
    ], dtype=np.uint8)

    upper = np.array([
        hsv_config['upper_h'],
        hsv_config['upper_s'],
        hsv_config['upper_v'],
    ], dtype=np.uint8)

    mask = cv2.inRange(image_hsv, lower, upper)
    return mask


def get_motor_speeds(image_rgb: np.ndarray, hsv_config: dict, config: dict) -> Tuple[float, float]:
    """
    Braitenberg vehicle: move forward while avoiding yellow ducks.

    The image is split into a left and right half.  The number of yellow
    pixels detected in each half drives the ipsilateral wheel faster,
    which steers the robot *away* from the duck (Vehicle 2b / aggressor
    wiring with excitatory connections):

        duck on LEFT  → left wheel faster  → robot turns RIGHT
        duck on RIGHT → right wheel faster → robot turns LEFT

    Args:
        image_rgb: Current camera frame in RGB (H x W x 3)
        hsv_config: HSV thresholds for yellow color detection
        config: dict with
            'const'               – base forward speed  (0–1)
            'gain'                – how strongly to react to detections
            'detection_threshold' – minimum yellow pixels (per half) to react

    Returns:
        (left_speed, right_speed), each clamped to [-1.0, 1.0]
    """
    const = float(config.get('const', 0.3))
    gain = float(config.get('gain', 1.5))
    threshold = float(config.get('detection_threshold', 100.0))

    mask = get_yellow_mask(image_rgb, hsv_config)

    h, w = mask.shape
    mid = w // 2

    left_count = float(np.sum(mask[:, :mid] > 0))
    right_count = float(np.sum(mask[:, mid:] > 0))

    # Normalize by half-image pixel count
    half_pixels = float(h * mid) or 1.0
    left_norm = left_count / half_pixels
    right_norm = right_count / half_pixels

    # If both halves are below threshold: drive straight
    if left_count < threshold and right_count < threshold:
        return const, const

    # Braitenberg avoidance: same-side excitatory connection
    left_speed = const + gain * left_norm
    right_speed = const + gain * right_norm

    left_speed = float(max(-1.0, min(1.0, left_speed)))
    right_speed = float(max(-1.0, min(1.0, right_speed)))

    return left_speed, right_speed
