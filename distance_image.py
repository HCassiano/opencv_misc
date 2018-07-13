# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
import urllib.request as urllib

def apply_denoising(img):
	# create a list of first 5 frames
	#img = [cap.read()[1] for i in xrange(5)]
	# convert all to grayscale
	gray = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in img]
	# convert all to float64
	#gray = [np.float64(i) for i in gray]
	# create a noise of variance 25
	#noise = np.random.randn(*gray[1].shape)*10
	# Add this noise to images
	#noisy = [i+noise for i in gray]
	# Convert back to uint8
	#noisy = [np.uint8(np.clip(i,0,255)) for i in noisy]
	# Denoise 3rd frame considering all the 5 frames
	dst = cv2.fastNlMeansDenoisingMulti(gray, 1, 3, None, 4, 7, 35)
	return dst

def get_smart_camera():
    url='http://192.168.43.1:8080/shot.jpg'
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    return img

def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = image
	#gray = cv2.GaussianBlur(gray, (5, 5), 0)
	#gray = cv2.fastNlMeansDenoising(gray,3,7,21)
	edged = cv2.Canny(gray, 35, 125)
	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	c = max(cnts, key = cv2.contourArea)
 
	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 30 centimeters
KNOWN_DISTANCE = 30.0
 
# initialize the known object width, which in this case, the piece of
# paper is 27 centimeters wide
KNOWN_WIDTH = 27.0
 
# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = get_smart_camera()
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH	
img = []
# loop over the images
while True:
	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera
	x = 0
	while x < 3:
		image = get_smart_camera()
		image = cv2.GaussianBlur(image, (5, 5), 0)
		img.append(image)
		x = x + 1
	x = 0
	image = apply_denoising(img)
	img = []
	marker = find_marker(image)
	centimeters = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
 
	# draw a bounding box around the image and display it
	box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
	box = np.int0(box)
	cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	cv2.putText(image, "%.2fcm" % centimeters , (image.shape[1] - 200, image.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)
	cv2.imshow("image", image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()