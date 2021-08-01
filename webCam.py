from tkinter.constants import NONE
import cv2
import imutils
from PIL import Image
from PIL import ImageTk

aaa = 0
class webCam:
    def __init__(self):
        # print(cv2.getBuildInformation())
        self.cap = NONE
        self.writer = NONE
        self.fps = NONE
        self.saving = False

    def __del__(self):
        if(self.cap != NONE):
            self.cap.release()

    def initCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.fps = self.getFPS()
        
    def getFPS(self):
        return 25; #Limitado a 25FPS
        #self.cap.get(cv2.CAP_PROP_FPS)

    def getFrame(self):
        if(self.cap == NONE):
            print("NO HAY CAMARA")
            return

        ret, frame = self.cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640, height = 480)

            if(self.saving):
                self.writer.write(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            return ImageTk.PhotoImage(image=im)
        else:
            print("Error leyendo frame")
            self.cap.release()



    def startSavingVideo(self, path):
        fourcc = fourcc= cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter(path, fourcc, self.fps, (640,480))
        self.saving = True

    def stopSavingVideo(self):
        self.saving = False
        self.writer.release()
        self.writer = NONE
