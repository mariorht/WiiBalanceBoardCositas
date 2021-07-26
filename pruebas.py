#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.format import BUFFER_SIZE
from wiiBoard import wiiBoard
import p5
import time


windowWidth, windowHeight = 1200, 1000
rectW, rectH = 600, 300
imageW, imageH = 285, 900

BUFFER_SIZE = 10
CURRENT_INDEX = 0
last_positions_x = np.zeros(BUFFER_SIZE)
last_positions_y = np.zeros(BUFFER_SIZE)

def setup():
    p5.size(windowWidth, windowHeight)
    clearCanvas()

FirstTime = True
def draw():
    global FirstTime
    if FirstTime == True:
        FirstTime = False
        clearCanvas()

    update_wiiBoard()


def key_pressed(event):
    if(key == 'ENTER'):
        clearCanvas()
    if(key == 'C'):
        print("Calibrado")
        wiiB.calibrar()

def clearCanvas():
    p5.background(204)

    p5.fill(100,100,100,155)
    p5.stroke(0)
    p5.rect((windowWidth - rectW)/2, (windowHeight-rectH)/2, rectW, rectH)

    p5.fill(0,0,0,255)
    p5.text("C: calibrar", 50,50)
    p5.text("Enter: limpiar", 50,65)

    p5.image(img, (windowWidth)/2, (windowHeight)/2, imageW, imageH)





def update_wiiBoard():
    global CURRENT_INDEX
    global last_positions_x 
    global last_positions_y

    try:
        x, y = wiiB.getSensorStatus()
        circleX = p5.remap(x,(-1, 1),(0,rectW)) + (windowWidth - rectW)/2
        circleY = p5.remap(y,(-1, 1),(rectH,0)) + (windowHeight-rectH)/2

       
        last_positions_x[CURRENT_INDEX] = circleX
        last_positions_y[CURRENT_INDEX] = circleY
                
    except:
        last_positions_x[CURRENT_INDEX] = windowWidth/2
        last_positions_y[CURRENT_INDEX] = windowHeight/2

    clearCanvas()
    p5.no_stroke()
    p5.fill(0,0,255,100)
    for i in range(BUFFER_SIZE):
        p5.circle((last_positions_x[i],last_positions_y[i]), 10.0)
    
    CURRENT_INDEX = CURRENT_INDEX +1
    if(CURRENT_INDEX >= BUFFER_SIZE):
        CURRENT_INDEX = 0

    time.sleep(0.005)

    


if __name__ == '__main__':
    wiiB = wiiBoard()
    wiiB.connect()
    wiiB.print_info()
    wiiB.calibrar()

    img = p5.load_image("images/tabla.png")
    p5.image_mode('center')


    p5.run(frame_rate=60)



        
