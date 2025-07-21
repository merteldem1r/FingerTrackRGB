import mediapipe as mp
import time
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python.vision.hand_landmarker import (
    HandLandmarker,
    HandLandmarkerOptions,
    HandLandmarkerResult
)
import config


class RealTimeHandTracker():
    def __init__(self):
        self.result = HandLandmarkerResult
        self.landmarker = HandLandmarker
        self.last_tick_count = cv2.getTickCount()
        self.fps = 0

    def initialize_tracker(self):
        # callback function
        def set_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
            self.result = result

            # fps calculations
            current_tick_count = cv2.getTickCount()
            time_passed = (current_tick_count -
                           self.last_tick_count) / cv2.getTickFrequency()
            if time_passed > 0:
                self.fps = int(1 / time_passed)
            self.last_tick_count = current_tick_count

        options = HandLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path=config.MODEL_PATH),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=set_result)

        self.landmarker = HandLandmarker.create_from_options(options)

    # for HandLandmarkerResult and complete drawn frame result
    def set_hand_marker_result(self, frame):
        timestamp_ms = int(time.time() * 1000)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.landmarker.detect_async(
            image=mp_image, timestamp_ms=timestamp_ms)

    # get index finger points
    def get_index_finger_points(self):
        try:
            hand_landmarks_list = self.result.hand_landmarks

            for idx in range(len(hand_landmarks_list)):
                hand_landmarks = hand_landmarks_list[idx]
                index_finger = hand_landmarks[8]
                index_finger_normalized_x = index_finger.x
                index_finger_normalized_y = index_finger.y

                x = int(index_finger_normalized_x * config.CAMERA_WIDTH)
                y = int(index_finger_normalized_y * config.CAMERA_HEIGHT)

                return (x, y)
        except:
            return (0, 0)

    def destroy(self):
        # destroy landmarker
        self.landmarker.close()
