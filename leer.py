#!/usr/bin/env python
import tkinter as tk
from tkinter.constants import COMMAND
from datetime import datetime
import numpy as np
from videoPlayer import videoPlayer

windowWidth, windowHeight = 1400, 1000
canvasWidth, canvasHeight = 800, windowHeight
rectW, rectH = 250, 150
imageW, imageH, offsetX = 285, 900, 5
CIRCLE_RADIUS = 6
FPS = 30 # se sobbreescribirá al valor que de la webcam para mantener un solo hilo
N_CIRCLES = 15


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        #video
        self.videoPlayer = videoPlayer()

        # WiiBoard


        # Tk
        self.master = master
        self.pack()

        self.create_widgets()



    def create_widgets(self):
        self.createCanvas()
        self.createButtons()
        self.createVideo()




    def createButtons(self):
        self.buttonsFrame = tk.Frame(self.master)
        self.buttonsFrame.place(x=50, y = 50)

        self.openVideoButton = tk.Button(self.buttonsFrame, text = "Open",  command = self.openVideo, width=15)
        self.openVideoButton.pack(pady=5)


    def createVideo(self):
        self.videoFrame = tk.Frame(self.master)
        self.videoFrame.place(anchor=tk.NE, relx = 0.95, rely = 0.15)
        self.labelVideo = tk.Label(self.videoFrame)
        self.labelVideo.pack()
        

    def createCanvas(self):
        self.canvas = tk.Canvas(self.master, width=canvasWidth, height=canvasHeight)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # self.rectangle = self.canvas.create_rectangle(windowWidth/2-rectW/2, windowHeight/2-rectH/2, windowWidth/2+rectW/2, windowHeight/2+rectH/2)

        self.tabla = tk.PhotoImage(file='images/tabla.png')
        self.canvas.create_image(canvasWidth/2+offsetX, canvasHeight/2,anchor=tk.CENTER, image=self.tabla)

        self.COG_list = []
        self.lastCOG = 0
        for i in range(N_CIRCLES):
            self.COG_list.append(self.canvas.create_circle(canvasWidth/2, canvasHeight/2, CIRCLE_RADIUS, fill='blue', width = 0))




    def get_COG_position(self):
        pos = self.canvas.coords(self.COG)
        return pos[0]+CIRCLE_RADIUS, pos[1]+CIRCLE_RADIUS

    def set_COG_postion(self, x, y):
        self.canvas.moveto(self.COG_list[self.lastCOG], x - CIRCLE_RADIUS -1, y - CIRCLE_RADIUS - 1)
        self.lastCOG += 1
        if self.lastCOG >= N_CIRCLES:
            self.lastCOG = 0


    def update_COG_position(self, x, y):
        self.set_COG_postion(x, y)




    def updateCamera(self):
        img = self.cam.getFrame()
        self.labelVideo.configure(image=img)
        self.labelVideo.image = img


    def openVideo(self):
        self.videoPlayer.openVideo("savings/2021-08-01 17:59:37.579707.avi")
        print(self.videoPlayer.getTotalFrames())






root = tk.Tk(className=' A surfear con la wiiBoard')
app = Application(master=root)
app.master.geometry("{}x{}".format(windowWidth, windowHeight))
app.mainloop()

