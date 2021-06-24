from ppadb.client import Client
import time
import cv2 as cv
import numpy as np
import win32gui
import pyautogui

##################################  Déclaration des constantes #####################################

BORDURE = 33                        # Valeur pour enlever le trop de bordure
RESX = 4.4736                       # Valeur pour adapter la recherche de X sur l'emulateur
RESY = 2.5164                       # Valeur pour adapter la recherche de Y sur l'emulateur
TAILLE_X = 14.73                    # Valeur trouver avec la taille X du screenshot / 100
TAILLE_Y = 8.29                     # Valeur trouver avec la taille Y du screenshot / 100
TRAPIDE = 2.5                       # Valeur temps rapide
TLENT = 4                           # Valeur temps lente
IP = '127.0.0.1'                    # Ip de base de l'emulateur
PORT = 5037                         # Port de base de l'emulateur
SCREEN = 'screenshot.png'           # Nom donné à l'emulateur
DOC_IMG = 'images/'                 # Chemin pour accéder au images
NOTHING = " "                       # Espace pour evité une erreur avec le 'Tap()'
MARGE_MOY = 0.7                     # Marge moyenne
MARGE_P = 0.9                       # Marge petite

#####################################################################################################

# Connection sur l'emulateur avec l'ip et port de base
adb = Client(host=IP, port=PORT)
devices = adb.devices()
if len(devices) == 0:
    print ('pas de device attaché')
    quit()
device = devices[0]


def Tap(cordsTap):
    #Tap a la coordonnee choisi avec le text qui vien avec dans le shell de l'emulateur
    tap = device.shell('input touchscreen tap ' + str(cordsTap))
    return tap


def ScreenShot():

    # Trouve l'application 'BlueStacks', là Un-minimize si necessaire et là met au premier plan
    hwnd = win32gui.FindWindow(None, 'BlueStacks')
    win32gui.ShowWindow(hwnd, 9) # Un-minimize
    win32gui.SetForegroundWindow(hwnd)

    # Calcule la taille de l'application et garde les coordonnées pour le screenshot
    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

    # Prend un screenshot avec les coordonnées trouver, enlève la bordure non-necessaire et sauvegarde
    screenshot = pyautogui.screenshot(region=(x, y + BORDURE, (x1 - BORDURE), y1 - BORDURE))
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    cv.imwrite(SCREEN, screenshot)


