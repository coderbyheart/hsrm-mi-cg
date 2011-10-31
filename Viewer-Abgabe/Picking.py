import Raytracing
from Quaternion import *
from Transformation import *
from Vec import Vec
import math

def pick(cursorX, cursorY, worldTrans, model, doProjectionMatrix):
   """ Picking """
  
   x, y = cursorX, cursorY

   # Picking starten
   glSelectBuffer (512)
   glRenderMode (GL_SELECT);

   #Projection auf geklickten bereich beschraenken.
   glMatrixMode (GL_PROJECTION)
   glPushMatrix ()
   glLoadIdentity ()
   
   viewport = glGetIntegerv(GL_VIEWPORT);
   gluPickMatrix(x,viewport[3]-y, 5,5, viewport);
   doProjectionMatrix()
   proMat=glGetDouble(GL_PROJECTION_MATRIX)
   
   #picking Object erstellen
   glInitNames()
   glMatrixMode (GL_MODELVIEW)
   glPushName(0)
   glLoadIdentity()
   worldTrans.openGLLookAt()
   model.model()
   modMat=glGetDouble(GL_MODELVIEW_MATRIX)
   glPopName(0)

   #Picking beenden und treffer holen
   hits = glRenderMode (GL_RENDER)

   #Original ansicht wieder herstellen
   glMatrixMode (GL_PROJECTION)
   glPopMatrix ()
   glMatrixMode(GL_MODELVIEW);
   glFlush ()

     
   # treffer  verarbeiten
   if len(hits)>0:
      #nahesten hit holen
      hit=reduce(minHits, hits)
      distance=min(hits[0].near,hit.far)
      #hitPunkt
      point =Vec(gluUnProject(x,viewport[3]-y,distance,modMat,proMat,viewport))
      #facet holen durch raytracing
      facet= Raytracing.doRaytracing(x,y, distance ,proMat, modMat, viewport, model, hit)
      #hitRay erzeugen
      near = Vec(gluUnProject(x, y, 0,            modMat, proMat, viewport))
      far  = Vec(gluUnProject(x, y, 1,            modMat, proMat, viewport))
      ray =  far - near
      
     
      if facet is not None:
         vortex= [model.v[face[0]] for face in facet]
         
      #gepickten Punkt centrieren
      centerFacet( point,model, worldTrans,ray, facet)
     
      # returnt gepickten bereich-name
      return model.getName(hit.names[0])

     
def minHits(hit0, hit1):
   """ holt vordesten hit vom Picking """
   if hit0.near < hit1.near:
      return hit0
   return hit1





def centerFacet( pickPoint, model, worldTrans,ray, facet=None):
        """ Centriert Kamera auf gepickten punkt """
        normale=Vec(0,0,0)
        point=Vec(0,0,0)
        points=[]
        # wenn facet gefunden wurde
        if facet is not None:
           for face in facet:
               #normale+=Vec(model.vn[face[2]])
               point+=Vec(model.v[face[0]])
               points.append(Vec(model.v[face[0]]) )
           #normale=normale.normalized()
           #Senkrechter Vecktor zum Dreick bestimmen
           normale=calcSenkrecht(points, ray)
           #Punkt auf Uniformgroesse skalieren
           point=point/3.0
           point = point - (  Vec(model.box.center) )
           point= point / max(model.box.length)
        else:
           #Falls kein Facet geliefert wurde, Senkrecht zu "PickPunkt zum Mittelpunkt des Models" schauen.
           point=pickPoint
           point = point - (  Vec(model.box.center) )
           point= point / max(model.box.length)
           normale= point.normalized()

        #HitPunkt mit ModelTransformation transformieren
        mT=model.modTrans
        point=mT.rotation.rotateVec(point)
        point = point *mT.scalar
        point = point + mT.translation
        normale=mT.rotation.rotateVec(normale)
        
        
        """ #idle model
        dirBlick=-worldTrans.directionZ
        winkel=dirBlick.winkel(normale)
        achse= dirBlick%normale
        quat=rotationQuat(winkel, -achse.normalized() )

        
        point = quat.rotateVec(-point)
        point = point + worldTrans.center # zentriert auf aktuellen blickpunkt
        point =point - worldTrans.getDisAtT(0.8)
        model.initIdle(rotation=quat, translation= point , scale=1 )
        #"""

       
        #ZielTransformation bestimmen
        
        winkel=normale.winkel(worldTrans.startVec)
        achse= worldTrans.startVec%normale
        rotattion=rotationQuat(winkel, achse.normalized() )
        #Idle Starten
        worldTrans.initIdle(point, rotattion, 1*mT.scalar)



def calcSenkrecht(points, ray):
    """ berechnet Senkrechte zum hit-Dreieck """
    v1=Vec(points[0])-Vec(points[1])
    v2=Vec(points[0])-Vec(points[2])
    senk=(v1%v2).normalized()
    winkel=senk.winkel(ray)
    if winkel<90:
        return -senk
    else:
        return senk
    
    
    
    
if __name__ == "__main__":
   import newGoogleBody
   newGoogleBody.main()
