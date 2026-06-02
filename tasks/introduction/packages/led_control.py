import colorsys
from typing import List


def set_turning_leds(direction: str) -> dict:
    """Set LEDs to indicate turning direction.

    direction: 'left' | 'right' | 'forward' | 'stop'
    Returns a dict mapping LED index -> [r, g, b]  (values 0.0–1.0).
    LED positions: 0=front-left, 2=front-right, 3=rear-right, 4=rear-left
    """
    ORANGE = [1.0, 0.5, 0.0]
    WHITE  = [1.0, 1.0, 1.0]
    RED    = [1.0, 0.0, 0.0]
    OFF    = [0.0, 0.0, 0.0]

    if direction == 'left':
        return {0: ORANGE, 2: OFF,   3: OFF,   4: ORANGE}
    elif direction == 'right':
        return {0: OFF,    2: ORANGE, 3: ORANGE, 4: OFF}
    elif direction == 'forward':
        return {0: WHITE,  2: WHITE,  3: OFF,   4: OFF}
    elif direction == 'stop':
        return {0: OFF,    2: OFF,    3: RED,   4: RED}
    else:
        return {0: OFF,    2: OFF,    3: OFF,   4: OFF}
