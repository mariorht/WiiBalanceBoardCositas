#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from wiiBoard import wiiBoard
import p5
from scipy.interpolate import interp1d


windowWidth, windowHeight = 480, 360
minX = -400000
maxX = 400000
minY = -200000
maxY = 200000


def setup():
    p5.size(windowWidth, windowHeight)
    p5.no_stroke()
    p5.background(204)

def draw():
    update_wiiBoard()


def key_pressed(event):
    p5.background(204)





def update_wiiBoard():
    try:
        NO, NE, SO, SE = wiiB.read_events()
        meanX = (NE + SE - NO - SO)*43
        meanY = (NO + NE - SO - SE)*23

        p5.fill(0,0,255,100)
        p5.circle((mx(meanX), my(meanY)), 10.0)


    except:
        pass


if __name__ == '__main__':
    wiiB = wiiBoard()
    wiiB.connect()
    wiiB.print_info()
    f = open("values.txt", "w")

    mx = interp1d([minX, maxX],[0,windowWidth])
    my = interp1d([minY, maxY],[windowHeight,0])

    p5.run()



        
