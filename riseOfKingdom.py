from ppadb.client import Client
from PIL import Image
import time
import tkinter as tk
import cv2 as cv
import numpy as np
import re


SENSI =  0.949

TRAPIDE = 1
TLENT = 3

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
    image = cv.imread('screen.png')
    return image

def ImgRecherche(template):
    target = ScreenShot()
    template = cv.imread(template)
    time.sleep(TRAPIDE)
    method = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED]
    th, tw = template.shape[:2]
    centers = []
    for md in method:
        result = cv.matchTemplate(target, template, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0]+tw, tl[1]+th)
        cv.rectangle(target, tl, br, (0,0,255))

    centers.append((max_loc[0] + tw//2, max_loc[1] + th//2))

    cv.imwrite('output.png', target)

    centers = re.sub("[^0-9]", " ", str(centers))

    return centers

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
    Tap(ImgRecherche('explorer.png'))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('loupe.png'))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('btnExplorer.png'))
    time.sleep(TLENT)


def Collecte():
    Tap(ImgRecherche('mais.png'))

    Tap(ImgRecherche('bois.png'))

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
    Tap(ImgRecherche('archerfini.png'))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('archer.png'))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('formation.png'))
    time.sleep(TLENT)
    Tap(ImgRecherche('train.png'))

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

