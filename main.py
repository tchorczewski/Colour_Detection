# @Author Bartosz Tchorowski

import numpy as num
import cv2 as cv


# def mouse_callback(event, x, y, flags, param):
#    if event == cv.EVENT_LBUTTONDBLCLK: # sprawdzic eventy, któty jest wysyłany i dlaczego nie ten co chcesz
#        mouse_X = frame[x]
#        mouse_Y = frame[y]
#        [b, g, r] = frame[mouse_X, mouse_Y, 2]
#        hsv_colour = cv.cvtColor((b, g, r), cv.COLOR_BGR2HSV)
#        cv.putText(frame, hsv_colour, (10, 500), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv.LINE_AA)
#       return hsv_colour


# detection methods
def detect_from_square(colour_mask, colour_bgr, used_frame):
    detected_contour, hierarchy = cv.findContours(colour_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(detected_contour):  # Loop using i and contour to count the loops and give value of the
        # current iteration
        area = cv.contourArea(contour)  # Measuring the area of detected contour
        # If the area is smaller than 300 px then object will not be counted/detected- used to reduce noise detection
        if area < 100:
            continue
        (h, v, l, he) = cv.boundingRect(contour)
        # drawing rectangle around the position
        cv.rectangle(used_frame, (h, v,), (h + l, v + he), colour_bgr, 2)
        # storing object data  in lists
        length.append(l)
        horizontal.append(h + (l / 2))
        vertical.append(v + (he / 2))
        height.append(he)


def red():
    # Red colour range
    red_lower = num.array([160, 50, 50], num.uint8)
    red_higher = num.array([180, 255, 255], num.uint8)
    red_mask = cv.inRange(hsv_frame, red_lower, red_higher)
    return red_mask


def green():
    # Green colour range
    green_lower = num.array([70, 100, 120], num.uint8)
    green_higher = num.array([102, 255, 255], num.uint8)
    green_mask = cv.inRange(hsv_frame, green_lower, green_higher)
    return green_mask


def blue():
    # Blue colour range
    blue_lower = num.array([110, 70, 70], num.uint8)
    blue_higher = num.array([130, 255, 255], num.uint8)
    blue_mask = cv.inRange(hsv_frame, blue_lower, blue_higher)
    return blue_mask


def yellow():
    # Yellow colour range
    yellow_lower = num.array([20, 100, 100])
    yellow_higher = num.array([30, 255, 255])
    yellow_mask = cv.inRange(hsv_frame, yellow_lower, yellow_higher)
    return yellow_mask


def violet():
    violet_lower = num.array([140, 70, 70])
    violet_higher = num.array([150, 255, 255])
    violet_mask = cv.inRange(hsv_frame, violet_lower, violet_higher)
    return violet_mask


min_width = 1420
min_height = 480
reference_frame = None
kernal = num.ones((1, 1), num.uint8) # Kernal sized one works the best in this situation
# opening the camera
camera = cv.VideoCapture(0)  # 0 is default id for built-in webcam

# checking if the camera is opened successfully
if not (camera.isOpened()):
    print("Could not open device")
# setting the resolution
camera.set(3, min_width)
camera.set(4, min_height)
# Setting the colours for rectangle drawing
green_bgr = (0, 255, 0)
red_bgr = (0, 0, 255)
blue_bgr = (255, 0, 0)
yellow_bgr = (0, 255, 255)
violet_rgb = (255, 0, 127)
# Camera needs some time to automatically adjust, so we are going  to skip first frames
for i in range(0, 20):
    (grabbed, Frame) = camera.read()
name = 'Processed image'
name1 = 'Detection done on hsv colour palette'
name2 = 'Detection done on greyscale image'
cv.namedWindow(name)
# object detection, when camera is opened
while camera.isOpened():
    horizontal = []
    vertical = []
    length = []
    height = []
    (grabbed, frame) = camera.read()
    # To reduce the noise each frame is being eroded, dilated and morphed
    frame = cv.dilate(frame, kernal)
    frame = cv.erode(frame, kernal)
    # converting into greyscale to make object detection possible
    grey_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # simple if to check is frame was grabbed
    if not grabbed:
        break
    # turning frame into hsv, because it offers better colour description than RGB
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    detect_from_square(green(), green_bgr, frame)
    detect_from_square(red(), red_bgr, frame)
    detect_from_square(blue(), blue_bgr, frame)
    detect_from_square(yellow(), yellow_bgr, frame)
    detect_from_square(violet(), violet_rgb, frame)

    cv.imshow(name, frame)

    detect_from_square(green(), green_bgr, hsv_frame)
    detect_from_square(red(), red_bgr, hsv_frame)
    detect_from_square(blue(), blue_bgr, hsv_frame)
    detect_from_square(yellow(), yellow_bgr, hsv_frame)
    detect_from_square(violet(), violet_rgb, hsv_frame)

    cv.imshow(name1, hsv_frame)

    detect_from_square(green(), green_bgr, grey_frame)
    detect_from_square(red(), red_bgr, grey_frame)
    detect_from_square(blue(), blue_bgr, grey_frame)
    detect_from_square(yellow(), yellow_bgr, grey_frame)
    detect_from_square(violet(), violet_rgb, grey_frame)

    cv.imshow(name2, grey_frame)

    if cv.waitKey(10) & 0xFF == ord('q'):
        camera.release()
        cv.destroyAllWindows()
        break

    #elif cv.waitKey(10) == ord('a'):
    #   cv.setMouseCallback(name, mouse_callback)
