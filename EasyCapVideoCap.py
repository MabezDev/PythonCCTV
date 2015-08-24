

from VideoCapture import Device
import time
import os
import cv2
import numpy

#w = cv2.cvCreateVideoWriter("Vidja.avi", -1 ,)

class Camera:

    def __init__(self):
        self.winName = "Dad CCTV"
        self.fps = 12
        device = int(raw_input("Choose System Device: "))
        self.cam = Device(devnum=device)
        self.newpath = time.strftime("%d.%m.%y"+"\\") 
        self.fileName = time.strftime("%H.%M.%S")
        print self.newpath
        if not os.path.exists(self.newpath): os.makedirs(self.newpath)
        self.getBaseFrame()
        self.startWriter()
        recording = True
        print "Recording... Press Ctr-C to stop"
        try:
            while(recording):
                self.write()
                
        except KeyboardInterrupt:
            self.cleanUp()
            
    def getCurrentTime(self):
        time = time.strftime("%H:%M:%S")

    def getBaseFrame(self):
        self.cam.saveSnapshot("1.jpg")

    def getFrame(self):
         return numpy.array(self.cam.getImage())

    def startWriter(self):
        img = cv2.imread("1.jpg")
        height,width,layers = img.shape
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        self.videoWriter = cv2.VideoWriter(self.newpath+self.fileName+".avi",fourcc,self.fps,(width,height))
    

    def write(self):
        self.videoWriter.write(self.getFrame())

    def cleanUp(self):
        recording = False
        self.videoWriter.release()
        print "Stopped Recording File Saved As: " + self.fileName
        



def Menu():
    print "1) Initialize Camera"
    print "2) Start Recording to Disk"
    print "3) Start Motion Detection Recording"
    print "4) Exit"
    choice  = int(raw_input(""))
    if(choice==1):
        camera = Camera()
    if(choice==4):
        exit()
    
while(True):
    Menu()
