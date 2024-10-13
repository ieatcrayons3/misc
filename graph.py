import numpy as np
import cv2
from math import *

def graph(sig, scale = None, offset = None, hold = True, continuous = True, name = None, linecolor = 1, bgcolor = 0, lineweight = 1, headless = False, labels = True, grid = True):
    if name == None: #sets the default name of the graph for CV2 to name the window
        name = "steven" #lmao
    if scale == None: #autoscale data to fit fully within window. note if you have insane outliers it will squish everything else
        scale = (len(sig)/500,500/(max(1,max(sig) - min(sig))))
    if offset == None: #auto offsets to center data. i.e. if your data spans 500 to 1000 it will cut off the 0-500 portion of the graph
        offset = (0, min(sig))
    arr = np.ones((500,500)) #array init
    arr *= bgcolor
    samp = 0
    p0 = (0,499-floor((sig[samp]-offset[1])*scale[1])) #gets initial p0 for the continuous line graph
    if len(sig) < 500: #honestly this is really hacky but the vibes to fix it were Not there
        stepsize = floor(500 / len(sig)) #interpolation of sample for smaller-than-resolution amounts. 
        for x in range(len(sig)): #iterates over data and plots each point
            samp = round(scale[0] * x * stepsize)
            p1 = (stepsize*x,499-floor((sig[samp]-offset[1])*scale[1])) #translation of point from array space to graph space
            if continuous:
                cv2.line(arr,p0,p1, linecolor, lineweight)
                p0 = p1
            else:
                arr[p1] = 255 * linecolor #cv2 is rancid for using 0-1 as a line color even if the array is in 8 bit color space

            #arr[x,50] = 255
    else:

        for x in range(500):
            samp = round(scale[0] * x) #interpolator for >= 500 point data. this kind of sucks i should actually interpolate the data as opposed to just picking nearest points
            p1 = (x,499-floor((sig[samp]-offset[1])*scale[1]))
            if continuous:
                cv2.line(arr,p0,p1,linecolor, lineweight)
                p0 = p1
            else:
                arr[p1] = 255*linecolor
            #arr[x,50] = 255
    if not continuous: #again, my finest bodge
        arr = cv2.flip(arr, 0)
        arr = cv2.rotate(arr, cv2.ROTATE_90_CLOCKWISE)

    if labels:
        maxval = max(sig)
        minval = min(sig)
        step = (maxval - minval) / 10
        pn = minval-1
        for i in range(10):
            label = round(step*i + minval,2)
            print(label, pn)
            if label != pn: #keeps labels from repeating if they round to the same data point

                arr = cv2.putText(arr, str(label), (0,500-i*50-7), 0, 0.3, linecolor, 1, cv2.LINE_AA)
                pn = label
                if grid:
                    arr = cv2.line(arr, (0,round(500-i*50)), (499,round(500-i*50)), linecolor / 4, 1)
                else:
                    arr = cv2.line(arr, (5,round(500-i*50)), (30,round(500-i*50)), linecolor / 4, 1)
    if headless:
        return arr
    else: #will literally show the image on client. cool for personal stuff less so if you need the image for anything other than looking pretty
        cv2.imshow(name, arr)
        if hold:
            cv2.waitKey(0)
        else:
            cv2.waitKey(1)
#data = [10 * x*x for x in range(1000)]
#graph(data)


if __name__ == "__main__":
    from random import randint
    from math import atan, pi, log
    def basefunc(x):
        return log(x/100+1)

    def simulnoise(points = 1000, noise = 0.2):

        data = np.zeros((points))
        for i in range(points):
            noisedat = np.random.normal(1,noise,points)
            data[i] = basefunc(i) * noisedat[i]
        return data
    dataToPlot = simulnoise()
    graphdata = graph(dataToPlot, continuous=True, linecolor = 0.25, bgcolor = 0, lineweight = 1, headless = True, labels=False)
    graphdata += graph(dataToPlot, continuous=False, linecolor = 1, bgcolor = 0, lineweight = 1, headless = True) #yes you can just add them
    cv2.imshow("graph", graphdata)
    cv2.waitKey(0)
