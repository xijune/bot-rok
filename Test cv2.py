import cv2 as cv
import numpy as np
import re
import time
from PIL import Image
import os
from ppadb.client import Client

def Adb():
    # Connection sur l'emulateur avec l'ip et port de base
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print ('pas de device attaché')
        quit()
    device = devices[0]
    return device

def ScreenShot():
    #Prend un screenshot
    image = Adb().screencap()
    with open('1.png', 'wb') as f:
        f.write(image)
    image = '1.png'
    return image


def template_demo():
    screen = ScreenShot()
    capture = 'archer.png'

    target = cv.imread(screen, cv.IMREAD_UNCHANGED)
    template = cv.imread(capture, cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(target, template, cv.TM_CCOEFF_NORMED)

    min_val, max_val, max_loc, min_loc = cv.minMaxLoc(result)

    print('Best match top left position: %s' % str(max_loc))
    print('Best match confidence: %s' % str(max_val))

    threshold = 0.99
    if max_val >= threshold:
        print('Found archer')

        archer_w = template.shape[1]
        archer_h = template.shape[0]

        top_left = max_loc
        bottom_right = (top_left[0] + archer_w, top_left[1] + archer_h)

        cv.rectangle(target, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
    
        cv.imshow('Result', target)
        cv.waitKey()

    else:
        print('Archer not found')


template_demo()