import os

SERIAL_PORT = "/dev/tty.usbserial-B0044FJ3"
BAUD_RATE = 115200

# Video settings
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# RGB settings
RGB_BOX_COUNT = 3
RGB_BOX_WIDTH = 75
RGB_BOX_HEIGHT = 400

RGB_BOX_START_Y = 230

# current color
CURRENT_RGB_COLOR_BOX_START = (600, 14)

# Text Points
FPS_START_POINTS = (25, 60)
RESERT_BUTTON_START_POINTS = (15, 100)
PRESS_ESC_POINTS_START_POINTS = (950, 60)
CURRENT_RGB_COLOR_TEXT = (425, 60)

MODEL_PATH = os.path.abspath(os.path.join(
    os.getcwd(), "models", "hand_landmarker.task"))
