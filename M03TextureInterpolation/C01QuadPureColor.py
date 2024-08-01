import numpy as np
from FrameBuffer import *
import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)


# Create a frame buffer of size 100x100 as global variable
fb = FrameBuffer(16, 8)


def DrawFlatTopTriangle(v0, v1, v2, color):
    # 特殊情况判断
    if v2.y == v0.y:
        return  # 防止遇到这种奇葩：[[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]]

    # 计算三角形两条边的反斜率
    # 为什么用反斜率？因为反斜率kPrime对应deltaX，而正斜率k对应deltaY
    # 我们每行每行遍历，每行y+=1，所以x+=deltaX，反斜率更符合要求
    # 并且反斜率有个好处，不会出现除以0的情况（您可以带几个值试试看）
    m0 = (v2.x - v0.x) / (v2.y - v0.y)
    m1 = (v2.x - v1.x) / (v2.y - v1.y)

    # 计算扫描线的yStart和yEnd坐标
    yStart = math.ceil(v0.y - 0.5)
    yEnd = math.ceil(v2.y - 0.5)  # 注意，这里是最后绘制那根线+1
    # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

    for y in range(int(yStart), int(yEnd)):

        # 计算这行扫描线的：两个边缘端顶点
        # 注意，y一定要+0.5，因为像素中心都是有0.5的（例如(5.5, 7.5)是中心）
        px0 = m0 * (float(y) + 0.5 - v0.y) + v0.x
        px1 = m1 * (float(y) + 0.5 - v1.y) + v1.x

        # 计算“这行”扫描线的xStart和xEnd坐标
        xStart = math.ceil(px0 - 0.5)
        xEnd = math.ceil(px1 - 0.5)  # 注意，这里是最后绘制那个像素+1
        # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

        for x in range(int(xStart), int(xEnd)):
            fb.set_pixel(x, y, color)


def DrawFlatBottomTriangle(v0, v1, v2, color):
    # 特殊情况判断
    if v1.y == v0.y:
        return  # 防止遇到这种奇葩：[[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]]

    # 计算三角形两条边的反斜率
    # 为什么用反斜率？因为反斜率kPrime对应deltaX，而正斜率k对应deltaY
    # 我们每行每行遍历，每行y+=1，所以x+=deltaX，反斜率更符合要求
    # 并且反斜率有个好处，不会出现除以0的情况（您可以带几个值试试看）
    m0 = (v1.x - v0.x) / (v1.y - v0.y)
    m1 = (v2.x - v0.x) / (v2.y - v0.y)

    # 计算扫描线的yStart和yEnd坐标
    yStart = math.ceil(v0.y - 0.5)
    yEnd = math.ceil(v2.y - 0.5)  # 注意，这里是最后绘制那根线+1
    # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

    for y in range(int(yStart), int(yEnd)):

        # 计算这行扫描线的：两个边缘端顶点
        # 注意，y一定要+0.5，因为像素中心都是有0.5的（例如(5.5, 7.5)是中心）
        px0 = m0 * (float(y) + 0.5 - v0.y) + v0.x
        px1 = m1 * (float(y) + 0.5 - v0.y) + v0.x

        # 计算“这行”扫描线的xStart和xEnd坐标
        xStart = math.ceil(px0 - 0.5)
        xEnd = math.ceil(px1 - 0.5)  # 注意，这里是最后绘制那个像素+1
        # 为什么要+1？因为for循环左闭右开，进行+1完，才能变成左闭右闭

        for x in range(int(xStart), int(xEnd)):
            fb.set_pixel(x, y, color)


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

        x = 50 + x_1 * 50
        y = 50 - y_1 * 50

        points_2d.append([x, y])

    return points_2d


if __name__ == "__main__":
    fb = FrameBuffer(100, 100)

    points = GeneratePoints(theta=np.pi/4)
    points = FarAwayPoints(points)

    points_2d = PerspProject(points)

    # Quad Surface 1
    v0 = Vec2(points_2d[0][0], points_2d[0][1])
    v1 = Vec2(points_2d[1][0], points_2d[1][1])
    v2 = Vec2(points_2d[2][0], points_2d[2][1])
    DrawTriangle(v0, v1, v2, (127, 0, 0))

    # Quad Surface 2
    v0 = Vec2(points_2d[3][0], points_2d[3][1])
    v1 = Vec2(points_2d[1][0], points_2d[1][1])
    v2 = Vec2(points_2d[2][0], points_2d[2][1])
    DrawTriangle(v0, v1, v2, (127, 127, 0))

    # Quad Vertex
    for point_2d in points_2d:
        fb.set_pixel(
            int(point_2d[0]),
            int(point_2d[1]),
            (255, 255, 255)
        )

    fb.display()
