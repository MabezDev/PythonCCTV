

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
        self.getBaseFrame()
        self.startWriter()
    def record(self):
        self.initFile()
        print self.newpath
        if not os.path.exists(self.newpath): os.makedirs(self.newpath)
        self.recording = True
        print "Recording... Press Ctr-C to stop"
        try:
            self.write()    
        except KeyboardInterrupt:
            print "Stopped Recording File Saved As: " + self.fileName
            self.cleanUp()
        
            
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

    def __init__(self):
        self.cam = Camera()
        self.totalPixels = 414720
        running = True
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        #add func to get avg background img using 1 single for now
        self.bgFrame = self.fgbg.apply(self.cam.getFrame())
        #self.baseNoChangedPixels = self.getAvgArraySum()
        #self.Threshold = self.baseNoChangedPixels+(0.1*self.baseNoChangedPixels)#1 percent difference increase is required
        #print self.Threshold
        try:
            while(running):
                frame = self.cam.getFrame()
                frame = cv2.blur(frame,(5,5))
                fgmask = self.fgbg.apply(frame)
                if(frame.sum()==0):
                    continue
            
                
                mask = cv2.absdiff(fgmask,self.bgFrame)
                #diffBase = diffArray.sum()/self.totalPixels
                #print diffArray.sum()/self.totalPixels
                gray =  self.to_grayscale(mask)
                ret,gray = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)

                #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
                #gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

                gray = cv2.blur(gray,(9,9))
                
                # Display the fgmask frame
                cv2.imshow('difference',gray)
                # Display original frame
                cv2.imshow('img', frame)

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
