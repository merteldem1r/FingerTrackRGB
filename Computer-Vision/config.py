import os

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

RGB_BOX_COUNT = 3
RGB_BOX_WIDTH = 100
RGB_BOX_HEIGHT = 510

FPS_START_POINTS = (25, 60)

MODEL_PATH = os.path.abspath(os.path.join(
    os.getcwd(), "models", "hand_landmarker.task"))
