import collections
from ppadb.client import Client
from PIL import Image
import time
import tkinter as tk
import cv2
import numpy as np
import re


SENSI =  0.9841

TRAPIDE = .05
TLENT = 3

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
    image = 'screen.png'
    return image

def ImgRecherche(obj, sensibilite):
    image = cv2.imread(ScreenShot(), cv2.IMREAD_COLOR )
    template = cv2.imread(obj, cv2.IMREAD_COLOR)
    h, w = template.shape[:2]

    methode = cv2.TM_CCORR_NORMED

    res = cv2.matchTemplate(image, template, methode)
    res_h, res_w = res.shape[:2]

    #Initialisation du max_val pour commencer la boucle
    max_val = 1
    centers = []
    while max_val > sensibilite:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > sensibilite:
            centers.append( (max_loc[0] + w//2, max_loc[1] + h//2) )

            x1 = max(max_loc[0] - w//2, 0)
            y1 = max(max_loc[1] - h//2, 0)

            x2 = min(max_loc[0] + w//2, res_w)
            y2 = min(max_loc[1] + h//2, res_h)

            res[y1:y2, x1:x2] = 0

            image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,255,0) )

    centers = re.sub("[^0-9]", " ", str(centers))

    cv2.imwrite('output.png', image)

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
    Tap(ImgRecherche("mais.png", SENSI))

    Tap(ImgRecherche("bois.png", SENSI))

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
    Tap(ImgRecherche("archerfini.png", SENSI))
    Tap(ImgRecherche("archer.png", SENSI))
    Tap(ImgRecherche("formation.png", SENSI))
    Tap(ImgRecherche("train.png", SENSI))

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
