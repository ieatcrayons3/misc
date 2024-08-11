#vectorfield.py
import cv2
import numpy as np
from math import *
import time

white=(1,1,1)


def dx(x,y):
    return (y-35)

def dy(x,y):
    return -(x+35)

def fstrength(x,y):
    magnetude = sqrt( x**2 + y**2 )
    if magnetude == 0:
        return x , y
    return round(dx(x,y)/1500)+x, round(25*dy(x,y)/1500)+y



field = np.zeros((500,500))

location=[250,240]
force=[0,10]
c=0
res = 15
while True:
    for x in range(int(500/res)):
        for y in range(int(500/res)):
                cv2.line(field,(res*x,res*y),(fstrength(res*x,res*y)),white)
    location = location[0] + dx(location[0],location[1]) + force[0], location[1] + dy(location[0],location[1]) + force[1]
    cv2.circle(field, (round(location[0]),round(location[1])), 2, white, -1)
    cv2.imshow('field',field)
    if cv2.waitKey(1) ==ord('q'):
        break
    time.sleep(0.01)
    field = np.zeros((500,500))
