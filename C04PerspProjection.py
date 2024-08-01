import numpy as np
from FrameBuffer import *


def GeneratePoints(theta):
    # Order: X-Y-Z; OpenGL Right Hand Coordination System

    A = [np.float64(-1), np.sin(theta), -np.cos(theta)]
    B = [np.float64(1), np.sin(theta), -np.cos(theta)]
    C = [np.float64(-1), -np.sin(theta), np.cos(theta)]
    D = [np.float64(1), -np.sin(theta), np.cos(theta)]

    return [A, B, C, D]


def FarAwayPoints(points):
    # from z-minimum of 1 to sth in front of focal plane "-1.5", 1 + (-2.5) = (-1.5)

    points_prime = []

    for point in points:
        x = point[0]
        y = point[1]
        z = point[2] - 2.5
        points_prime.append([x, y, z])

    return points_prime


def PerspProject(points):
    # Fixed Resolution: (100, 100), with a center in (50, 50)

    points_2d = []

    for point in points:
        x_1 = point[0] / -point[2]
        y_1 = point[1] / -point[2]

        x = 50 + x_1 * 25
        y = 50 - y_1 * 25

        points_2d.append([x, y])

    return points_2d


if __name__ == "__main__":
    fb = FrameBuffer(100, 100)

    points = GeneratePoints(theta=np.pi/4)
    points = FarAwayPoints(points)

    points_2d = PerspProject(points)

    for point_2d in points_2d:
        fb.set_pixel(
            int(point_2d[0]),
            int(point_2d[1]),
            (255, 255, 255)
        )

    fb.display()
