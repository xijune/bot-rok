from ppadb.client import Client
import time
import cv2 as cv
import numpy as np
import re
import win32gui
import pyautogui

# Addition pour cliquer à la bonne place
# (1920 / 100) - (1473 / 100) * 23.28125
# 2.51
# RESY = 2.5164

TRAPIDE = 2.5
TLENT = 6

# Connection sur l'emulateur avec l'ip et port de base
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print ('pas de device attaché')
    quit()
device = devices[0]


def Tap(cordsTap):
    #Tap a la coordonnee choisi
    tap = device.shell('input touchscreen tap ' + str(cordsTap))
    return tap


def ScreenShot():
    hwnd = win32gui.FindWindow(None, 'BlueStacks')

    win32gui.ShowWindow(hwnd, 9) # Un-minimize
    win32gui.SetForegroundWindow(hwnd)

    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

    screenshot = pyautogui.screenshot(region=(x, y + 33, (x1 - 33), y1 - 33))
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    cv.imwrite('screenshot.png', screenshot)


def ImgRecherche(template, thresholdJour):
    ScreenShot()
    target = cv.imread('screenshot.png')
    template = cv.imread('images/' + template)

    md = cv.TM_CCOEFF_NORMED
    th, tw = template.shape[:2]

    result = cv.matchTemplate(target, template, md)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    tl = max_loc
    br = (tl[0]+tw, tl[1]+th)

    # print(max_val)
    # cv.rectangle(target, tl, br, (0,0,255))
    # cv.imshow('matches', target)
    # cv.waitKey(0)

    centerXEmu = (max_loc[0] + tw//2)
    centerX = (centerXEmu / 14.73)
    centerX =  centerXEmu + (4.4736 * centerX)

    centerYEmu = (max_loc[1] + th//2)
    centerY = (centerYEmu / 8.29)
    centerY =  centerYEmu + (2.5164 * centerY)

    centers = str(centerX) + ' ' + str(centerY)

    if max_val > thresholdJour:
        # print(centers)
        return centers

    else:
        return " "


def Exploration():
    cord_text = ImgRecherche('explorer.png', 0.73)
    cord_bat = ImgRecherche('batExplorer.png', 0.8)
    if cord_text != " " and cord_bat != " ":
        print('Exploration en cours')
        Tap(cord_bat)
        time.sleep(TRAPIDE)
        Tap(ImgRecherche('loupe.png', 0.98))
        time.sleep(TRAPIDE)
        cord_btn = ImgRecherche('btnExplorer.png', 0.98)
        if cord_btn != " ":
            Tap(cord_btn)
            time.sleep(TLENT)
            Tap(ImgRecherche('btnExplorer.png', 0.95))
            time.sleep(TRAPIDE)
            Tap(ImgRecherche('btnEnvoyer.png', 0.94))
            time.sleep(TRAPIDE)
            Tap(ImgRecherche('btnRentre.png', 0.98))
            print('Exploration terminé, Retour à la base')
            time.sleep(TLENT)
        else:
            pass
    else: 
        print('Aucune exploration disponible')
    


def Collecte():
    cord_mais = ImgRecherche('mais.png', 0.7)
    if cord_mais != " ":
        Tap(cord_mais)
        print('Collection maîs')

    cord_bois = ImgRecherche('bois.png', 0.7)
    if cord_bois != " ":
        Tap(cord_bois)
        print('Collection bois')
    
    else:
        print('Aucune collection disponible')


def Infenterie():
    ll = 2


def Archer():
    cord_pause = ImgRecherche('archerPause.png', 0.45)
    cord_bat = ImgRecherche('batArcher.png', 0.9)
    cord_collect = ImgRecherche('archer.png', 0.98)
    if cord_pause != " " and cord_bat != " " or cord_collect != " ":
        if cord_collect != " ":
            Tap(cord_collect)

        time.sleep(TRAPIDE)
        Tap(ImgRecherche('batArcher.png', 0.9))
        time.sleep(TRAPIDE)
        Tap(ImgRecherche('formation.png', 0.90))
        time.sleep(TLENT)
        Tap(ImgRecherche('train.png', 0.90))
    else:
        print('Archer déjà en formation')


def Cadeau():
    pix = (105, 208)


while True:
    Collecte()
    Archer()
    Exploration()