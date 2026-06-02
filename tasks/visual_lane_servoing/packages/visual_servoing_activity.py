from typing import Tuple
import os
import numpy as np
import cv2
import yaml

_HSV_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config', 'lane_servoing_hsv_config.yaml')
try:
    with open(_HSV_FILE) as _f:
        _h = yaml.safe_load(_f) or {}
except FileNotFoundError:
    _h = {}

_yellow_lower = np.array([_h.get('yellow_lower_h', 0),  _h.get('yellow_lower_s', 0),  _h.get('yellow_lower_v', 0)])
_yellow_upper = np.array([_h.get('yellow_upper_h', 0),  _h.get('yellow_upper_s', 0), _h.get('yellow_upper_v', 0)])

_white_lower = np.array([_h.get('white_lower_h', 0),   _h.get('white_lower_s', 0), _h.get('white_lower_v', 0)])
_white_upper = np.array([_h.get('white_upper_h', 0), _h.get('white_upper_s', 0), _h.get('white_upper_v', 0)])

def detect_lane_markings(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    h, w = image.shape[:2]

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (0, 0), 3)
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1)
    gmag = np.sqrt(sobelx * sobelx + sobely * sobely)

    mask_mag = (gmag > 40)
    mask_sx_pos = (sobelx > 0)
    mask_sx_neg = (sobelx < 0)
    mask_sy_neg = (sobely < 0)

    mask_ground = np.zeros((h, w), dtype=np.uint8)
    mask_ground[int(h * 0.4):, :] = 1

    mid = w // 2
    mask_left_half = np.zeros((h, w), dtype=np.uint8)
    mask_left_half[:, :mid] = 1
    mask_right_half = np.zeros((h, w), dtype=np.uint8)
    mask_right_half[:, mid:] = 1

    mask_yellow = cv2.inRange(hsv, _yellow_lower, _yellow_upper) > 0
    mask_white = cv2.inRange(hsv, _white_lower, _white_upper) > 0

    mask_left = (mask_ground * mask_left_half * mask_mag *
                 mask_sx_neg * mask_sy_neg * mask_yellow).astype(np.uint8)
    mask_right = (mask_ground * mask_right_half * mask_mag *
                  mask_sx_pos * mask_sy_neg * mask_white).astype(np.uint8)

    return mask_left, mask_right




def set_hsv_bounds(yellow_lower, yellow_upper, white_lower, white_upper):
    global _yellow_lower, _yellow_upper, _white_lower, _white_upper
    _yellow_lower    = np.array(yellow_lower)
    _yellow_upper    = np.array(yellow_upper)
    _white_lower = np.array(white_lower)
    _white_upper = np.array(white_upper)

def get_hsv_bounds():
    return {
        'yellow_lower_h': int(_yellow_lower[0]),    'yellow_upper_h': int(_yellow_upper[0]),
        'yellow_lower_s': int(_yellow_lower[1]),    'yellow_upper_s': int(_yellow_upper[1]),
        'yellow_lower_v': int(_yellow_lower[2]),    'yellow_upper_v': int(_yellow_upper[2]),
        'white_lower_h':  int(_white_lower[0]), 'white_upper_h':  int(_white_upper[0]),
        'white_lower_s':  int(_white_lower[1]), 'white_upper_s':  int(_white_upper[1]),
        'white_lower_v':  int(_white_lower[2]), 'white_upper_v':  int(_white_upper[2]),
    }