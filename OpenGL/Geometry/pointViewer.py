from tkinter import *
import sys
from PointCloud import PointCloud
from HomMatrix3 import HomMatrix3, FrustrumMatrix
from ProgressMeter import Meter

WIDTH  = 800 # width of canvas
HEIGHT = 800 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

pointList = [] # list of points (used by Canvas.delete(...))
#pc = PointCloud().readRaw('data/elephant_points.raw').normalized()
#pc = PointCloud().readRaw('data/bunny_points.raw').normalized()
#pc = PointCloud().readRaw('data/cow_points.raw').normalized()
#pc = PointCloud().readRaw('data/pyramide_points.raw').normalized()
#pc = PointCloud().readRaw('data/wuerfel5-allneg_points.raw').normalized()
pc = PointCloud().readRaw('data/cube_points.raw').normalized()

xAngle = 0
yAngle = 0
zAngle = 0

## Sichtvolumen Kamera
fm = FrustrumMatrix(-2, 2, -2, 2, -1, 10)
cm = HomMatrix3()
cm.setTranslation(0,0,-3)

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    """ draw points """
    global pc
    
    border = 20
    
    numpoints = pc.getNumPoints()
    i = 0
    for point in pc:
        i += 1
        
        # Punkte durch die Frustrum-Matrix jagen
        point = cm * point
        point = (fm * point).normalized()
        
        x = border + ((point.x + 1) / 2) * (WIDTH - 2 * border)
        y = border + ((-point.y + 1) / 2)* (HEIGHT - 2 * border)

        #z = point.z * HEIGHT
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE,
                           fill=COLOR, outline=COLOR)
        pointList.insert(0,p)
        
        m.set(i / numpoints)

def rotYp():
    """ rotate counterclockwise around y axis """
    global pointList
    pc.rotateY(-10)
    can.delete(*pointList)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    global pointList
    pc.rotateY(10)
    can.delete(*pointList)
    draw()
    
def rotX(angle):
    "Auf der X-Achse drehen"
    global pointList, xAngle
    angle = int(angle)
    pc.rotateX(-(angle - xAngle))
    xAngle = angle
    can.delete(*pointList)
    draw()

def rotY(angle):
    "Auf der Y-Achse drehen"
    global pointList, yAngle
    angle = int(angle)
    pc.rotateY(-(angle - yAngle))
    yAngle = angle
    can.delete(*pointList)
    draw()
    
def rotZ(angle):
    "Auf der Z-Achse drehen"
    global pointList, zAngle
    angle = int(angle)
    pc.rotateZ(-(angle - zAngle))
    zAngle = angle
    can.delete(*pointList)
    draw()

def setCameraZ(pos):
    global cm
    cm.setTranslation(0,0,float(pos))
    can.delete(*pointList)
    draw()
    
def setCameraN(N):
    global fm
    fm = FrustrumMatrix(fm.xl, fm.xr, fm.yb, fm.yt, int(N), fm.F)
    can.delete(*pointList)
    draw()
    
def setCameraF(F):
    global fm
    fm = FrustrumMatrix(fm.xl, fm.xr, fm.yb, fm.yt, fm.N, int(F))
    can.delete(*pointList)
    draw()
    
def setCameraXL(xl):
    global fm
    fm = FrustrumMatrix(int(xl), fm.xr, fm.yb, fm.yt, fm.N, fm.F)
    can.delete(*pointList)
    draw()
    
def setCameraXR(xr):
    global fm
    fm = FrustrumMatrix(fm.xl, int(xr), fm.yb, fm.yt, fm.N, fm.F)
    can.delete(*pointList)
    draw()
    
def setCameraYB(yb):
    global fm
    fm = FrustrumMatrix(fm.xl, fm.xr, int(yb), fm.yt, fm.N, fm.F)
    can.delete(*pointList)
    draw()

def setCameraYT(yt):
    global fm
    fm = FrustrumMatrix(fm.xl, fm.xr, fm.yb, int(yt), fm.N, fm.F)
    can.delete(*pointList)
    draw()

if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print("pointViewerTemplate.py")
       sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    can = Canvas(mw, width=WIDTH, height=HEIGHT)
    can.grid(column=0, row=0, columnspan=3)
    
    m = Meter(mw, relief='ridge', bd=3, width=WIDTH)
    m.grid(column=0, row=1, columnspan=3)
    
    if pc.getNumPoints() < 1000:
        xs = Scale(mw, label="Drehung auf der X-Achse", orient=HORIZONTAL, to=360, length=200, command=rotX)
        xs.grid(column=0, row=2)
        ys = Scale(mw, label="Drehung auf der Y-Achse", orient=HORIZONTAL, to=360, length=200, command=rotY)
        ys.grid(column=0, row=3)
        zs = Scale(mw, label="Drehung auf der Z-Achse", orient=HORIZONTAL, to=360, length=200, command=rotZ)
        zs.grid(column=0, row=4)
    else:
        bRotYn = Button(mw, text="<-", command=rotYn)
        bRotYn.grid(column=0, row=2)
        bRotYp = Button(mw, text="->", command=rotYp)
        bRotYp.grid(column=0, row=2)
        
    cz = Scale(mw, label="Z-Position der Kamera", orient=HORIZONTAL, from_=-2, to=-10, length=200, command=setCameraZ)
    cz.set(-3)
    cz.grid(column=1, row=2)
    
    cxl = Scale(mw, label="Kamera links oben (X)", orient=HORIZONTAL, from_=-20, to=20, length=200, command=setCameraXL)
    cxl.set(-2)
    cxl.grid(column=1, row=3)
    cyt = Scale(mw, label="Kamera links oben (Y)", orient=HORIZONTAL, from_=-20, to=20, length=200, command=setCameraYT)
    cyt.set(2)
    cyt.grid(column=2, row=3)
    cxr = Scale(mw, label="Kamera rechts unten (X)", orient=HORIZONTAL, from_=-20, to=20, length=200, command=setCameraXR)
    cxr.set(2)
    cxr.grid(column=1, row=4)
    cyb = Scale(mw, label="Kamera rechts unten (Y)", orient=HORIZONTAL, from_=-20, to=20, length=200, command=setCameraYB)
    cyb.set(-2)
    cyb.grid(column=2, row=4)
    
    cn = Scale(mw, label="NEAR", orient=HORIZONTAL, from_=-20, to=20, length=200, command=setCameraN)
    cn.set(-1)
    cn.grid(column=1, row=5)
    cf = Scale(mw, label="FAR", orient=HORIZONTAL, from_=-20, to=20, length=200, command=setCameraF)
    cf.set(10)
    cf.grid(column=2, row=5)
    
    bExit = Button(mw, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.grid(column=2, row=2)
    
    draw()
    
    # start
    mw.mainloop()
    
    
    
