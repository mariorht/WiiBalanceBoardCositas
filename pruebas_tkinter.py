#!/usr/bin/env python

import tkinter as tk
from wiiBoard import wiiBoard
from p5 import remap

windowWidth, windowHeight = 1200, 1000
rectW, rectH = 300, 150
imageW, imageH, offsetX = 285, 900, 5
CIRCLE_RADIUS = 5
FPS = 100


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.check_wiiBoard()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=windowWidth, height=windowHeight)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        
        self.wiiBoard = self.canvas.create_rectangle(windowWidth/2-rectW/2, windowHeight/2-rectH/2, windowWidth/2+rectW/2, windowHeight/2+rectH/2)

        self.tabla = tk.PhotoImage(file='images/tabla.png')
        self.canvas.create_image(windowWidth/2+offsetX, windowHeight/2,anchor=tk.CENTER, image=self.tabla)


        self.COG = self.canvas.create_circle(windowWidth/2, windowHeight/2, CIRCLE_RADIUS, fill='blue')


    def get_COG_position(self):
        pos = self.canvas.coords(self.COG)
        return pos[0]+CIRCLE_RADIUS, pos[1]+CIRCLE_RADIUS

    def set_COG_postion(self, x, y):
        self.canvas.moveto(self.COG, x - CIRCLE_RADIUS -1, y - CIRCLE_RADIUS - 1)


    def update_COG_position(self, x, y):
        self.set_COG_postion(x, y)


    def check_wiiBoard(self):
        x, y = update_wiiBoard()
        self.update_COG_position(x, y)
        self.master.after(1000//FPS, self.check_wiiBoard)

def update_wiiBoard():
    try:
        x, y = wiiB.getSensorStatus(10)
        print(x,y)
        circleX = remap(x,(-1, 1),(0,rectW)) + (windowWidth - rectW)/2
        circleY = remap(y,(-1, 1),(rectH,0)) + (windowHeight-rectH)/2
                
    except:
        circleX = windowWidth/2
        circleY = windowHeight/2

    return circleX, circleY





wiiB = wiiBoard()
wiiB.connect()
wiiB.print_info()
wiiB.calibrar()


root = tk.Tk(className=' A surfear con la wiiBoard')
app = Application(master=root)
app.master.geometry("{}x{}".format(windowWidth, windowHeight))
app.mainloop()

