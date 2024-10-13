import numpy as np
import cv2
from math import *

def graph(sig, scale = None, offset = None, hold = True, continuous = True, name = None, linecolor = 1, bgcolor = 0, lineweight = 1, headless = False, labels = True, grid = True):
    if name == None:
        name = "steven"
    if scale == None:
        scale = (len(sig)/500,500/(max(1,max(sig) - min(sig))))
    if offset == None:
        offset = (0, min(sig))
    arr = np.ones((500,500))
    arr *= bgcolor
    samp = 0
    p0 = (0,499-floor((sig[samp]-offset[1])*scale[1]))
    if len(sig) < 500:
        stepsize = floor(500 / len(sig))
        for x in range(len(sig)):
            samp = round(scale[0] * x * stepsize)
            p1 = (stepsize*x,499-floor((sig[samp]-offset[1])*scale[1]))
            if continuous:

                cv2.line(arr,p0,p1, linecolor, lineweight)
                p0 = p1
            else:
                arr[p1] = 255 * linecolor

            #arr[x,50] = 255
    else:

        for x in range(500):
            samp = round(scale[0] * x)
            p1 = (x,499-floor((sig[samp]-offset[1])*scale[1]))
            if continuous:
                cv2.line(arr,p0,p1,linecolor, lineweight)
                p0 = p1
            else:
                arr[p1] = 255
            #arr[x,50] = 255
    if not continuous:
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
            if label != pn:

                arr = cv2.putText(arr, str(label), (0,500-i*50-7), 0, 0.3, linecolor, 1, cv2.LINE_AA)
                pn = label
                if grid:
                    arr = cv2.line(arr, (0,round(500-i*50)), (499,round(500-i*50)), linecolor / 4, 1)
                else:
                    arr = cv2.line(arr, (5,round(500-i*50)), (30,round(500-i*50)), linecolor / 4, 1)
    if headless:
        return arr
    else:
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
    graphdata += graph(dataToPlot, continuous=False, linecolor = 1, bgcolor = 0, lineweight = 1, headless = True)
    cv2.imshow("graph", graphdata)
    cv2.waitKey(0)
