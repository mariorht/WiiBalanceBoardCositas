import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np


NO_LIST = np.zeros(1000)
NE_LIST = np.zeros(1000)
SO_LIST = np.zeros(1000)
SE_LIST = np.zeros(1000)
index = 0
def new_point(NO, NE, SO, SE):
    global index

    NO_LIST[index] = NO
    NE_LIST[index] = NE
    SE_LIST[index] = SE
    SO_LIST[index] = SO
    
    plt.clf()
    plt.subplot(4,1,1)
    plt.plot(NO_LIST)

    plt.subplot(4,1,2)
    plt.plot(NE_LIST)
    
    plt.subplot(4,1,3)
    plt.plot(SE_LIST)
    
    plt.subplot(4,1,4)
    plt.plot(SO_LIST)

    plt.show(block=False)
    index = index +1
    if index==1000:
        index = 0







#################################################################################

from wiiBoard import wiiBoard

wiiB = wiiBoard()
wiiB.connect()
wiiB.print_info()


left_column = [
    [sg.Text(0,key="NO",size=(10,1))],
    [sg.Text(0,key="SO",size=(10,1))]
]
right_column = [
    [sg.Text(0,key="NE",size=(10,1))],
    [sg.Text(0,key="SE",size=(10,1))]
]

layout = [
    [
        sg.Column(left_column),
        sg.VSeperator(),
        sg.Column(right_column),
    ]
]

new_point(0,0,0,0)
# plt.show()

# Create the window
window = sg.Window("Demo", layout)





# Create an event loop
while True:
    event, values = window.read(timeout=1)
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

    try:
        NO, NE, SO, SE = wiiB.read_events()
        window["NO"].update(NO)
        window["SO"].update(SO)
        window["NE"].update(NE)
        window["SE"].update(SE)

        new_point(NO, NE, SO, SE)


    except:
        pass

    
window.close()    
