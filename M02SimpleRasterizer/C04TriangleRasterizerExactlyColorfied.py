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
    if v2.y == v0.y:
        return  # 防止遇到这种奇葩：[[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]]

    m0 = (v2.x - v0.x) / (v2.y - v0.y)
    m1 = (v2.x - v1.x) / (v2.y - v1.y)

    yStart = math.ceil(v0.y - 0.5)
    yEnd = math.ceil(v2.y - 0.5)

    for y in range(int(yStart), int(yEnd)):
        px0 = m0 * (float(y) + 0.5 - v0.y) + v0.x
        px1 = m1 * (float(y) + 0.5 - v1.y) + v1.x

        xStart = math.ceil(px0 - 0.5)
        xEnd = math.ceil(px1 - 0.5)

        for x in range(int(xStart), int(xEnd)):
            fb.set_pixel(x, y, color)


def DrawFlatBottomTriangle(v0, v1, v2, color):
    if v1.y == v0.y:
        return  # 防止遇到这种奇葩：[[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]]

    m0 = (v1.x - v0.x) / (v1.y - v0.y)
    m1 = (v2.x - v0.x) / (v2.y - v0.y)

    yStart = math.ceil(v0.y - 0.5)
    yEnd = math.ceil(v2.y - 0.5)

    for y in range(int(yStart), int(yEnd)):
        px0 = m0 * (float(y) + 0.5 - v0.y) + v0.x
        px1 = m1 * (float(y) + 0.5 - v0.y) + v0.x

        xStart = math.ceil(px0 - 0.5)
        xEnd = math.ceil(px1 - 0.5)

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


def DrawTriangleVecList(vecList, color):
    v0 = Vec2(vecList[0][0], vecList[0][1])
    v1 = Vec2(vecList[1][0], vecList[1][1])
    v2 = Vec2(vecList[2][0], vecList[2][1])
    DrawTriangle(v0, v1, v2, color)


if __name__ == "__main__":

    DrawTriangleVecList([[1, 1], [2, 4], [6, 2]], (255, 0, 0))
    DrawTriangleVecList([[1, 6], [5, 6], [7, 4]], (255, 255, 0))
    DrawTriangleVecList([[5, 6], [8, 7], [7, 4]], (255, 0, 0))
    DrawTriangleVecList([[8, 7], [9.5, 5.5], [7, 4]], (255, 255, 0))

    DrawTriangleVecList([[7.74, 2.5], [11.74, 2.5], [9.74, 0.77]], (255, 255, 0))
    DrawTriangleVecList([[7.74, 2.5], [9.5, 5.25], [11.74, 2.5]], (255, 0, 0))
    DrawTriangleVecList([[13.5, 1.5], [14.5, 2.5], [15, 0]], (255, 0, 0))
    DrawTriangleVecList([[13.5, 1.5], [14.5, 4.5], [14.5, 2.5]], (255, 0, 0))

    DrawTriangleVecList([[13.5, 5.5], [13.5, 7.5], [15.5, 5.5]], (255, 0, 0))
    DrawTriangleVecList([[13.5, 7.5], [15.5, 7.5], [15.5, 5.5]], (255, 255, 0))
    DrawTriangleVecList([[5.25, 1.27], [6.25, 1.27], [6.25, 0.27]], (255, 0, 0))
    DrawTriangleVecList([[6.5, 1.5], [7.5, 1.5], [7.5, 0.5]], (255, 0, 0))

    DrawTriangleVecList([[11.5, 4.5], [11.5, 6.5], [12.5, 5.5]], (255, 255, 0))
    DrawTriangleVecList([[9.5, 7.5], [9.5, 7.9], [10.5, 7.5]], (255, 0, 0))
    DrawTriangleVecList([[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]], (255, 0, 0))

    # Display the frame buffer
    fb.display()
    fb.display_debug()
