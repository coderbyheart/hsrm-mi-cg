import math
from Vec import Vec
from Quaternion import *
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class WorldTrans():
    """ Transformation der Welt (LookAt) """
    
    def __init__(self, eye, center, up):
        """init"""
        self.eye=Vec(eye)
        self.center=Vec(center)
        self.up=Vec(up).normalized()
        self.calcDirections()
        self.idle=False
        self.startVec=Vec(0,0,-3)

    def calcDirections(self):
        """ berechnet Koordinaten-Vektoren der Kamera"""
        self.directionZ = (self.center - self.eye).normalized()
        self.directionX = (self.up % self.directionZ ).normalized()
        self.directionY = (self.directionZ % self.directionX ).normalized()
        

   
    
    def openGLLookAt(self):
        """ setzt gluLookAt """
        ex,ey,ez = self.eye
        cx,cy,cz = self.center
        ux,uy,uz = self.up
        gluLookAt(ex,ey,ez, cx,cy,cz, ux,uy,uz)
        
    def translate(self, translation):
        """ verschiebt Kamera"""
        self.eye+=translation
        self.center+=translation

    def zoom(self, zDistance):
        """ entfernung vonder Kamera um blickpunkt"""
        self.eye += (self.directionZ * zDistance)

    def setEyeCenter(self,eye,center):
        """ setzt neues Eye, Center(Blickpunkt) """
        self.eye=eye
        self.center=center
        self.calcDirections()
        
    
    def rotate(self, rotation):
        """ Rotiert Auge um das Center """
        eye = self.eye - self.center
        rotatedOrigin = rotation.rotateVec(eye)
        self.eye = rotatedOrigin + self.center
        self.calcDirections()

    def initIdle(self, targetCenter=Vec(0,0,0), targetRot=rotationQuat(0, Vec(0,0,1)), targetDis=3):
        """ initiiert Idle"""
        self.t=time.time()

        self.targetCenter=targetCenter
        self.targetRot=targetRot
        self.targetDis=targetDis
        self.oldCenter=self.center

        self.oldDis=(self.center-self.eye).length()
        self.oldEye=self.eye-self.center
        winkel=self.oldEye.winkel(self.startVec)
        if winkel == 0:
            achse = self.startVec
        else:
            achse=self.oldEye % self.startVec
        
        self.oldRotate=rotationQuat(-winkel, achse)
        self.idle=True


    def idleWorld(self):
        """ Idle Kamera"""
        t=time.time() - self.t
        if t>1.0:
            t=1.0
        

        newCenter=self.oldCenter * (1-t) + self.targetCenter * t
        newRot=self.oldRotate.slerp(self.targetRot, t)
        
        newEye= newRot.rotateVec(self.startVec)
        newDis=self.oldDis*(1-t) + self.targetDis*t
        newEye=newEye.normalized()*newDis
        
        self.setEyeCenter(newEye+newCenter,newCenter)
        if t>=1.0:
            self.idle=False

  
        





class ModTrans():
    """ Transformation des Models"""
    
    def __init__(self, rotation=rotationQuat(0, Vec(0,0,1)), translation=Vec(0,0,0), scalar=1.0):
        """ init"""
        self.rotation=rotation
        self.translation=translation
        self.scalar=scalar
       

        

    def getRotation(self):
        """ liefert Rotation"""
        return self.rotation

    def rotate(self, rotation):
        """ rotiert Objekt"""
        self.rotation = rotation * self.rotation

    def translate(self, translation):
        """ translatiert (verschiebt) Model """
        self.translation+=translation
       

    def scale(self, scalar):
        """ skaliert Model"""
        if self.scalar+scalar>0:
            self.scalar+=scalar

    def interpolate(self, targetModTrans, t):
        """SLERP, interpoliert von einer ModelTransformation zu einer anderen"""
        try:
            rotation=self.rotation.slerp( targetModTrans.rotation, t )
        except:
            rotation=targetModTrans.rotation
        position= self.translation*(1-t) + targetModTrans.translation * t
        scalar=self.scalar*(1-t)+targetModTrans.scalar*t
        return ModTrans(rotation, position, scalar)

    def openGLTransform(self):
        """ Transformiert Model"""
        tx,ty,tz=self.translation
        glTranslate(tx,ty,tz)
        glScale(self.scalar,self.scalar,self.scalar)
        glMultMatrixd(self.getRotation().rotationsmatrix())




if __name__ == "__main__":
   import newGoogleBody
   newGoogleBody.main()

