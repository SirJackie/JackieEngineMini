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
