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


if __name__ == "__main__":
    # Create a frame buffer of size 100x100
    fb = FrameBuffer(100, 100)

    # Set some pixels to different colors
    fb.set_pixel(10, 10, (255, 0, 0))  # Red pixel
    fb.set_pixel(20, 20, (0, 255, 0))  # Green pixel
    fb.set_pixel(30, 30, (0, 0, 255))  # Blue pixel
    fb.set_pixel(40, 40, (255, 255, 0))  # Yellow pixel
    fb.set_pixel(50, 50, (255, 255, 255))  # White pixel

    # Display the frame buffer
    fb.display()

    # Clear the buffer with black color
    fb.clear()

    # Display the cleared buffer
    fb.display()
