import matplotlib.pyplot as plt
import matplotlib.patches as patches

triangles = [
    [[1, 1], [2, 4], [6, 2]],
    [[1, 6], [5, 6], [7, 4]],
    [[5, 6], [8, 7], [7, 4]],
    [[8, 7], [9.5, 5.5], [7, 4]],

    [[7.74, 2.5], [11.74, 2.5], [9.74, 0.77]],
    [[7.74, 2.5], [9.5, 5.25], [11.74, 2.5]],
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


if __name__ == "__main__":
    # 创建一个新的绘图
    fig, ax = plt.subplots()

    # 绘制每一个三角形
    for triangle in triangles:
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
