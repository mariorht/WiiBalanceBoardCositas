#!/usr/bin/env python
import tkinter as tk
from tkinter.constants import COMMAND
from wiiBoard import wiiBoard
from webCam import webCam
from datetime import datetime
import numpy as np

windowWidth, windowHeight = 1400, 1000
canvasWidth, canvasHeight = 800, windowHeight
rectW, rectH = 250, 150
imageW, imageH, offsetX = 285, 900, 5
CIRCLE_RADIUS = 6
FPS = 50 # se sobbreescribirá al valor que de la webcam para mantener un solo hilo
N_CIRCLES = 25


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        #chapuza para que la wiiborad vaya al doble de FPS que la cámara
        self.flag = True 
        
        #webcam
        self.cam = webCam()
        self.cam.initCamera()
        FPS = self.cam.getFPS()
        print("FPS: ", FPS)

        # WiiBoard
        self.wiiB = wiiBoard()
        self.wiiB.connect()
        self.wiiB.print_info()
        self.wiiB.calibrar()

        # Tk
        self.master = master
        self.pack()

        self.create_widgets()
        self.startWiiBoardLoop()
        self.startWiiBoardBatteryPolling()


    def create_widgets(self):
        self.createCanvas()
        self.createButtons()
        self.createVideo()




    def createButtons(self):
        self.buttonsFrame = tk.Frame(self.master)
        self.buttonsFrame.place(x=50, y = 50)

        self.calibrateButton = tk.Button(self.buttonsFrame, text = "Calibrar",  command = self.wiiB.calibrar, width=15)
        self.calibrateButton.pack(pady=5)

        self.saving = False
        self.recButton = tk.Button(self.buttonsFrame, text = "Start saving",  command = self.startSave, width=15)
        self.recButton.pack(pady=5)


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

        self.canvas.create_line(-(imageW/2 - 15) + canvasWidth/2, canvasHeight/2, imageW/2 - 15 + canvasWidth/2, canvasHeight/2, fill="#b3ad9b", width=3)

        self.COG_list = []
        self.lastCOG = 0
        for i in range(N_CIRCLES):
            self.COG_list.append(self.canvas.create_circle(canvasWidth/2, canvasHeight/2, CIRCLE_RADIUS, fill='blue', width = 0))

        lbl_font = ("Sans sheriff", 18, "bold")
        self.wiiBoard_battery_Label = self.canvas.create_text(windowWidth - 200, 50, text="100%", font=lbl_font)



    def startSave(self):
        if(self.saving == False):
            self.recButton['text'] = "Stop saving"
            now = datetime.now()
            self.file = open("savings/{}.csv".format(now), 'w')
            self.cam.startSavingVideo("savings/{}.avi".format(now))
            self.saving = True

        else:
            self.recButton['text'] = "Start saving"
            self.saving = False
            self.cam.stopSavingVideo()
            self.file.close()


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


    def startWiiBoardLoop(self):
        if(self.flag):
            self.flag = False
            self.updateCamera()
        else:
            self.flag = True

        self.check_wiiBoard()
        self.master.after(1000//FPS, self.startWiiBoardLoop)


    def check_wiiBoard(self):
        x, y = self.update_wiiBoard()
        self.update_COG_position(x, y)

        if self.flag:
            return

        if self.saving == True:
            self.file.write("{},{}\n".format(x,y))

    def startWiiBoardBatteryPolling(self):
        battery = self.wiiB.getBatteryLevel()
        self.canvas.itemconfig(self.wiiBoard_battery_Label, text="wiiBoard battery: {}%".format(battery))
        if battery <= 20:
            self.canvas.itemconfig(self.wiiBoard_battery_Label, fill="red")

        self.master.after(5000, self.startWiiBoardBatteryPolling)


    def update_wiiBoard(self):
        try:
            x, y = self.wiiB.getSensorStatus()
            circleX = np.interp(x,(-1, 1),(0,rectW)) + (canvasWidth - rectW)/2
            circleY = np.interp(y,(-1, 1),(rectH,0)) + (canvasHeight-rectH)/2
                    
        except:
            circleX = canvasWidth/2
            circleY = canvasHeight/2

        return circleX, circleY

    def updateCamera(self):
        img = self.cam.getFrame()
        self.labelVideo.configure(image=img)
        self.labelVideo.image = img









root = tk.Tk(className=' A surfear con la wiiBoard')
app = Application(master=root)
app.master.geometry("{}x{}".format(windowWidth, windowHeight))
app.mainloop()

