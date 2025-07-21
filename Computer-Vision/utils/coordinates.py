import config


def getFingerInBoxRgbCoordinates(finger_points, rgb_box_points):
    red_box, green_box, blue_box = rgb_box_points
    finger_x, finger_y = finger_points

    if (finger_x >= red_box[0][0] and finger_y >= red_box[0][1]) and (finger_x <= red_box[1][0] and finger_y <= red_box[1][1]):
        # in RED box
        return [0, finger_points]
    elif (finger_x >= green_box[0][0] and finger_y >= green_box[0][1]) and (finger_x <= green_box[1][0] and finger_y <= green_box[1][1]):
        # in GREEN box
        return [1, finger_points]
    elif (finger_x >= blue_box[0][0] and finger_y >= blue_box[0][1]) and (finger_x <= blue_box[1][0] and finger_y <= blue_box[1][1]):
        # in BLUE box
        return [2, finger_points]

    return [3, (0, 0)]


def getValueRGB(finger_points, rgb_box_points):
    red_value = 0
    green_value = 0
    blue_value = 0

    # RED
    if finger_points[0][1]:
        red_end_y = rgb_box_points[0][1][1]

        red_filled_height = red_end_y - finger_points[0][1]
        red_value = int(red_filled_height / config.RGB_BOX_HEIGHT * 255)

    # GREEN
    if finger_points[1][1] > 0:
        green_end_y = rgb_box_points[1][1][1]

        green_filled_height = green_end_y - finger_points[1][1]
        green_value = int(green_filled_height / config.RGB_BOX_HEIGHT * 255)

    # BLUE
    if finger_points[2][1] > 0:
        blue_end_y = rgb_box_points[2][1][1]

        blue_filled_height = blue_end_y - finger_points[2][1]
        blue_value = int(blue_filled_height / config.RGB_BOX_HEIGHT * 255)

    return [red_value, green_value, blue_value]
