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

colors = [
          

"#f1eef6",
"#d4b9da",
"#c994c7",
"#df65b0",
"#e7298a",
"#ce1256",
"#91003f",

          
"#ffffb2",
"#fed976",
"#feb24c",
"#fd8d3c",
"#f03b20",
"#bd0026",

"#7fc97f",
"#beaed4",
"#fdc086",
"#ffff99",
"#386cb0",
"#f0027f",
"#bf5b17",
"#666666",
"#a6cee3",
"#1f78b4",
"#b2df8a",
"#33a02c",
"#fb9a99",
"#e31a1c",
"#fdbf6f",
"#ff7f00",
"#cab2d6",
"#6a3d9a",
"#ffff99",
"#b15928",]
subPointList = {}

def drawPoints():
    """ draw (control-)points """
    return
    for p in pointList:
	element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                  p[0]+HPSIZE, p[1]+HPSIZE,
                                  fill=CCOLOR, outline=CCOLOR)
	elementList.append(element)    


def drawPolygon():
    """ draw (control-)polygon conecting (control-)points """
    return
    if len(pointList) > 1:
        for i in range(len(pointList)-1):
            element = can.create_line(pointList[i][0], pointList[i][1],
                                      pointList[i+1][0], pointList[i+1][1],
                                      fill=CCOLOR)
            elementList.append(element)

def drawBezierCurve():
    """ draw bezier curve defined by (control-)points """
    drawCasteljau(pointList)

def drawCasteljau(points, level = 0):
    N = len(points) 
    if N < 3:
        return
    for i in range(1, N - 1):
        lcolor = colors[level]
        if lcolor not in subPointList:
            subPointList[lcolor] = {}
        subPointList[lcolor][level] = []
        t = float(i)/float(N - 1)
        for (i,p) in enumerate(points):
            if i == N - 1:
                break
            n = points[i+1]
            px = p[0] + t*(n[0] - p[0])
            py = p[1] + t*(n[1] - p[1])
            subPointList[lcolor][level].append((px, py))
        drawCasteljau(subPointList[lcolor][level], level + 1)

    for color in subPointList:
        for level in subPointList[color]:
            for (i,p) in enumerate(subPointList[color][level]):
                element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                      p[0]+HPSIZE, p[1]+HPSIZE,
                                      fill=color, outline=color)
                elementList.append(element)
                if i > 0:
                    element = can.create_line(subPointList[color][level][i][0], subPointList[color][level][i][1],
                                          subPointList[color][level][i-1][0], subPointList[color][level][i-1][1],
                                          fill=color)
                    elementList.append(element)
            
    #print "drawBezierCurve() not yet implemented..."
    #print "curve should have color: ", BCOLOR, " and width: ", BWIDTH


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
    drawPolygon()
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
    

