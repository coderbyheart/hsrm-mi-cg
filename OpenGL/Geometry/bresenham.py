from tkinter import *
import sys


WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 10 # half of point size (must be integer)
HPSIZE2 = HPSIZE * 2
FCOLOR = "#AAAAAA" # fill color
PCOLOR = "#AA00AA"
BCOLOR = "#000000" # boundary color

pointList = []   # list of points
elementList = [] # list of elements (used by Canvas.delete(...))


def drawGrid(s):
    """ draw a rectangular grid """
    for i in range(0,WIDTH,s):
        element = can.create_line(i,0,i,HEIGHT)
    for i in range(0,HEIGHT,s):
        element = can.create_line(0,i,WIDTH,i)


def drawPoints():
    """ draw points """
    for p in pointList:
        element = can.create_rectangle(p[0]-HPSIZE, p[1]-HPSIZE,
                                       p[0]+HPSIZE, p[1]+HPSIZE,
                                       fill=FCOLOR, outline=BCOLOR)
        elementList.append(element)    


def drawLines():
    """ draw lines """
    for line in zip(pointList[::2],pointList[1::2]):
        drawBresenhamLine(line[0],line[1])
        element = can.create_line(line,width=1)
        elementList.append(element)    

def sgn(x):
    if x > 0: 
        return 1
    if x < 0:
        return -1
    return 0

def drawBresenhamLine(p,q):
    """ draw a line using bresenhams algorithm """
    x0 = int((p[0] - HPSIZE) / HPSIZE2)
    y0 = int((p[1] - HPSIZE) / HPSIZE2)
    x1 = int((q[0] - HPSIZE) / HPSIZE2)
    y1 = int((q[1] - HPSIZE) / HPSIZE2)
    
    # Entfernung
    dx = x1 - x0
    dy = y1 - y0
    
    # Absolutbeträge Distanzen
    adx = abs(dx)
    ady = abs(dy)
    # Signum Distanzen
    sdx = sgn(dx)
    sdy = sgn(dy)
 
    if adx > ady: # x ist schnelle Richtung
       # pd. ist Parallelschritt
       pdx = sdx
       pdy = 0
       # dd. ist Diagonalschritt
       ddx = sdx
       ddy = sdy
       # Fehlerschritte schnell, langsam 
       es  = ady
       el  = adx
    else: # y ist schnelle Richtung
        pdx = 0
        pdy = sdy
        ddx = sdx
        ddy = sdy
        es  = adx
        el  = ady
        
    x = x0
    y = y0
    addPixel(x, y)
    fehler = el/2
    for i in range(el):
        # Aktualisier Fehlerterm
        fehler = fehler - es
        if fehler < 0:
            # Fehlerterm wieder positiv (>=0) machen
            fehler = fehler + el 
            # Schritt in langsame Richtung
            # Diagonalschritt
            x = x + ddx
            y = y + ddy
        else:
            # Schritt in schnelle Richtung
            # Parallelschritt
            x = x + pdx
            y = y + pdy
        addPixel(x, y)
           
def addPixel(x, y):
       px = x * HPSIZE2 + HPSIZE
       py = y * HPSIZE2 + HPSIZE
       element = can.create_rectangle(px-HPSIZE, py-HPSIZE, px+HPSIZE, py+HPSIZE, fill=PCOLOR, outline=BCOLOR)
       elementList.append(element)

def drawBresenhamLine2(p,q):
    """ draw a line using bresenhams algorithm """
    HPSIZE2 = int(2*HPSIZE)
    x0 = int((p[0] - HPSIZE) / HPSIZE2)
    y0 = int((p[1] - HPSIZE) / HPSIZE2)
    x1 = int((q[0] - HPSIZE) / HPSIZE2)
    y1 = int((q[1] - HPSIZE) / HPSIZE2)
    
    dx =  abs(x1-x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1-y0)
    sy = 1 if y0 < y1 else -1 
    err = dx + dy
    
    while True:
        px = x0 * HPSIZE2 + HPSIZE
        py = y0 * HPSIZE2 + HPSIZE
        element = can.create_rectangle(px-HPSIZE, py-HPSIZE, px+HPSIZE, py+HPSIZE, fill=PCOLOR, outline=BCOLOR)
        elementList.append(element)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints()
    drawLines()

def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    # get point coordinates
    d = 2*HPSIZE
    p = [d/2+d*int(event.x/d), d/2+d*int(event.y/d)] 
    pointList.append(p)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print("draw lines using bresenhams algorithm")
       sys.exit(-1)

    # create main window
    mw = Tk()
    mw._root().wm_title("Line drawing using bresenhams algorithm")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>",mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left") 
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    drawGrid(2*HPSIZE)
    # start
    mw.mainloop()
    
