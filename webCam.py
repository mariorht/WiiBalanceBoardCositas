from tkinter.constants import NONE
import cv2
import imutils
from PIL import Image
from PIL import ImageTk


class webCam:
    def __init__(self, fps):
        # print(cv2.getBuildInformation())
        self.cap = NONE
        self.writer = NONE
        self.fps = fps


    def __del__(self):
        if(self.cap != NONE):
            self.cap.release()

    def initCamera(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)


    def getFrame(self):
        if(self.cap == NONE):
            print("NO HAY CAMARA")
            return

        ret, frame = self.cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640, height = 480)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if(self.writer != NONE):
                self.writer.write(frame)

            im = Image.fromarray(frame)
            return ImageTk.PhotoImage(image=im)
        else:
            print("Error leyendo frame")
            self.cap.release()



    def startSavingVideo(self, path):
        print(path)
        fourcc = fourcc= cv2.VideoWriter_fourcc('M','J', 'P', 'G')

        self.writer = cv2.VideoWriter('path', fourcc, self.fps, (640,480))

    def stopSavingVideo(self):
        self.writer.release()
        self.writer = NONE
