from Tkinter import *
from Canvas import *
import sys

WIDTH  = 1000 # width of canvas
HEIGHT = 1000 # height of canvas

HPSIZE = 1 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue (color of control-points and polygon)

BCOLOR = "#000000" # black (color of bezier curve)
BWIDTH = 4 # width of bezier curve

pointList = []   # list of (control-)points
elementList = [] # list of elements (used by Canvas.delete(...))

def drawPoints(pointList, color=None):
    """ draw (control-)points """
    lcolor = CCOLOR if color == None else color
    for p in pointList:
	element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                  p[0]+HPSIZE, p[1]+HPSIZE,
                                  fill=lcolor, outline=lcolor)
	elementList.append(element)    


def drawPolygon(pointList, color=None):
    """ draw (control-)polygon conecting (control-)points """
    lcolor = CCOLOR if color == None else color
    if len(pointList) > 1:
        for i in range(len(pointList)-1):
            element = can.create_line(pointList[i][0], pointList[i][1],
                                      pointList[i+1][0], pointList[i+1][1],
                                      fill=lcolor)
            elementList.append(element)

def drawBezierCurve():
    """ draw bezier curve defined by (control-)points """
    if len(pointList) < 3:
        return
    bezierPoints = []
    bezierPoints.append(pointList[0])
    # Anzahl der Unterteilungen
    N = 100
    for i in range(1, N + 1):
        t = float(i)/float(N + 1)
        p = casteljau(pointList, t)
        bezierPoints.append(p)
    bezierPoints.append(pointList[-1])
    drawPoints(bezierPoints, "#91003f")
    drawPolygon(bezierPoints, "#91003f")

def casteljau(points, t):
    "Berechnet den Punkt auf der Kurve an der Stelle t"
    numPoints = len(points)
    if (numPoints == 1):
        return points[0]
    newPoints = []
    pairs = zip(points[:-1], points[1:])
    for (p,n) in pairs:
        px = p[0] + t*(n[0] - p[0])
        py = p[1] + t*(n[1] - p[1])
        newPoints.append([px, py])
    return casteljau(newPoints, t)

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints(pointList)
    drawPolygon(pointList)
    drawBezierCurve()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]

def mouseEvent(event):
    """ process mouse events """
    print "left mouse button clicked at ", event.x, event.y
    pointList.append([event.x, event.y])
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT, background="white")
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
    
    pointList.append([WIDTH * 0.0625, HEIGHT * 0.0625])
    pointList.append([WIDTH * 0.9375, HEIGHT * 0.0625])
    pointList.append([WIDTH * 0.9375, HEIGHT * 0.9375])
    pointList.append([WIDTH * 0.0625, HEIGHT * 0.9375])
    pointList.append([WIDTH * 0.0625, HEIGHT * 0.25])
    pointList.append([WIDTH * 0.625, HEIGHT * 0.25])
    pointList.append([WIDTH * 0.625, HEIGHT * 0.625])
    pointList.append([WIDTH * 0.375, HEIGHT * 0.625])
    
    draw()

    # start
    mw.mainloop()
    

