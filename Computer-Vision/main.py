import utils.coordinates as CoordinatesUtil
from hand_tracking.hand_tracker import RealTimeHandTracker
from serial_com.serial import SerialComm
import config
import utils.frame_util as FrameUtil
import sys
import cv2


# Serial (UART) communication
ser = SerialComm()
print("Serial PORT:", ser.getSerialPort())

# Video settings
source = cv2.VideoCapture(0)
source.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
source.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

actual_width = source.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = source.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Camera resolution: {actual_width} x {actual_height}")

if not source.isOpened():
    print("Error: While openning camera")
    sys.exit(1)

win_name = "hand_detection"
cv2.namedWindow(win_name)

# Hand Tracker initialization
hand_tracker = RealTimeHandTracker()
hand_tracker.initialize_tracker()
hand_finger_points = (0, 0)

fps_text = f"FPS: {hand_tracker.fps}"
fps_text_points = config.FPS_START_POINTS

RGB_Values = [0, 0, 0]
last_box_finger_points = [
    (0, 0),  # in RED box
    (0, 0),  # in GREEN box
    (0, 0),  # in BLUE
]

out_start_tick = cv2.getTickCount()
while True:
    has_frame, frame = source.read()
    frame = cv2.flip(frame, 1)

    if not has_frame:
        print("Error: Frame not found")
        break

    # get handmark result and draw landmark
    hand_tracker.last_tick_count = cv2.getTickCount()

    hand_tracker.set_hand_marker_result(frame)

    # rgb reset button
    reset_points = FrameUtil.drawResetButtonRGB(frame, is_triggered=False)

    # update index finger points
    hands_finger_point_res = hand_tracker.get_index_finger_points()
    frame = hand_tracker.draw_landmarks_on_image(frame)

    # for each HAND
    for i in range(len(hands_finger_point_res)):
        hand_finger_points = hands_finger_point_res[i]

        # RGB boxes
        rgb_box_points = FrameUtil.drawBoxesRGB(frame, RGB_Values)
        finger_box_coordinates = CoordinatesUtil.getFingerInBoxRgbCoordinates(
            hand_finger_points, rgb_box_points)

        # change RGB and box values if finger in RGB box
        if finger_box_coordinates[0] != 3:
            if finger_box_coordinates[0] == 0:
                # finger FOUND in RED BOX
                last_box_finger_points[0] = finger_box_coordinates[1]
            elif finger_box_coordinates[0] == 1:
                # finger FOUND in GREEN BOX
                last_box_finger_points[1] = finger_box_coordinates[1]
            elif finger_box_coordinates[0] == 2:
                # finger FOUND in BLUE BOX
                last_box_finger_points[2] = finger_box_coordinates[1]

            RGB_Values = CoordinatesUtil.getValueRGB(
                last_box_finger_points, rgb_box_points)

            print("Last Box Finger Points: ", last_box_finger_points)
            print("RGB Values: ", RGB_Values)

            ser.set_rgb(RGB_Values)

        # for RGB reset button
        FrameUtil.fillBoxesWithFingerRGB(
            frame, rgb_box_points, last_box_finger_points, RGB_Values)

        if CoordinatesUtil.isFingerResetButton(hand_finger_points, reset_points):
            RGB_Values = [0, 0, 0]
            last_box_finger_points = [
                (0, 0),  # in RED box
                (0, 0),  # in GREEN box
                (0, 0),  # in BLUE
            ]
            ser.reset_rgb()
            print("Reset RGB triggered")
            reset_points = FrameUtil.drawResetButtonRGB(
                frame, is_triggered=True)

    # update fps every 200 ms
    if ((cv2.getTickCount() - out_start_tick) / cv2.getTickFrequency() >= 0.2):
        fps_text = f"FPS: {hand_tracker.fps}"
        out_start_tick = cv2.getTickCount()

    # fps display
    FrameUtil.drawTextBox(frame, fps_text, fps_text_points, 1.5, 2, [0, 0, 0])
    FrameUtil.drawText(frame, fps_text, fps_text_points,
                       [255, 255, 255], 1.5, 2)

    # esc display
    FrameUtil.drawTextBox(frame, "Prss ESC to close",
                          config.PRESS_ESC_POINTS_START_POINTS, 1, 2, [0, 0, 0])
    FrameUtil.drawText(frame, "Prss ESC to close", config.PRESS_ESC_POINTS_START_POINTS,
                       [255, 255, 255], 1, 2)

    # current rgb
    FrameUtil.drawTextBox(
        frame, "Color: ", config.CURRENT_RGB_COLOR_TEXT, 1.5, 2, [0, 0, 0])
    FrameUtil.drawText(frame, "Color:", config.CURRENT_RGB_COLOR_TEXT,
                       [255, 255, 255], 1.5, 2)
    cv2.rectangle(frame, config.CURRENT_RGB_COLOR_BOX_START,
                  (config.CURRENT_RGB_COLOR_BOX_START[0] + 100, config.CURRENT_RGB_COLOR_BOX_START[1] + 70), [RGB_Values[2], RGB_Values[1], RGB_Values[0]], cv2.FILLED)

    key = cv2.waitKey(1)
    if key == 27:
        print("Video capture stopped")
        break

    cv2.imshow(win_name, frame)


ser.close()
hand_tracker.destroy()
source.release()
cv2.destroyAllWindows()
