import cv2
import imutils
from PIL import Image
from PIL import ImageTk


class videoPlayer:
    def __init__(self):
        self.cap = None
        self.fps = None

    def openVideo(self, path):
        print(path)
        self.cap = cv2.VideoCapture(path)
        if (self.cap.isOpened()== False):
            print("Error opening video stream or file")


    def getTotalFrames(self):
        if self.cap != None:
            return self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        else:
            print("No hay un archivo de video abierto")
            return 0


