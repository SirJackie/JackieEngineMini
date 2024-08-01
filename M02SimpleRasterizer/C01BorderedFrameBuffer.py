from FrameBuffer import *


if __name__ == "__main__":
    # Create a frame buffer of size 100x100
    fb = FrameBuffer(50, 50)

    # Set some pixels to different colors
    fb.set_pixel(10, 10, (255, 0, 0))  # Red pixel
    fb.set_pixel(20, 20, (0, 255, 0))  # Green pixel
    fb.set_pixel(30, 30, (0, 0, 255))  # Blue pixel
    fb.set_pixel(40, 40, (255, 255, 0))  # Yellow pixel

    # Display the frame buffer
    fb.display()
    fb.display_debug()
