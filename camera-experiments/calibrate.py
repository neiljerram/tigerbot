# import the necessary packages
import argparse
import imutils
import cv2
import numpy as np
import math
import yaml

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# Load the image and convert it to HSV.
image = cv2.imread(args["image"])
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Load config.
with open('/cfg/calibrate.yaml', 'r') as f:
    config = yaml.load(f)['balls']

def hue_mask(hsv, h_lo, h_hi, s_lo, s_hi, v_lo, v_hi):
    return cv2.inRange(hsv,
                       np.array([h_lo, s_lo, v_lo]),
                       np.array([h_hi, s_hi, v_hi]))

def hsv_mask(hsv, h_lo, h_hi, s_lo, s_hi, v_lo, v_hi):
    if h_hi > h_lo:
        return hue_mask(hsv, h_lo, h_hi, s_lo, s_hi, v_lo, v_hi)
    else:
        mask1 = hue_mask(hsv, h_lo, 180, s_lo, s_hi, v_lo, v_hi)
        mask2 = hue_mask(hsv, 0, h_hi, s_lo, s_hi, v_lo, v_hi)
        return cv2.bitwise_or(mask1, mask2)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print x, y, hsv[y,x]

def find_ball2(config, colour):
    print "Looking for %r" % colour
    h_lo = config[colour]['huemin']
    h_hi = config[colour]['huemax']
    s_lo = config[colour]['satmin']
    s_hi = config[colour]['satmax']
    v_lo = config[colour]['valmin']
    v_hi = config[colour]['valmax']

    mask = hsv_mask(hsv, h_lo, h_hi, s_lo, s_hi, v_lo, v_hi)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
	# find the largest contour in the mask, then use
	# it to compute the minimum enclosing circle and
	# centroid
	c = max(cnts, key=cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

	# only proceed if the radius meets a minimum size
	if radius > 10:
	    # draw the circle and centroid on the frame,
	    # then update the list of tracked points
	    cv2.circle(image, (int(x), int(y)), int(radius),
		       (0, 255, 255), 2)
	    cv2.circle(image, center, 5, (0, 0, 255), -1)

def show_result():
    desc = args["image"]
    cv2.imshow(desc, image)
    cv2.setMouseCallback(desc, mouse_callback)
    while True:
        code = cv2.waitKey(0)
        print "Key pressed: %r" % code
        if code == 110:
            break

print "Image shape = %r" % [image.shape]
print "HSV shape = %r" % [hsv.shape]

find_ball2(config, "yellow")
find_ball2(config, "green")
find_ball2(config, "blue")
find_ball2(config, "red")
show_result()
