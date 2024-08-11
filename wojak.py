import nltk
import wikipedia
from twitterbot import tweet
import cv2
from urllib.request import urlopen
import numpy as np
from random import shuffle


#def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
#    resp = urlopen(url)
#    image = np.asarray(bytearray(resp.read()), dtype="uint8")
#    image = cv2.imdecode(image, readFlag)
##    return image

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

google_API_key = 


blocklist = ["be","refer", "provide"]

#def scale(img, scale_percent = 15):
#    width = int(img.shape[1] * scale_percent / 100)
#    height = int(img.shape[0] * scale_percent / 100)
#    dim = (width, height)

    # resize image
#    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#    return resized

def wojak(noun):
    #if wiki_wiki == None:
    #    wiki_wiki = wikipediaapi.Wikipedia('en')
    try:
        page_py = wikipedia.summary(noun)
        #if False:
        #    im = wikipedia.page(noun).images[0]
            #cv2.imshow("i",im)
            #if "svg" not in im:
                #image = url_to_image(im)
                #image = scale(image, 30)
                #cv2.imshow(noun, image)
                #cv2.waitKey(0)

    except:# wikipedia.exceptions.DisambiguationError:
        return None
    pword = None
    if len(page_py) > 50:
        #print("Page - Title: %s" % page_py.title)
            # Page - Title: Python (programming language)
        #print("Page - Summary: %s" % page_py.summary[0:60])


        text = nltk.tokenize.word_tokenize(page_py)
        text = nltk.pos_tag(text)
        pword = None
        for j in text:
            if j[1] == "VB" and j[0] not in blocklist:
                #print(j[0])
                pword = j[0]
                break
    if pword != None:
        txt = "Say the line {name}jack!\nI'm gonna {word}\nI love this guy"
        pword = pword.lower().replace(" ","")
        w = txt.format(name = noun, word = pword)
        #print(w)
        return w

if __name__ == "__main__":
    with open("nouns.txt","r") as f: #it needs a list of nouns
        lines = f.readlines()
    lines = [i.replace("\n","") for i in lines]
    shuffle(lines)
    lines = lines[0:48]
    #print(lines)
    for i in lines:
        w=wojak(i)
        if w != None:
            print(w)
            print()
