import cv2
import config


def drawText(frame, text, points, color, font_scale, thickness):
    x, y = points
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness)


def drawTextBox(frame, text, text_points, font_scale, text_thickness, box_color):
    x, y = text_points

    text_size = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)
    label_size, baseline = text_size

    cv2.rectangle(
        frame, (x - 10, y - label_size[1] - baseline), (x + label_size[0] + 10, y + baseline + 10), box_color, thickness=cv2.FILLED, lineType=cv2.LINE_AA)


def drawBoxesRGB(frame, rgb_value):
    box_padding = int(
        (config.CAMERA_WIDTH - (config.RGB_BOX_COUNT *
         config.RGB_BOX_WIDTH)) / 4
    )

    box_start_y = config.RGB_BOX_START_Y
    box_end_y = box_start_y + config.RGB_BOX_HEIGHT

    box_start_x = box_padding

    # RED box
    red_box_start_x = box_start_x

    red_box_end_x = box_start_x + config.RGB_BOX_WIDTH
    cv2.rectangle(frame, (box_start_x, box_start_y),
                  (red_box_end_x, box_end_y), color=[0, 0, rgb_value[0]], thickness=2, lineType=cv2.LINE_AA)
    box_start_x = red_box_end_x + box_padding

    red_box_text = f"R: {rgb_value[0]}"
    drawTextBox(frame, red_box_text, (
                red_box_start_x, box_start_y - 30), 1, 2, [0, 0, 0])
    drawText(frame, red_box_text, (red_box_start_x,
             box_start_y - 30), [0, 0, 255], 1, 2)

    # GREEN box
    green_box_start_x = box_start_x

    green_box_end_x = box_start_x + config.RGB_BOX_WIDTH
    cv2.rectangle(frame, (box_start_x, box_start_y), (green_box_end_x,
                  box_end_y), color=[0, rgb_value[1], 0], thickness=2, lineType=cv2.LINE_AA)
    box_start_x = green_box_end_x + box_padding

    green_box_text = f"G: {rgb_value[1]}"
    drawTextBox(frame, green_box_text, (
                green_box_start_x, box_start_y - 30), 1, 2, [0, 0, 0])
    drawText(frame, green_box_text, (green_box_start_x,
             box_start_y - 30), [0, 255, 0], 1, 2)

    # BLUE box
    blue_box_start_x = box_start_x

    blue_box_end_x = box_start_x + config.RGB_BOX_WIDTH
    cv2.rectangle(frame, (box_start_x, box_start_y),
                  (blue_box_end_x, box_end_y), color=[rgb_value[2], 0, 0], thickness=2, lineType=cv2.LINE_AA)

    blue_box_text = f"B: {rgb_value[2]}"
    drawTextBox(frame, blue_box_text, (
                blue_box_start_x, box_start_y - 30), 1, 2, [0, 0, 0])
    drawText(frame, blue_box_text, (blue_box_start_x,
             box_start_y - 30), [255, 0, 0], 1, 2)

    return [
        [(red_box_start_x, box_start_y), (red_box_end_x, box_end_y)],
        [(green_box_start_x, box_start_y), (green_box_end_x, box_end_y)],
        [(blue_box_start_x, box_start_y), (blue_box_end_x, box_end_y)]
    ]


def fillBoxesWithFingerRGB(frame, rgb_box_points, finger_box_coordinates, rgb_values):
    red_box_pts, green_box_pts, blue_box_pts = rgb_box_points
    red_finger_pts, green_finger_pts, blue_finger_pts = finger_box_coordinates

    # fill RED part
    if red_finger_pts[0] > 0 and red_finger_pts[1] > 0:
        cv2.rectangle(frame, (red_box_pts[0][0], red_finger_pts[1]),
                      (red_box_pts[1][0], red_box_pts[1][1]), [0, 0, rgb_values[0]], thickness=cv2.FILLED)

    # fill GREEN part
    if green_finger_pts[0] > 0 and green_finger_pts[1] > 0:
        cv2.rectangle(frame, (green_box_pts[0][0], green_finger_pts[1]),
                      (green_box_pts[1][0], green_box_pts[1][1]), [0, rgb_values[1], 0], thickness=cv2.FILLED)

    # fill BLUE part
    if blue_finger_pts[0] > 0 and blue_finger_pts[1] > 0:
        cv2.rectangle(frame, (blue_box_pts[0][0], blue_finger_pts[1]),
                      (blue_box_pts[1][0], blue_box_pts[1][1]), [rgb_values[2], 0, 0], thickness=cv2.FILLED)
