import numpy as np
from FrameBuffer import *


def GeneratePoints(theta):
    # Order: X-Y-Z; OpenGL Right Hand Coordination System

    A = [np.float64(-1), np.sin(theta), -np.cos(theta)]
    B = [np.float64(1), np.sin(theta), -np.cos(theta)]
    C = [np.float64(-1), -np.sin(theta), np.cos(theta)]
    D = [np.float64(1), -np.sin(theta), np.cos(theta)]

    return [A, B, C, D]


if __name__ == "__main__":
    # Create a frame buffer of size 100x100
    fb = FrameBuffer(100, 100)
    x = GeneratePoints(0)
    pass
