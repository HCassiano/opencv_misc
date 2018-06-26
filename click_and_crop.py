# import the necessary packages
import cv2
import numpy as np
from imutils import paths
import imutils
 
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
drawRectangleFlag = False
KNOWN_DISTANCE= 30.0
KNOWN_WIDTH = 23.0

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
 
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    c = max(cnts, key = cv2.contourArea)
    # compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(c) 

def click_and_crop(event, x, y, flags, params):
    # grab references to the global variables
    global refPt, cropping, drawRectangleFlag
 
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        drawRectangleFlag = True
 
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        drawRectangleFlag = False
        # DEBUG: check edge detection results
        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)
        cv2.imshow("DEBUG", edged)
    
    # constant drawing in interface during drag-box
    elif event == cv2.EVENT_MOUSEMOVE:
        if refPt != [] and (refPt[0][0] < x) and (refPt[0][1] < y):
            drawTuple = (x,y)
            cv2.rectangle(frame, refPt[0], drawTuple, (0, 255, 0), 2)            
            cv2.imshow("feed", frame)

def draw_distance(image,marker,distance_centimeters):
    box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
    box = np.int0(box)
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.putText(image, "%.2fcm" % (distance_centimeters),
        (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
        2.0, (0, 255, 0), 3)
    #cv2.imshow("image", image)

cap = cv2.VideoCapture(0)
cv2.namedWindow("feed")
cv2.setMouseCallback("feed", click_and_crop)
focalLength = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    clone = frame.copy()
    # Display the resulting frame
    if not drawRectangleFlag and focalLength == 0:    
        cv2.imshow("feed",frame)
    #print refPt
    if len(refPt) == 2 and (refPt[0][1] < refPt[1][1]) and (refPt[0][0] < refPt[1][0]):
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        marker = find_marker(roi)
        focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
        print focalLength
        cv2.imshow("ROI", roi)
        #clear refPt after draw
        refPt = []
    if focalLength != 0:
        marker = find_marker(frame)
        distance_centimeters = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        draw_distance (frame, marker, distance_centimeters)
        cv2.imshow("feed",frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
