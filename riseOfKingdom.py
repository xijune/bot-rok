from ppadb.client import Client
from PIL import ImageGrab
import time
import cv2 as cv
import numpy as np
import re
import win32gui

# Addition pour cliquer à la bonne place
RESX = 195
RESY = 180

TRAPIDE = 0.5
TLENT = 4

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
    windows_list = []
    toplist = []
    def enum_win(hwnd, result):
        win_text = win32gui.GetWindowText(hwnd)
        windows_list.append((hwnd, win_text))
    win32gui.EnumWindows(enum_win, toplist)

    game_hwnd = 0
    for (hwnd, win_text) in windows_list:
        if "BlueStacks" in win_text:
            game_hwnd = hwnd

    win32gui.ShowWindow(game_hwnd, 9) # Un-minimize
    win32gui.ShowWindow(game_hwnd, 5)
    win32gui.SetForegroundWindow(game_hwnd)
    time.sleep(1)

    position = win32gui.GetWindowRect(game_hwnd)

    position = (position[0], position[1] + 33, position[2] - 33, position[3])

    screenshot = ImageGrab.grab(position)
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    cv.imwrite('screenshot.png', screenshot)


def ImgRecherche(template, threshold):
    ScreenShot()
    target = cv.imread('screenshot.png')
    template = cv.imread('images/' + template)

    time.sleep(1)
    md = cv.TM_CCOEFF_NORMED
    th, tw = template.shape[:2]
    centers = []

    result = cv.matchTemplate(target, template, md)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    tl = max_loc
    br = (tl[0]+tw, tl[1]+th)
    centers.append((max_loc[0] + tw//2 + RESX, max_loc[1] + th//2 + RESY))

    centers = re.sub("[^0-9]", " ", str(centers))
    
    print(max_val)
    cv.rectangle(target, tl, br, (0,0,255))
    cv.imshow('matches', target)
    cv.waitKey(0)
    if max_val > threshold:
        print(centers)
        return centers

    if not tl[0] in range(10, 40) or tl[1] > 20:
        return ''


def Exploration():
    Tap(ImgRecherche('explorer.png'))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('loupe.png'))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('btnExplorer.png'))
    time.sleep(TLENT)
    Tap(ImgRecherche('btnExplorer.png'))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('btnExplorer.png'))


def Collecte():
    Tap(ImgRecherche('mais.png'))

    Tap(ImgRecherche('bois.png'))

    print('Collection terminee')


def Infenterie():
    ll = 2


def Archer():
    Tap(ImgRecherche('archer.png', 0.469))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('archerPause.png', 0.55))
    time.sleep(TRAPIDE)
    Tap(ImgRecherche('formation.png', 0.99))
    time.sleep(TLENT)
    Tap(ImgRecherche('train.png'))


def Cadeau():
    pix = (105, 208)

ImgRecherche('train.png', 0.99)