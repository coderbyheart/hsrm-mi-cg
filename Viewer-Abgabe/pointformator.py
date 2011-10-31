
import sys

def readPoints(fileName):
    """ obj-File Laden """
    fileobj=open(fileName)
    v=[]
    vt=[]
    vn=[]
    f=[]
    name={}
    n="default"
    name[n]=[]
    for line in fileobj:
        line=line.replace("\r", "")
        line=line.replace(" \n", "")
        line=line.replace("\n", "")
        line=line.replace("   ", " ")
        line=line.replace("  ", " ")
        split=line.split(" ")
        if split[0] == 'v':
            v.append( [float(x) for x in split[1:] if x!=""])
        if split[0] == 'vt':
            vt.append( [float(x) for x in split[1:] if x!=""])
        if split[0] == 'g':
            n=" ".join(split[1:])
            if n not in name.keys():
                name[n]=[]
        if split[0] == 'vn':
            vn.append( [float(x) for x in split[1:] if x!=""])
        if split[0] == 'f':
            split=[ x.split("/") for x in split[1:] if x!=""]
            zz=[]
            for y in split:
                z=[]
                for x in y:
                    if x == "":
                        x=0
                    z.append(int(x)-1)
                zz.append(z)
            name[n].append(zz)
  
    return v, vt, vn, name


def getpoints(fileName):
    """ liefert Facet, BoundingBox"""
    v, vt, vn, n=readPoints(fileName)
    bbox=calcBoundingbox(v)
    return (bbox, v, vt, vn, n)
   

class Boundingbox:
    """ Boundingbox"""
    def __init__(self, vmin, vmax):
        self.vmin=vmin
        self.vmax=vmax
        self.center=[ (vmin[i] + vmax[i]) /2.0 for i in range(len(vmin))]
        self.length=[ (vmax[i] - vmin[i])      for i in range(len(vmin))]
        
       
        

def calcBoundingbox(points):
    """ berechnet boundingbox"""
    x=[vec[0] for vec in points]
    y=[vec[1] for vec in points]
    z=[vec[2] for vec in points]
    vmax=[max(x), max(y), max(z)]
    vmin=[min(x), min(y), min(z)]    
    return Boundingbox(vmin, vmax  )




