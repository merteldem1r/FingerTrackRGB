import config
import utils.frame_util as FrameUtil
import sys
import cv2
import numpy as np
import mediapipe as mp
import time
# from custom class
from hand_tracking.hand_tracker import RealTimeHandTracker
import hand_tracking.utils as HandTrackerUtil
import utils.coordinates as CoordinatesUtil

# Video settings
source = cv2.VideoCapture(0)
source.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
source.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

actual_width = source.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = source.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Camera resolution: {actual_width} x {actual_height}")

if not source.isOpened():
    print("Error: While openning camera")
    sys.exit()

win_name = "hand_detection"
cv2.namedWindow(win_name)

# Hand Tracker initialization
hand_tracker = RealTimeHandTracker()
hand_tracker.initialize_tracker()

fps_text = f"FPS: {hand_tracker.fps}"
fps_text_points = config.FPS_START_POINTS


# RGB and Finger points
index_finger_points = (0, 0)
RGB_Values = [0, 0, 0]
last_box_finger_points = [
    (0, 0),  # RED box
    (0, 0),  # GREEN box
    (0, 0),  # BLUE
]

out_start_tick = cv2.getTickCount()
while True:
    has_frame, frame = source.read()
    frame = cv2.flip(frame, 1)

    if not has_frame:
        print("Error: Frame not found")
        break

    # get handmark result and draw landmark
    hand_tracker.set_hand_marker_result(frame)
    frame = HandTrackerUtil.drawLandmarksOnImage(
        rgb_image=frame, detection_result=hand_tracker.result)

    # update index finger points
    finger_points_res = hand_tracker.get_index_finger_points()
    if finger_points_res != None:
        index_finger_points = finger_points_res

    # RGB boxes
    rgb_box_points = FrameUtil.drawBoxesRGB(frame, RGB_Values)
    finger_box_coordinates = CoordinatesUtil.getFingerInBoxRgbCoordinates(
        index_finger_points, rgb_box_points)

    # change RGB and box values if finger in BOX
    if finger_box_coordinates[0] != 3:
        if finger_box_coordinates[0] == 0:
            # finger FOUND in RED BOX
            print("RED box")
            last_box_finger_points[0] = finger_box_coordinates[1]
        elif finger_box_coordinates[0] == 1:
            # finger FOUND in GREEN BOX
            print("GREEN box")
            last_box_finger_points[1] = finger_box_coordinates[1]
        elif finger_box_coordinates[0] == 2:
            # finger FOUND in BLUE BOX
            print("BLUE box")
            last_box_finger_points[2] = finger_box_coordinates[1]

        RGB_Values = CoordinatesUtil.getValueRGB(
            last_box_finger_points, rgb_box_points)

    print(RGB_Values)

    FrameUtil.fillBoxesWithFingerRGB(
        frame, rgb_box_points, last_box_finger_points)

    print(last_box_finger_points)

    # update fps every 200 ms
    if ((cv2.getTickCount() - out_start_tick) / cv2.getTickFrequency() >= 0.2):
        fps_text = f"FPS: {hand_tracker.fps}"
        out_start_tick = cv2.getTickCount()

    # fps display
    FrameUtil.drawTextBox(frame, fps_text, fps_text_points, 1.5, 2, [0, 0, 0])
    FrameUtil.drawText(frame, fps_text, fps_text_points,
                       [255, 255, 255], 1.5, 2)

    key = cv2.waitKey(1)
    if key == 27:
        print("Video capture stopped")
        break

    cv2.imshow(win_name, frame)


hand_tracker.destroy()
source.release()
cv2.destroyAllWindows()
