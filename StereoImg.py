import cv2
class Stereo:
    def __init__ (self, minDisparity, maxDisparity,blockSize,windowSize, preFilterCap, disp12MaxDiff,uniquenessRatio,speckleWindowSize,speckleRange, mode):
        self.minDisparity = minDisparity * 16
        self.maxDisparity = maxDisparity * 16
        self.blockSize = blockSize
        self.windowSize = windowSize
        self.disp12MaxDiff = disp12MaxDiff
        self.uniquenessRatio = uniquenessRatio
        self.speckleWindowSize = speckleWindowSize
        self.speckleRange = speckleRange
        self.numDisparity = maxDisparity - minDisparity
        self.preFilterCap = preFilterCap
        self.mode = mode
        self.stereo = cv2.StereoSGBM_create(minDisparity = self.minDisparity,
        numDisparities = self.numDisparity,
        blockSize = self.blockSize,
        P1 = 8*1*self.windowSize**2,
        P2 = 32*1*self.windowSize**2,
        preFilterCap = self.preFilterCap,
        disp12MaxDiff = self.disp12MaxDiff,
        uniquenessRatio = self.uniquenessRatio,
        speckleWindowSize = self.speckleWindowSize,
        speckleRange = self.speckleRange,
        mode = self.mode
        )

    def updateMinDisparity (self,value) :
        #must be smaller than maxDisp and multiple of 16
        #if (self.maxDisparity > (int(value) * 16)):
        self.minDisparity = int(value) * 16
        #self.minDisparity = int(value) * 16
        #self.numDisparity = self.maxDisparity - self.minDisparity
        self.updateSGBM()
    def updateMaxDisparity (self,value) :
        #must be multiple of 16
        self.maxDisparity = int(value) * 16
        #self.numDisparity = self.maxDisparity - self.minDisparity
        self.updateSGBM()
    def updateBlockSize(self,value) :
        #must be odd
        value_received = int(value)
        if value_received % 2 == 0:
            value_received = value_received + 1
        self.blockSize = value_received
        self.updateSGBM()
    def updateWindowSize(self,value) :
        self.windowSize = int(value)
        self.updateSGBM()
    def updateDisp12MaxDiff(self,value) :
        self.disp12MaxDiff = int(value)
        self.updateSGBM()
    def updateUniquenessRatio(self,value) :
        self.uniquenessRatio = int(value)
        self.updateSGBM()
    def updateSpeckleWindowSize(self,value) :
        self.speckleWindowSize = int(value)
        self.updateSGBM()
    def updateSpeckleRange(self,value) :
        self.speckleRange = int(value)
        self.updateSGBM()
    def updatePreFilterCap(self,value) :
        self.preFilterCap = int(value)
        self.updateSGBM()
    def updateMode(self, value) :
        #must be boolean
        if int(value) == 0:
            self.mode = False
        else: 
            self.mode = True
        self.updateSGBM()       


    def updateSGBM (self):
        self.stereo = cv2.StereoSGBM_create(minDisparity = self.minDisparity,
        numDisparities = self.numDisparity,
        blockSize = self.blockSize,
        P1 = 8*1*self.windowSize**2,
        P2 = 32*1*self.windowSize**2,
        preFilterCap = self.preFilterCap,
        disp12MaxDiff = self.disp12MaxDiff,
        uniquenessRatio = self.uniquenessRatio,
        speckleWindowSize = self.speckleWindowSize,
        speckleRange = self.speckleRange,
        mode = self.mode
        )

    def getSGBM(self):
        return self.stereo