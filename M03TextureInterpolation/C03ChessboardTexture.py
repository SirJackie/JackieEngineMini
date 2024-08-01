import numpy as np
import matplotlib.pyplot as plt


def create_chessboard(board_size, square_size):
    # 创建棋盘基本结构
    chessboard = np.zeros((board_size * square_size, board_size * square_size), dtype=np.uint8)

    # 设置黑白交替方块
    for row in range(board_size):
        for col in range(board_size):
            if (row + col) % 2 == 0:
                chessboard[row * square_size:(row + 1) * square_size,
                           col * square_size:(col + 1) * square_size] = 255  # 白色方块

    return chessboard


if __name__ == "__main__":
    # 参数设置
    board_size = 4     # 棋盘的大小（8x8）
    square_size = 10   # 每个方块的像素大小

    # 生成棋盘
    chessboard = create_chessboard(board_size, square_size)

    # 显示棋盘
    plt.imshow(chessboard, cmap='gray')
    plt.axis('off')  # 关闭坐标轴
    plt.show()