def ImgRecherche(template, threshold):
    # Prend un screenshot avant d'effectué le matching
    ScreenShot()

    # Effectue le matching de l'image donné dans le screenshot avec une norme et donne le restultat
    target = cv.imread(SCREEN)
    template = cv.imread(DOC_IMG + template)

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

    # Calcule le centre du rectangle correspondant trouver
    centerXEmu = (max_loc[0] + tw//2)
    centerX = (centerXEmu / TAILLE_X)
    centerX =  centerXEmu + (RESX * centerX)

    centerYEmu = (max_loc[1] + th//2)
    centerY = (centerYEmu / TAILLE_Y)
    centerY =  centerYEmu + (RESY * centerY)

    # Garde le resultat en string pour la compatibilité pour la commande shell
    centers = str(centerX) + ' ' + str(centerY)

    # Retourne le resultat si le rectangle trouvé est plus grand que la marge donnée
    if max_val > threshold:
        return centers

    # Sinon retourne un espace pour terminé la commande 'Tap()'
    else:
        return NOTHING


def Exploration():

    # Envoye les explorateur explorer la map
    cord_text = ImgRecherche('explorer.png', MARGE_MOY)
    cord_bat = ImgRecherche('batExplorer.png', MARGE_MOY)
    if cord_text != NOTHING and cord_bat != NOTHING:
        print('Exploration en cours')
        Tap(cord_bat)
        time.sleep(TRAPIDE)
        Tap(ImgRecherche('loupe.png', 0.98))
        time.sleep(TRAPIDE)
        cord_btn = ImgRecherche('btnExplorer.png', 0.98)

        # Controle pour les boutons 'explorer'
        if cord_btn != NOTHING:
            Tap(cord_btn)
            time.sleep(TLENT)
            Tap(ImgRecherche('btnExplorer.png', 0.95))
            time.sleep(TRAPIDE)
            Tap(ImgRecherche('btnEnvoyer.png', 0.94))
            time.sleep(TRAPIDE)
            Tap(ImgRecherche('btnRentre.png', 0.98))
            print('Exploration terminé, Retour à la base')
            time.sleep(TLENT)

        # Sinon quitte la page si il le faut et passe
        else:
            Tap(ImgRecherche('btnFermer.png', MARGE_P))
            time.sleep(TRAPIDE)

    # Sinon controle si le joueur est a la base et rentre si necessaire
    else:
        Tap(ImgRecherche('btnRentre.png', 0.98))
        print('Aucune exploration disponible')



def Collecte():

    # Collecte le maîs
    cord_mais = ImgRecherche('mais.png', MARGE_MOY)
    if cord_mais != NOTHING:
        Tap(cord_mais)
        print('Collection maîs')
        time.sleep(TRAPIDE)

    # Collecte le bois
    cord_bois = ImgRecherche('bois.png', MARGE_MOY)
    if cord_bois != NOTHING:
        Tap(cord_bois)
        print('Collection bois')
        time.sleep(TRAPIDE)

    # Collecte la pierre
    cord_pierre = ImgRecherche('pierre.png', MARGE_MOY)
    if cord_pierre != NOTHING:
        Tap(cord_pierre)
        print('Collection pierre')
        time.sleep(TRAPIDE)

    # Collecte l'or
    cord_or = ImgRecherche('or.png', MARGE_MOY)
    if cord_or != NOTHING:
        Tap(cord_or)
        print('Collection or')
        time.sleep(TRAPIDE)

    # Sinon ecrit dans le cmd
    else:
        print('Aucune collection disponible')


def Infenterie():

    # Collecte et relance la formation de l'infenteries
    cord_pause = ImgRecherche('pause.png', 0.45)
    cord_bat = ImgRecherche('batInfenterie2.png', MARGE_MOY)
    cord_collect = ImgRecherche('archer.png', 0.98)
    if cord_pause != NOTHING and cord_bat != NOTHING or cord_collect != NOTHING:

        # Si l'infenteries est pretes, collecte avant de relancer
        if cord_collect != NOTHING:
            Tap(cord_collect)

        time.sleep(TRAPIDE)
        Tap(cord_bat)
        time.sleep(TRAPIDE)
        Tap(ImgRecherche('formationInfenterie.png', MARGE_P))
        time.sleep(TLENT)
        Tap(ImgRecherche('train.png', MARGE_P))
        print('Formation infenterie lancée !')
        time.sleep(TRAPIDE)

    # Quitte si une fenetre existe sinon passe
    else:
        print('Infenterie déjà en formation')
        Tap(ImgRecherche('btnFermer.png', MARGE_P))
        time.sleep(TRAPIDE)


def Archer():

    # Collecte et relance la formation des archers
    cord_pause = ImgRecherche('pause.png', 0.45)
    cord_bat = ImgRecherche('batArcher2.png', MARGE_MOY)
    cord_collect = ImgRecherche('archer.png', 0.98)
    if cord_pause != NOTHING and cord_bat != NOTHING or cord_collect != NOTHING:

        # Si les archers sont prets, collecte avant de relancer
        if cord_collect != NOTHING:
            Tap(cord_collect)
            time.sleep(TRAPIDE)

        Tap(cord_bat)
        time.sleep(TRAPIDE)
        Tap(ImgRecherche('formationArcher.png', MARGE_P))
        time.sleep(TLENT)
        Tap(ImgRecherche('train.png', MARGE_P))
        print('Formation archer lancée !')
        time.sleep(TRAPIDE)

    # Quitte si une fenetre existe sinon passe
    else:
        print('Archer déjà en formation')
        Tap(ImgRecherche('btnFermer.png', MARGE_P))
        time.sleep(TRAPIDE)


def Recrute():

    # Entre dans la taverne
    cord_recrute = ImgRecherche('recruter.png', MARGE_MOY)
    time.sleep(TRAPIDE)
    cord_bat = ImgRecherche('batRecruter.png', MARGE_MOY)
    if cord_recrute != NOTHING and cord_bat != NOTHING:
        Tap(cord_bat)
        time.sleep(TRAPIDE)
        Tap(ImgRecherche('btnRecruter.png', MARGE_MOY))
        time.sleep(TRAPIDE)

        # Ouverture de coffres
        cord_ouvrir = ImgRecherche('btnOuvrir.png', MARGE_P)
        if cord_ouvrir != NOTHING:
            Tap(cord_ouvrir)
            print('Ouverture de coffre !')
            time.sleep(TLENT)
            Tap(ImgRecherche('btnConfirmer.png', MARGE_P))
            time.sleep(TRAPIDE)

    # Quitter la page des coffres
    else:
        Tap(ImgRecherche('btnFlecheRetour.png', MARGE_P))
        Tap(ImgRecherche('btnConfirmer.png', MARGE_P))
        time.sleep(TRAPIDE)
        print('Aucun coffre disponible !')


def AideAlly():

    # Aide des membres de l'alliance
    cord_help = ImgRecherche('aideAlly.png', MARGE_P)
    if cord_help != NOTHING:
        Tap(cord_help)
        print('Alliance aidée')
        time.sleep(TRAPIDE)
    else:
        print('Aucune aide alliance disponible')



def Alliance():
    Tap(ImgRecherche('alliance.png', MARGE_P))

    # Dons pour la technologie d'alliance
    cord_tech = ImgRecherche('technologie.png', 0.98)
    if cord_tech != NOTHING:
        Tap(cord_tech)
        time.sleep(TRAPIDE)
        Tap(ImgRecherche('recommand.png', MARGE_P))
        time.sleep(TRAPIDE)
        cord_donner = ImgRecherche('donner.png', MARGE_P)
        while cord_donner != NOTHING:
            cord_donner = ImgRecherche('donner.png', MARGE_P)
            Tap(cord_donner)

    # Recolte des cadeaux d'alliance
    time.sleep(TRAPIDE)
    cord_cadeau = ImgRecherche('cadeau.png', 0.98)
    if cord_cadeau != NOTHING:
        Tap(cord_cadeau)
        time.sleep(TRAPIDE)
        cord_reclamer = ImgRecherche('reclamer.png', MARGE_P)
        if cord_reclamer != NOTHING:
            Tap(ImgRecherche('toutObtenir.png', MARGE_P))
            time.sleep(TRAPIDE)
    Tap(ImgRecherche('btnFermer.png', MARGE_P))