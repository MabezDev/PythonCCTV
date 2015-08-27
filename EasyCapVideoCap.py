

from VideoCapture import Device
import time
import os
import cv2
import numpy
from scipy import sum, average
from scipy.linalg import norm

class Camera:

    def __init__(self):
        self.winName = "Dad CCTV"
        self.recording = False
        self.fps = 24
        device = int(raw_input("Choose System Device: "))
        self.cam = Device(devnum=device)

    def initFile(self):
        self.newpath = time.strftime("%d.%m.%y"+"\\") 
        self.fileName = time.strftime("%H.%M.%S")
        if not os.path.exists(self.newpath): os.makedirs(self.newpath)
        self.getBaseFrame()
        self.startWriter()
    def record(self):
        self.initFile()
        self.recording = True
        print "Recording... Press Ctr-C to stop"
        try:
            self.write()    
        except KeyboardInterrupt:
            print "Stopped Recording File Saved As: " + self.fileName
            self.cleanUp()

    def setRecording(self,decider):
        self.recording = decider
        
            
    def getCurrentTime(self):
        time = time.strftime("%H:%M:%S")

    def getBaseFrame(self):
        self.cam.saveSnapshot("1.jpg")

    def getFrame(self):
         return numpy.array(self.cam.getImage())

    def getPILFrame(self):
        return self.cam.getImage()

    def startWriter(self):
        img = cv2.imread("1.jpg")
        height,width,layers = img.shape
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        self.videoWriter = cv2.VideoWriter(self.newpath+self.fileName+".avi",fourcc,self.fps,(width,height))

    def record5Seconds(self):
        recording =True
        self.initFile()
        now = time.time()
        future = now + 5
        while time.time() < future:
            self.write()
        else:
            self.cleanUp()
            
    def write(self):
        self.videoWriter.write(self.getFrame())

    def cleanUp(self):
        recording = False
        self.videoWriter.release()

    def isRecording(self):
        return self.recording


class MotionDetect():

    def __init__(self):##this seem very promising need to work on recording and keep readin the difference
        self.cam = Camera()
        self.totalPixels = 414720
        running = True
        self.old = self.cam.getPILFrame()
        try:
            while(running):
                frame = self.cam.getPILFrame()
                self.percentDifference = self.rossetaPerDiff(frame,self.old)
                self.old = frame
                if(self.percentDifference>8):
                    if(self.cam.isRecording()):
                        self.cam.write()
                    else:
                        self.cam.initFile()
                        self.cam.write()
                else:
                    if(self.cam.isRecording()):
                        self.cam.cleanUp()
                # Display original frame
                cv2.imshow('img', numpy.array(frame))

                if  cv2.waitKey ( 1 ) & 0xFF  ==  ord ( 'q' ):
                    cv2.destroyAllWindows()
                    self.cam.cleanUp()
                    


        except KeyboardInterrupt:
            running=False
            self.cam.cleanUp()
            cv2.destroyAllWindows()

    def to_grayscale(self,arr):
        if len(arr.shape) == 3:
            return average(arr, -1)  # average over the last axis (color channels)
        else:
            return arr

    def getAvgArraySum(self):
        diffBase = 0
        for x in range(20):
            frame = self.cam.getFrame()
            fgmask = self.fgbg.apply(frame)
            diffArray = cv2.absdiff(fgmask,self.bgFrame)
            diffBase +=diffArray.sum()/self.totalPixels
        return diffBase/20
    def rossetaPerDiff(self,img1,img2):
        from itertools import izip
        import Image
         
        i1 = img1
        i2 = img2
        assert i1.mode == i2.mode, "Different kinds of images."
        assert i1.size == i2.size, "Different sizes."
         
        pairs = izip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            # for gray-scale jpegs
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
         
        ncomponents = i1.size[0] * i1.size[1] * 3
        print "Difference (percentage):", (dif / 255.0 * 100) / ncomponents
        return (dif / 255.0 * 100) / ncomponents
        



def Menu():
    print "1) Initialize Camera"
    print "2) Start Recording to Disk"
    print "3) Start Motion Detection Recording"
    print "4) Exit"
    choice  = int(raw_input(""))
    if(choice==2):
        camera = Camera()
        camera.record()
    if(choice==3):
        motion = MotionDetect()
    if(choice==4):
        exit()
    
while(True):
    Menu()
