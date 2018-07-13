import numpy as np
import cv2
import time
import tkinter as tk
import StereoImg
#feed2,cap2 = L
#feed1,cap1 = R
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
stereo = cv2.StereoBM_create(numDisparities = 128, blockSize = 5)
#stereo = StereoImg.Stereo(16,6 * 16,16,3,61,1,10,100,32,False)
'''
window_size = 3
min_disp = 16
num_disp = 112-min_disp
stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
    numDisparities = num_disp,
    blockSize = 16,
    P1 = 8*1*window_size**2,
    P2 = 32*1*window_size**2,
    disp12MaxDiff = 1,
    uniquenessRatio = 10,
    speckleWindowSize = 100,
    speckleRange = 32
    )
'''
'''
#create sliders
master_ui = tk.Tk()
#minDisparity
w1 = tk.Scale(master_ui, from_=0, to=100, length = 350,  label = 'minDisparity', orient=tk.HORIZONTAL, command=stereo.updateMinDisparity)
w1.pack()
#maxDisparity
w2 = tk.Scale(master_ui, from_=0, to=1000, length = 350, label = 'maxDisparity', orient=tk.HORIZONTAL, command=stereo.updateMaxDisparity)
w2.pack()
#blockSize
w3 = tk.Scale(master_ui, from_=0, to=100, length = 350,  label = 'blockSize', orient=tk.HORIZONTAL, command=stereo.updateBlockSize)
w3.pack()
#windowSize
w4 = tk.Scale(master_ui, from_=0, to=10, length = 350,  label = 'windowSize', orient=tk.HORIZONTAL, command=stereo.updateWindowSize)
w4.pack()
#disp12MaxDiff
w5 = tk.Scale(master_ui, from_=0, to=100, length = 350,  label = 'disp12MaxDiff', orient=tk.HORIZONTAL, command=stereo.updateDisp12MaxDiff)
w5.pack()
#uniquenessRatio
w6 = tk.Scale(master_ui, from_=0, to=10, length = 350,  label = 'uniquenessRatio', orient=tk.HORIZONTAL, command=stereo.updateUniquenessRatio)
w6.pack()
#speckleWindowSize
w7 = tk.Scale(master_ui, from_=0, to=100, length = 350,  label = 'speckleWindowSize', orient=tk.HORIZONTAL, command=stereo.updateSpeckleWindowSize)
w7.pack()
#speckleRange
w8 = tk.Scale(master_ui, from_=0, to=1000, length = 350, label = 'speckleRange', orient=tk.HORIZONTAL, command=stereo.updateSpeckleRange)
w8.pack()
#preFilterCap
w9 = tk.Scale(master_ui, from_=0, to=1000, length = 350, label = 'preFilterCap', orient=tk.HORIZONTAL, command=stereo.updatePreFilterCap)
w9.pack()
#mode
w10 = tk.Scale(master_ui, from_=0, to=1, length = 350,  label = 'mode', orient=tk.HORIZONTAL, command=stereo.updateMode)
w10.pack()
'''
while True:
	ret, frame1 = cap1.read()
	ret, frame2 = cap2.read()
	frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
	disparity = stereo.compute(frame1,frame2)
	#disparity = stereo.getSGBM().compute(frame1,frame2)
	disparity = np.uint8(disparity)
	im_color = cv2.applyColorMap(disparity, cv2.COLORMAP_BONE)
	cv2.imshow("disparity",im_color)
	#master_ui.update()
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap1.release()
cap2.release()
cv2.destroyAllWindows()