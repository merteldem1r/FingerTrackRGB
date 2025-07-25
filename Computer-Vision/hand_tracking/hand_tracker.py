import config
import mediapipe as mp
import threading
import cv2
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python.vision.hand_landmarker import (
    HandLandmarker,
    HandLandmarkerOptions,
    HandLandmarkerResult
)
from mediapipe.framework.formats import landmark_pb2

"""
Author: MERT ELDEMIR
I have created own class, based on functions of the library that shown in link below
Google Mediapipe Link: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python
"""

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green


class RealTimeHandTracker():
    def __init__(self):
        self.result: HandLandmarkerResult = None
        self.result_lock = threading.Lock()
        self.landmarker: HandLandmarker = None
        self.last_tick_count = cv2.getTickCount()
        self.fps = 0

    def initialize_tracker(self):
        # callback function
        def set_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
            with self.result_lock:
                self.result = result

                # FPS calculation
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
            num_hands=2,
            result_callback=set_result)

        self.landmarker = HandLandmarker.create_from_options(options)

    # for HandLandmarkerResult and complete drawn frame result
    def set_hand_marker_result(self, frame):
        ticks = cv2.getTickCount()
        frequency = cv2.getTickFrequency()
        timestamp_ms = int((ticks / frequency) * 1000)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.landmarker.detect_async(
            image=mp_image, timestamp_ms=timestamp_ms)

    # get index finger points
    def get_index_finger_points(self):
        res = [(0, 0), (0, 0)]

        with self.result_lock:
            if not self.result or not self.result.hand_landmarks:
                return res

            hand_landmarks_list = self.result.hand_landmarks

        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            index_finger = hand_landmarks[8]
            index_finger_normalized_x = index_finger.x
            index_finger_normalized_y = index_finger.y

            x = int(index_finger_normalized_x * config.CAMERA_WIDTH)
            y = int(index_finger_normalized_y * config.CAMERA_HEIGHT)

            res[idx] = (x, y)

        return res

    def draw_landmarks_on_image(self, rgb_image):
        with self.result_lock:
            if not self.result or not self.result.hand_landmarks:
                return rgb_image

            hand_landmarks_list = self.result.hand_landmarks
            handedness_list = self.result.handedness

        annotated_image = np.copy(rgb_image)

        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            # Draw the hand landmarks.
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
            ])
            mp.solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                mp.solutions.hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style())

            # Get the top left corner of the detected hand's bounding box.
            height, width, _ = annotated_image.shape
            x_coordinates = [landmark.x for landmark in hand_landmarks]
            y_coordinates = [landmark.y for landmark in hand_landmarks]
            text_x = int(min(x_coordinates) * width)
            text_y = int(min(y_coordinates) * height) - MARGIN

        return annotated_image

    def destroy(self):
        # destroy landmarker
        self.landmarker.close()
