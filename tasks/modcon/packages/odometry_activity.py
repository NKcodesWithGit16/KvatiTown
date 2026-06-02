from typing import Tuple
import numpy as np


def delta_phi(ticks: int, prev_ticks: int, resolution: int) -> Tuple[float, float]:
    alpha = 2 * np.pi / resolution
    dphi = alpha * (ticks - prev_ticks)
    return dphi, ticks


def pose_estimation(
    R: float,
    baseline: float,
    x_prev: float,
    y_prev: float,
    theta_prev: float,
    delta_phi_left: float,
    delta_phi_right: float,
) -> Tuple[float, float, float]:
    d_left = R * delta_phi_left
    d_right = R * delta_phi_right
    d_a = (d_left + d_right) / 2.0
    delta_theta = (d_right - d_left) / baseline

    theta = theta_prev + delta_theta
    x = x_prev + d_a * np.cos(theta_prev)
    y = y_prev + d_a * np.sin(theta_prev)

    return x, y, theta
