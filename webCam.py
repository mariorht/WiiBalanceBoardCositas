from tkinter.constants import NONE
import cv2
import imutils
from PIL import Image
from PIL import ImageTk


class webCam:
    def __init__(self):
        self.cap = NONE

    def __del__(self):
        if(self.cap != NONE):
            self.cap.release()

    def initCamera(self):
        self.cap = cv2.VideoCapture(0)


    def getFrame(self):
        if(self.cap == NONE):
            print("NO HAY CAMARA")
            return

        ret, frame = self.cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            return ImageTk.PhotoImage(image=im)
        else:
            print("Error leyendo frame")
            self.cap.release()
