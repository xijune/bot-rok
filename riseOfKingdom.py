from ppadb.client import Client
from PIL import Image
import time
import tkinter as tk
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

TRAPIDE = .05
TLENT = 3

#RGBA des pixels
MAISMIN = (240, 198, 32, 255)
MAISMAX = (255, 218, 52, 255)
BOISMIN = (213, 150, 100, 255)
BOISMAX = (233, 170, 120, 255)

BOUTTONHOME = (113, 229, 252, 255)

EXPLORERJOURMIN = (110, 114, 87, 255)
EXPLORERJOURMAX = (130, 134, 107, 255)
EXPLORERNUITMIN = (80, 93, 88, 255)
EXPLORERNUITMAX = (100, 113, 108, 255)

FORMATIONJOURMIN = (137, 163, 68, 255)
FORMATIONJOURMAX = (157, 183, 88, 255)

IFORMATIONNUITMIN = (36, 85, 74, 255)
IFORMATIONNUITMAX = (56, 105, 94, 255)

AFORMATIONNUITMIN = (37, 85, 79, 255)
AFORMATIONNUITMAX = (57, 105, 99, 255)

PRETMIN = (148, 60, 0, 255)
PRETMAX = (168, 80, 20, 255)

CADEAUMIN = (217, 0, 0, 255)
CADEAUMAX = (237, 20, 20, 255)

RECLAMERMIN = (0, 173, 4, 255)
RECLAMERMAX = (20, 193, 24, 255)

NOTIFMIN = (217, 0, 0, 255)
NOTIFMAX = (237, 20, 20, 255)

bolReclame = False

def Adb():
    # Connection sur l'emulateur avec l'ip et port de base
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print ('pas de device attaché')
        quit()
    device = devices[0]
    return device

def Tap(cordsTap):
    #Tap a la coordonnee choisi
    tap = Adb().shell('input touchscreen tap ' + cordsTap)
    return tap

def ScreenShot():
    #Prend un screenshot et lis l'image
    image = Adb().screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)
    image = Image.open('screen.png')
    return image

def ImgRecherche():
    img = cv.imread('messi5.jpg',0)
    img2 = img.copy()
    template = cv.imread('template.jpg',0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()

def Pix(cordPixX, cordPixY):
    #Prend le RGBA du pixel de la coordonée
    pix = ScreenShot().getpixel((cordPixX, cordPixY))
    return pix

def Base():
    #Si correcte, appuis sur le boutton Home
    pix = Pix(76, 981)
    if pix == BOUTTONHOME:
        Tap('76 981')
        time.sleep(TLENT)
    else:
        pass

def Exploration():
    #Si correcte, fait une exploration
    pix = Pix(1175, 475)
    if pix <= EXPLORERJOURMAX and pix >= EXPLORERJOURMIN or pix <= EXPLORERNUITMAX and pix >= EXPLORERNUITMIN:
        Tap('1160 610')
        time.sleep(TRAPIDE)
        Tap('1360 810')
        time.sleep(TRAPIDE)
        Tap('1500 480')
        time.sleep(TLENT)
        Tap('1200 710')
        time.sleep(TRAPIDE)
        Tap('1500 250')
        time.sleep(TRAPIDE)
        Tap('76 981')
        time.sleep(TLENT)
        print('Retour à la base')

    else:
        print('Aucun exploreur disponible')
        pass
    time.sleep(TLENT)

def Collecte():
    #Si correcte, collecte
    pix = Pix(983, 671)
    if pix <= MAISMAX and pix >= MAISMIN:
        Tap('983 671')
        print('Collecte du maîs')

    pix = Pix(827,794)
    if pix <= BOISMAX and pix >= BOISMIN:
        Tap('827 794')
        print('Collecte du bois')

    print('Collection terminee')

def Infenterie():
    #Si correcte, passe
    pix = Pix(695, 741)
    if pix <= FORMATIONJOURMAX and pix >= FORMATIONJOURMIN or pix <= IFORMATIONNUITMAX and pix >= IFORMATIONNUITMIN:
        print('Lancement infenterie')

        pix = Pix(770, 565)
        if pix <= PRETMAX and pix >= PRETMIN:
            Tap('780 650')
            time.sleep(TLENT)
            Tap('780 650')
            time.sleep(TRAPIDE)
            Tap('990 860')
            time.sleep(TRAPIDE)
            Tap('1480 890')

        #Sinon, juste relance
        else:
            Tap('780 650')
            time.sleep(TRAPIDE)
            Tap('990 860')
            time.sleep(TRAPIDE)
            Tap('1480 890')

    else:
        print('Infenterie deja en formation')
        pass

def Archer():
    #Si correcte,
    pix = Pix(876, 572)
    if pix <= FORMATIONJOURMAX and pix >= FORMATIONJOURMIN or pix <= AFORMATIONNUITMAX and pix >= AFORMATIONNUITMIN:
        print('Lancement archer')

        pix = Pix(957, 396)
        if pix <= PRETMAX and pix >= PRETMIN:
            Tap('962 484')
            time.sleep(TLENT)
            Tap('962 484')
            time.sleep(TRAPIDE)
            Tap('1172 694')
            time.sleep(TRAPIDE)
            Tap('1480 890')

        #Sinon, juste relance
        else:
            Tap('962 484')
            time.sleep(TRAPIDE)
            Tap('1172 694')
            time.sleep(TRAPIDE)
            Tap('1480 890')

    else:
        print('Archer deja en formation')
        pass

def Cadeau():
    pix = Pix(105, 208)
    if pix <= CADEAUMAX and pix >= CADEAUMIN:
        Tap('70 250')
        time.sleep(TLENT)

        pix = Pix(1463, 611)
        if pix <= RECLAMERMAX and pix >= RECLAMERMIN:
            bolReclame = True

        while bolReclame:
            Tap('1463 611')
            time.sleep(TLENT)  

            pix = Pix(1463, 611)
            if pix > RECLAMERMAX or pix < RECLAMERMIN :
                bolReclame = False

        pix = Pix(96, 396)
        if pix <= NOTIFMAX and pix >= NOTIFMIN:
            Tap('170 472')

while True:
    Archer()
    Infenterie()
    Exploration()