import numpy as np
from FrameBuffer import *
import math


class Vec5:
    def __init__(self, x, y, z, u, v):
        self.x = x
        self.y = y
        self.z = z

        self.u = u
        self.v = v

    def __add__(self, other):
        return Vec5(self.x + other.x, self.y + other.y, self.z + other.z, self.u + other.u, self.v + other.v)

    def __sub__(self, other):
        return Vec5(self.x - other.x, self.y - other.y, self.z - other.z, self.u - other.u, self.v - other.v)

    def __mul__(self, scalar):
        return Vec5(self.x * scalar, self.y * scalar, self.z * scalar, self.u * scalar, self.v * scalar)

    def __truediv__(self, scalar):
        return Vec5(self.x / scalar, self.y / scalar, self.z / scalar, self.u / scalar, self.v / scalar)


# Create a frame buffer of size 100x100 as global variable
fb = FrameBuffer(100, 100)


def DrawFlatTopTriangle(v0, v1, v2, color):
    # 特殊情况判断
    if v2.y == v0.y:
        return  # 防止遇到这种奇葩：[[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]]

    # 计算三角形两条边的Vector增量
    delta_y = v2.y - v0.y
    dv0 = (v2 - v0) / delta_y
    dv1 = (v2 - v1) / delta_y

    # 计算扫描线的yStart和yEnd坐标
    yStart = math.ceil(v0.y - 0.5)
    yEnd = math.ceil(v2.y - 0.5)  # 注意，这里是最后绘制那根线+1
    # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

    # 创建Interpolator
    itEdge0 = v0  # 左侧边界Interpolator
    itEdge1 = v1  # 右侧边界Interpolator

    # 进行Interpolator Pre Step，确保起始点在像素中央
    itEdge0 += dv0 * (yStart + 0.5 - v0.y)
    itEdge1 += dv1 * (yStart + 0.5 - v0.y)

    for y in range(int(yStart), int(yEnd)):

        # 计算“这行”扫描线的xStart和xEnd坐标
        xStart = math.ceil(itEdge0.x - 0.5)
        xEnd = math.ceil(itEdge1.x - 0.5)  # 注意，这里是最后绘制那个像素+1
        # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

        delta = (itEdge1 - itEdge0) / (itEdge1.x / itEdge0.x)
        interpolator = itEdge0 + delta * (xStart + 0.5 - itEdge0.x)

        for x in range(int(xStart), int(xEnd)):
            fb.set_pixel(x, y, color)
            interpolator += delta

        # 每次扫描线循环，递增Interpolator
        itEdge0 += dv0
        itEdge1 += dv1


def DrawFlatBottomTriangle(v0, v1, v2, color):
    # 特殊情况判断
    if v1.y == v0.y:
        return  # 防止遇到这种奇葩：[[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]]

    # 计算三角形两条边的Vector增量
    delta_y = v2.y - v0.y
    dv0 = (v1 - v0) / delta_y
    dv1 = (v2 - v0) / delta_y

    # 计算扫描线的yStart和yEnd坐标
    yStart = math.ceil(v0.y - 0.5)
    yEnd = math.ceil(v2.y - 0.5)  # 注意，这里是最后绘制那根线+1
    # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

    # 创建Interpolator
    itEdge0 = v0  # 左侧边界Interpolator
    itEdge1 = v0  # 右侧边界Interpolator

    # 进行Interpolator Pre Step，确保起始点在像素中央
    itEdge0 += dv0 * (yStart + 0.5 - v0.y)
    itEdge1 += dv1 * (yStart + 0.5 - v0.y)

    for y in range(int(yStart), int(yEnd)):

        # 计算“这行”扫描线的xStart和xEnd坐标
        xStart = math.ceil(itEdge0.x - 0.5)
        xEnd = math.ceil(itEdge1.x - 0.5)  # 注意，这里是最后绘制那个像素+1
        # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

        delta = (itEdge1 - itEdge0) / (itEdge1.x / itEdge0.x)
        interpolator = itEdge0 + delta * (xStart + 0.5 - itEdge0.x)

        for x in range(int(xStart), int(xEnd)):
            fb.set_pixel(x, y, color)
            interpolator += delta

        # 每次扫描线循环，递增Interpolator
        itEdge0 += dv0
        itEdge1 += dv1


def DrawTriangle(v0, v1, v2, color):

    # 对顶点进行排序（按照y坐标，从小到大）
    vertices = [v0, v1, v2]
    vertices.sort(key=lambda v: v.y)
    pv0, pv1, pv2 = vertices

    if pv0.y == pv1.y:  # FlatTop三角形
        if pv1.x < pv0.x:  # 确保Top两个顶点，x坐标较小的，在左边
            pv0, pv1 = pv1, pv0
        DrawFlatTopTriangle(pv0, pv1, pv2, color)

    elif pv1.y == pv2.y:  # FlatBottom三角形
        if pv2.x < pv1.x:  # 确保Bottom两个顶点，x坐标较小的，在左边
            pv1, pv2 = pv2, pv1
        DrawFlatBottomTriangle(pv0, pv1, pv2, color)

    else:  # Regular三角形，需要分解为：一个FlatTop + 一个FlatBottom
        alphaSplit = (pv1.y - pv0.y) / (pv2.y - pv0.y)  # 切割系数
        vi = pv0 + (pv2 - pv0) * alphaSplit  # 切割出来的新顶点

        if pv1.x < vi.x:  # MajorRight的Regular三角形
            DrawFlatBottomTriangle(pv0, pv1, vi, color)
            DrawFlatTopTriangle(pv1, vi, pv2, color)

        else:  # MajorLeft的Regular三角形
            DrawFlatBottomTriangle(pv0, vi, pv1, color)
            DrawFlatTopTriangle(vi, pv1, pv2, color)


def GeneratePoints(theta):
    # Order: X-Y-Z; OpenGL Right Hand Coordination System

    A = Vec5(np.float64(-1), np.sin(theta), -np.cos(theta), 0, 0)
    B = Vec5(np.float64(1), np.sin(theta), -np.cos(theta), 1, 0)
    C = Vec5(np.float64(-1), -np.sin(theta), np.cos(theta), 0, 1)
    D = Vec5(np.float64(1), -np.sin(theta), np.cos(theta), 1, 1)

    return [A, B, C, D]


def FarAwayPoints(points):
    # from z-minimum of 1 to sth in front of focal plane "-1.5", 1 + (-2.5) = (-1.5)

    points_prime = []

    for point in points:
        points_prime.append(
            Vec5(point.x, point.y, point.z - 2.5, point.u, point.v)
        )

    return points_prime


def PerspProject(points):
    # Fixed Resolution: (100, 100), with a center in (50, 50)

    points_prime = []

    for point in points:
        x_1 = point.x / -point.z
        y_1 = point.y / -point.z

        x = 50 + x_1 * 50
        y = 50 - y_1 * 50

        points_prime.append(
            Vec5(x, y, point.z, point.u, point.v)
        )

    return points_prime


if __name__ == "__main__":
    points = GeneratePoints(theta=np.pi/4)
    points = FarAwayPoints(points)
    points = PerspProject(points)

    # Quad Surface
    DrawTriangle(points[0], points[1], points[2], (127, 0, 0))
    DrawTriangle(points[3], points[1], points[2], (127, 127, 0))

    # Quad Vertex
    for point in points:
        fb.set_pixel(
            int(point.x),
            int(point.y),
            (255, 255, 255)
        )

    fb.display()
