from ppadb.client import Client
from PIL import Image
import time

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print ('pas de device attaché')
    quit()

device = devices[0]

image = device.screencap()

with open('screen.png', 'wb') as f:
    f.write(image)

image = Image.open('screen.png')

couleur = image.getpixel((1220, 470))

explorerJour = (202, 213, 169, 255)
explorerNuit = (151, 174, 172, 255)

while True:
    if couleur == explorerJour:
        device.shell('input touchscreen tap 1160 610')
        time.sleep(1)
        device.shell('input touchscreen tap 1360 810')
        time.sleep(1)
        device.shell('input touchscreen tap 1500 480')

    elif couleur == explorerNuit:
        device.shell('input touchscreen tap 1160 610')
        time.sleep(1)
        device.shell('input touchscreen tap 1360 810')
        time.sleep(1)
        device.shell('input touchscreen tap 1500 480')

    else:
        pass 