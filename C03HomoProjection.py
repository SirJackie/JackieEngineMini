import numpy as np
from FrameBuffer import *


def GeneratePoints(theta):
    # Order: X-Y-Z; OpenGL Right Hand Coordination System

    A = [np.float64(-1), np.sin(theta), -np.cos(theta)]
    B = [np.float64(1), np.sin(theta), -np.cos(theta)]
    C = [np.float64(-1), -np.sin(theta), np.cos(theta)]
    D = [np.float64(1), -np.sin(theta), np.cos(theta)]

    return [A, B, C, D]


def HomoProject(points):
    # Fixed Resolution: (100, 100), with a center in (50, 50)

    points_2d = []

    for point in points:
        x = 50 + point[0] * 25
        y = 50 + point[1] * 25
        points_2d.append([x, y])

    return points_2d


if __name__ == "__main__":
    fb = FrameBuffer(100, 100)

    points = GeneratePoints(theta=np.pi/2)
    points_2d = HomoProject(points)

    for point_2d in points_2d:
        fb.set_pixel(
            int(point_2d[0]),
            int(point_2d[1]),
            (255, 255, 255)
        )

    fb.display()
