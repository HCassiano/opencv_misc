import numpy as np
import cv2 as cv
#from matplotlib import pyplot as plt
imgL = cv.imread('imgL3.jpg',0)
imgR = cv.imread('imgR3.jpg',0)
#stereo = cv.StereoBM_create(numDisparities=384, blockSize=5)
#disparity = stereo.compute(imgL,imgR)
cv.namedWindow('image',cv.WINDOW_NORMAL)
cv.resizeWindow('image', 600,600)
#cv.namedWindow('ref',cv.WINDOW_NORMAL)
#cv.resizeWindow('ref', 600,600)
flag_break = False
while True:
	x = 1
	while x < 100:
		stereo = cv.StereoBM_create(numDisparities=(x * 16), blockSize=5)
		disparity = stereo.compute(imgL,imgR)
		#cv.putText(disparity, "%.2f" % (x * 16),
        #(disparity.shape[1] - 500, disparity.shape[0] - 50), cv.FONT_HERSHEY_SIMPLEX,
        #20.0, (0, 255, 0), 10)
		#print (disparity.shape[0])
		#print (disparity.shape[1])
		cv.imshow('image', disparity)
		#cv.imshow('ref',imgL)
		#time.sleep(1)
		#cv.destroyAllWindows()
		x = x + 1
		if cv.waitKey(200) & 0xFF == ord('q'):
			flag_break = True
			break
	x = 1
	if flag_break:
		break
cv.destroyAllWindows()
#plt.imshow(disparity,'gray')
#plt.showq