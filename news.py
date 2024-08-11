import numpy as np
import cv2
from math import floor
import random
import requests
from win32com.client import Dispatch
import time
#rom multiprocessing import Process
import threading


def bigflash(sr):
    z = np.zeros((1080,1920))
    cv2.namedWindow(" ", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(" ",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    #cv2.imshow("window", img)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 10
    org = (floor(1920/2 - len(sr)), floor(1080/2 + 2 * fontScale))
    # fontScale

    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 2 * fontScale
    # Using cv2.putText()
    z = cv2.putText(z, sr, org, font, fontScale, color, thickness, cv2.LINE_AA)
    org = (org[0], org[1] + 50)
    cv2.imshow(" ",z)
    q = cv2.waitKey(len(sr) * 200)

    return q

def talk(sr):
    print("test")
    speak = Dispatch("SAPI.Spvoice")
    speak.Speak(sr)

def scroll(sr):
    cv2.namedWindow(" ", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(" ",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    #cv2.imshow("window", img)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 10# / len(sr)
    color = (1,1,1)
    thickness = floor(2 *  fontScale)
    speed = 20

    textSize = cv2.getTextSize(sr, font, fontScale=fontScale, thickness=thickness)
    org = (1920, floor(1080/2 + textSize[0][1] / 2))
    #speak = Dispatch("SAPI.Spvoice")
    #x = Process(target = talk, args=(sr,))
    #speak.Speak(sr)
    #x.start()
    #talk(sr)
    for i in range(floor((1920 + textSize[0][0]) / speed)):
        #org = (org[0] , org[1])
        z = np.zeros((1080,1920))
        z = cv2.putText(z, sr, org, font, fontScale, color, thickness, cv2.LINE_AA)
        org = (org[0]-speed, org[1])
        cv2.imshow(" ", z)
        if cv2.waitKey(1) == ord("q"):
            quit()
    #x.join()



def NewsFromSrc():

    # BBC news api
    # following query parameters are used
    # source, sortBy and apiKey
    query_params = {
      "source": "google-news",
      "sortBy": "top",
      "apiKey": "31a5e1d5d8ce4bbfa4afa82d7d4679a4",
      "country": "us"

    }
    main_url = " https://newsapi.org/v1/articles"

    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()

    # getting all articles in a string article
    article = open_bbc_page["articles"]

    # empty list which will
    # contain all trending news
    results = []

    for ar in article:
        results.append(ar["title"])

    #for i in range(len(results)):

        # printing all trending news
        #print(i + 1, results[i])
    #    scroll(results[i])
    return results

    #to read the news out loud for us
    #from win32com.client import Dispatch
    #speak = Dispatch("SAPI.Spvoice")
    #speak.Speak(results)


#NewsFromSrc()
#scroll("this is a test message")
#scroll("this is a longer test message")
#scroll("test")
ls = []
j = True
def wate():
    for i in range(5000):
        time.sleep(1)
        print(i, end="\r")


while True:

    y = threading.Thread(target=wate)
    y.start()
    #x.join()
    #print("J")
    r = NewsFromSrc()
    for i in r:
        try:
            ls.remove(i)
        except:
            pass
        ls.append(i)
    random.shuffle(ls)
    for i in ls:
        x = threading.Thread(target=scroll,args=(i,))
        x.start()
        talk(i)
        x.join()
    while len(ls) > 10:
        ls.pop(0)#talk(ls.pop(0))
    y.join()
