#!/usr/bin/python2

from Tkinter import *
from Canvas import *
import sys
from os import path
from PointTween import PointTween
from MorphDef import MorphDef
from time import sleep

WIDTH  = 801 # width of canvas
HEIGHT = 600 # height of canvas

HPSIZE = 10 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue

elementList = [] # list of elements (used by Canvas.delete(...))

duration = 2
nsteps = 100
dt = duration / float(100)

frame = 0

pointTweens = []
morphIters = []

def drawObjekts():
    """ draw polygon and points """
    dots = []
    for morphIter in morphIters:
        try:
            p = morphIter.next()
            x = p[0] * WIDTH
            y = HEIGHT - p[1] * HEIGHT
            dots.append((x, y))
        except StopIteration:
            pass
    if len(dots) > 0:
        can.delete(*elementList)
        del elementList[:]
        for dot in dots:
            elementList.append(can.create_oval(dot[0]-HPSIZE, dot[1]-HPSIZE, dot[0]+HPSIZE, dot[1]+HPSIZE, fill=CCOLOR, outline=CCOLOR))
        dots.append(dots[0])
    for p,q in zip(dots, dots[1:]):
        elementList.append(can.create_line(p[0], p[1], q[0], q[1], fill=CCOLOR))

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    global frame
    drawObjekts()
    can.update()
    frame += 1
    can.postscript(file = "%04d.ps" % frame)

def forward():
    global time, duration, pointTweens, morphIters, md

    pointTweens = []
    morphIters = []
    for morphDef in md.morphdef:
        pt = PointTween(morphDef[0], morphDef[1], nsteps)
        pointTweens.append(pt)
        morphIters.append(pt.__iter__())

    cstep = 0
    while(cstep < nsteps):
        cstep += 1
        draw()
        sleep(dt)


def backward():
    global time, duration, pointTweens, morphIters, md

    pointTweens = []
    morphIters = []
    for morphDef in md.morphdef:
        pt = PointTween(morphDef[1], morphDef[0], nsteps)
        pointTweens.append(pt)
        morphIters.append(pt.__iter__())
    
    cstep = 0
    while(cstep < nsteps):
        cstep += 1
        draw()
        sleep(dt)
    

if __name__ == "__main__":
    # check parameters
    if len(sys.argv) < 3:
       print("Usage: %s firstPolygon secondPolygon [nearest=False]" % path.basename(sys.argv[0]))
       sys.exit(-1)

    shapeA = [((float(x.strip().split(" ")[0]), float(x.strip().split(" ")[1]))) for x in file(sys.argv[1]).readlines()]
    shapeB = [((float(x.strip().split(" ")[0]), float(x.strip().split(" ")[1]))) for x in file(sys.argv[2]).readlines()]
    nearest = bool(sys.argv[3]) if len(sys.argv) == 4 else False

    md = MorphDef(shapeA, shapeB, nearest)

    # create main window
    mw = Tk()
    mw._root().wm_title("Morphing")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="backward", command=backward)
    bClear.pack(side="left")
    bClear = Button(cFr, text="forward", command=forward)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()
    forward()
    draw()
    
    # start
    mw.mainloop()
    
