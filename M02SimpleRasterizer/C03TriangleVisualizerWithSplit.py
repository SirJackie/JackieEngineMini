import matplotlib.pyplot as plt
import matplotlib.patches as patches

triangles_split = []

triangles = [
    [[1, 1], [2, 4], [6, 2]],
    [[1, 6], [5, 6], [7, 4]],
    [[5, 6], [8, 7], [7, 4]],
    [[8, 7], [9.5, 5.5], [7, 4]],

    [[7.74, 2.51], [11.74, 2.51], [9.74, 0.77]],
    [[7.74, 2.51], [9.5, 5.25], [11.74, 2.51]],
    [[13.5, 1.5], [14.5, 2.5], [15, 0]],
    [[13.5, 1.5], [14.5, 4.5], [14.5, 2.5]],

    [[13.5, 5.5], [13.5, 7.5], [15.5, 5.5]],
    [[13.5, 7.5], [15.5, 7.5], [15.5, 5.5]],
    [[5.25, 1.27], [6.25, 1.27], [6.25, 0.27]],
    [[6.5, 1.5], [7.5, 1.5], [7.5, 0.5]],

    [[11.5, 4.5], [11.5, 6.5], [12.5, 5.5]],
    [[9.5, 7.5], [9.5, 7.9], [10.5, 7.5]],
    [[4.5, 0.5], [4.5, 0.5], [4.5, 0.5]]
]


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


def DrawFlatTopTriangle(pv0, pv1, pv2, color):
    triangles_split.append([pv0, pv1, pv2])


def DrawFlatBottomTriangle(pv0, pv1, pv2, color):
    triangles_split.append([pv0, pv1, pv2])


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


if __name__ == "__main__":

    for triangle in triangles:
        v0 = Vec2(triangle[0][0], triangle[0][1])
        v1 = Vec2(triangle[1][0], triangle[1][1])
        v2 = Vec2(triangle[2][0], triangle[2][1])
        DrawTriangle(v0, v1, v2, None)

    # 创建一个新的绘图
    fig, ax = plt.subplots()

    # 绘制每一个三角形
    for triangle_object in triangles_split:
        triangle = [
            [triangle_object[0].x, triangle_object[0].y],
            [triangle_object[1].x, triangle_object[1].y],
            [triangle_object[2].x, triangle_object[2].y]
        ]
        polygon = patches.Polygon(triangle, closed=True, edgecolor='blue', fill=False, linewidth=2)
        ax.add_patch(polygon)

    # 设置轴的范围
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.invert_yaxis()
    ax.set_aspect('equal', 'box')

    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks([i for i in range(0, 17)])
    plt.yticks([i for i in range(0, 9)])

    # 显示图形
    plt.title("Triangle Wireframes")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()
