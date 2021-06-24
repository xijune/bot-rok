import cv2 as cv
import numpy as np
import win32gui
import time
import re
import pyautogui
import os
from ppadb.client import Client

# Addition pour cliquer à la bonne place
RESX = 195
RESY = 180

def Adb():
    # Connection sur l'emulateur avec l'ip et port de base
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print ('pas de device attaché')
        quit()
    device = devices[0]
    return device


def ImgRecherche(template, threshold):
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

    else:
        return ''

def ConnectionAdb():
    os.system('cd D:\git-repo\platform-tools & adb connect loa')
    

def screenshot():
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

ConnectionAdb()
