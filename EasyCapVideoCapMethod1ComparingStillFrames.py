

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
        self.fps = 12
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
        self.previous = self.cam.getFrame()#get initial frame 
        self.Threshold = self.getBaseAvgPixelDifference()
        print self.Threshold 
        running = True
        try:
            while(running):
                frame = self.cam.getFrame()
                grayScaled_P = self.to_grayscale(self.previous)
                grayScaled_C = self.to_grayscale(frame)
                n_m, n_0 = self.compare_images(grayScaled_P, grayScaled_C)
                Difference = ((self.totalPixels/n_m)*100)
                print "Difference: "+str(Difference)+" %"
                if(Difference>self.Threshold):##6 is genreic need a func to work out based on the first few results with no movement(calibration)
                    self.cam.record5Seconds()
                    
                

        except KeyboardInterrupt:
            running=False
            self.cam.cleanUp()

    def to_grayscale(self,arr):
        if len(arr.shape) == 3:
            return average(arr, -1)  # average over the last axis (color channels)
        else:
            return arr
    def getBaseAvgPixelDifference(self):
        avg = 0
        for x in range(100):
            frame = self.cam.getFrame()
            grayScaled_P = self.to_grayscale(self.previous)
            grayScaled_C = self.to_grayscale(frame)
            n_m, n_0 = self.compare_images(grayScaled_P, grayScaled_C)
            avg +=(n_m)
        Difference = ((self.totalPixels/(avg/100))*100)

        return Difference

    def normalize(self,arr):
        rng = arr.max()-arr.min()
        amin = arr.min()
        return (arr-amin)*255/rng
            
            

    def compare_images(self,img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
        #img1 = self.normalize(img1)
        #img2 = self.normalize(img2)
    # calculate the difference and its norms
        diff = img1 - img2  # elementwise for scipy arrays
        m_norm = sum(abs(diff))  # Manhattan norm
        z_norm = norm(diff.ravel(), 0)  # Zero norm
        return (m_norm, z_norm)
            
        



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
