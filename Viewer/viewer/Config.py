# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
'''
Enthält die aktuelle Konfiguration des Viewers

@author: Markus Tacker <m@tacker.org>
'''
class Config(object):
    ".obj-Datei die das angezeigte Model definiert"
    #pointsfile = 'models/squirrel/squirrel-textured.obj'
    pointsfile = 'models/simple/strange-box.obj'
    
    # Drehwinkel Modell
    "Drehwinkel Modell: x"
    xAngle = 0.0
    "Drehwinkel Modell: y"
    yAngle = 0.0
    "Drehwinkel Modell: z"
    zAngle = 0.0

    # Position Modell
    "Position Modell: x"
    xPosModel = 0.0
    "Position Modell: y"
    yPosModel = 0.0
    "Position Modell: z"
    zPosModel = 0.0

    # Position Kamera
    "Postion Kamera: x"
    xPosCamera = 0.0
    "Postion Kamera: y"
    yPosCamera = 0.0
    "Postion Kamera: z"
    zPosCamera = 0.0
    
    # Stati der Maus
    "Maustaste gedrückt (irgendeine)"
    mousePressed = False
    "Linke Maustaste gedrückt"
    leftMousePressed = False
    "Mittlere Maustaste gedrückt"
    middleMousePressed = False
    "Rechte Maustaste gedrückt"
    rightMousePressed = False
    
    "Koordinatensystem anzeigen"
    showModelCross = False
    
    "Hintergrundfarbe"
    bgcolor = (0.6, 0.6, 0.6, 0.0)
    
    "Farbe des Models"
    mcolor = (0.0, 1.0, 0.0, 0.0)
    
    "Standard-Fensterbreite"
    windowWidth = 500
    
    "Standard-Fensterhöhe"
    windowHeight = 500

    # Beleuchtung
    "Position des Lichtes: x"
    xPosLight = 0.01
    "Position des Lichtes: y"
    yPosLight = 10.0
    "Position des Lichtes: z"
    zPosLight = 0.01

    # Letzte Mausposition
    "Letzte Mausposition: X"    
    mouseLastX = None
    "Letzte Mausposition: Y"
    mouseLastY = None
    
    "Textur verwende"
    useTexture = True

