import numpy as np
import matplotlib.pyplot as plt


class FrameBuffer:
    def __init__(self, width, height):
        # Initialize a buffer with the given width and height
        # Each pixel is represented by a 3-element array for RGB
        self.width = width
        self.height = height
        self.buffer = np.zeros((height, width, 3), dtype=np.uint8)

    def set_pixel(self, x, y, color):
        # Set the pixel at (x, y) to the specified color
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y, x] = color
        else:
            print("Pixel out of bounds!")

    def clear(self, color=(0, 0, 0)):
        # Clear the buffer with the given color
        self.buffer[:] = color

    def display(self):
        # Display the buffer using matplotlib
        plt.imshow(self.buffer)
        plt.axis('off')  # Hide axis
        plt.show()

    def display_debug(self):
        # 获取原始图像的高度和宽度
        height, width, channels = self.buffer.shape

        # 创建一个新的6倍分辨率的图像，初始为全白色
        new_height = height * 6
        new_width = width * 6
        new_buffer = np.ones((new_height, new_width, channels), dtype=np.uint8) * 255

        # 遍历每个像素，填充到新图像中
        for y in range(height):
            for x in range(width):
                # 将原像素的颜色复制到6x6块的左上角5x5区域
                new_buffer[y * 6:y * 6 + 5, x * 6:x * 6 + 5] = self.buffer[y, x]

        plt.imshow(new_buffer)
        plt.axis('off')  # 隐藏坐标轴
        plt.show()
