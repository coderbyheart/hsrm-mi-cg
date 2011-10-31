# -*- coding: utf-8 -*-

import pointformator
import time
from Transformation import *
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Quaternion import rotationQuat
class Model:

    def __init__(self, file_name):
        """init"""
        
        self.modTrans= ModTrans()
        box, v, vt, vn, nameFacet = pointformator.getpoints(file_name)
        self.box=box
        self.v=v
        self.vn=vn
        self.vt=vt
        self.nameFacet=nameFacet
        self.idle=False
        self.nameList=nameFacet.keys()
        self.color=(0,0,1)
        self.triangleLen=self.calcScaleFactor()
        self.loadTexture("model/squirrel/unnamed_object1_auv.bmp")
        #self.loadTexture("model/s2/s2.bmp")
       

    def doMaterial(self):
        glMaterialfv(GL_FRONT, GL_SPECULAR,  [0.5,0.5,0.5,1]);
        glMaterialf(GL_FRONT, GL_SHININESS, 5);
        glMaterialfv(GL_FRONT, GL_AMBIENT,   [0.2,0.2,0.2,1]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE,   [0.4,0.4,0.4,1]);


    def loadTexture(self, file_Name):
            """Texture Laden """
            #Bild Laden
            image = Image.open(file_Name)
            
            twidth, theight = image.size
            image_data = image.tostring("raw","RGB",0,-1)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            gluBuild2DMipmaps( GL_TEXTURE_2D, 3, twidth, theight,  GL_RGB, GL_UNSIGNED_BYTE, image_data )
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, twidth, theight, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
 
            self.texture=texture



    def calcScaleFactor(model):
        """ liefert Anaeherung an triangle groesse"""
        anzahl=len(model.allFace())
        lx,ly,lz=model.box.length
        oberflaesche=lx*ly*2+lx*lz*2+ly*lz*2
        triangleFlaesche=float(oberflaesche)/float(anzahl)
        triangleFlaesche=math.sqrt(triangleFlaesche)
        
        return triangleFlaesche
   


    def allFace(self):
        """ liefert Liste mit allen Facet """
        f=[]
        for face in self.nameFacet.values():
            f+=face
        return f

          

    def getName(self, number):
        """ liefert picking-Name zu Nummer"""
        return self.nameList[number]


    

    def createDisplaylist(self):
       """ baut Model-Liste """
       modelList = glGenLists(1)
       glNewList(modelList, GL_COMPILE)
       for nameNumber in range(len(self.nameList)):
           glLoadName(nameNumber)
           glBegin(GL_TRIANGLES)
           facet=self.nameFacet[self.nameList[nameNumber]]
           for triangle in facet:
               for i in triangle:
                glNormal3fv(self.vn[i[2]])
                if i[1] >=0:
                    glTexCoord2dv( self.vt[i[1]])
                glVertex3fv(self.v[i[0]])
           glEnd()
       glEndList()
       self.modelList=modelList


  

    def shadow(self, light):
        """schatten des Models"""
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        xLight, yLight, zLight, point = light
        p=[1.0, 0, 0, 0, 0, 1.0, 0, -1.0/yLight, 0, 0, 1.0, 0, 0, 0, 0, 0]
        
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        
        cy=self.box.length[1]/max(self.box.length)
        cy=cy/-2.0
        my= self.modTrans.translation[1]
        yy=0
        if cy+my<0:
            yy=cy+my
        glTranslatef(xLight, yLight+yy, zLight)
        glMultMatrixf(p)
        glTranslatef(-xLight, -yLight-yy, -zLight)
        
       
        glEnable (GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0,0,0, 0.2)
        self.model()
        glDisable (GL_BLEND)
        glPopMatrix()
        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
     
    def uniform(self):
        """ bereinheitlicht ModelTransformation """
        cx,cy,cz = self.box.center
        lx,ly,lz = self.box.length
        scale= 1.0/ max(lx,ly,lz)
        glScale(scale,scale,scale)
        glTranslate(-cx,-cy,-cz)
        

   

   

    def initIdle(self, rotation=None, translation=None, scale=None):
        """ setzt Idle-StartWerte """
        self.originalModelTrans = self.modTrans
        
        if rotation is None:
            rotation=self.modTrans.rotation
        if translation is None:
            translation=self.modTrans.translation
        if scale is None:
            scale=self.modTrans.scalar
        self.targetModelTrans=ModTrans(rotation, translation, scale)
        self.t=time.time()
        self.idle=True


    def idleModel(self):
        """ idlet Model"""
        t=time.time()-self.t
        if t>1:
            t=1.0
        self.modTrans = self.originalModelTrans.interpolate(self.targetModelTrans, t)

        if t>=1:
            self.idle=False
       
        

   
        

    def model(self):
        """ zeichnet Transformiertes Model"""
        self.modTrans.openGLTransform()
        self.uniform()
        glCallList(self.modelList)


    def draw(self):
        """ zeichnet komplettes Model """
        glPushMatrix()
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glEnable(GL_POLYGON_OFFSET_FILL)
        #Teturieren
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPolygonOffset(1.0,1.0)
        
        #Model
        self.doMaterial()
        self.model()
       
        glDisable(GL_POLYGON_OFFSET_FILL)
        glPopMatrix()
        glPushMatrix()
        # facetLinien
        glDisable(GL_LIGHTING)
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glEnable (GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0,1.0,1.0, 0.2) 
        glLineWidth(1)
        self.model()
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glDisable (GL_BLEND);
        glEnable(GL_LIGHTING)
        glPopMatrix()

if __name__ == "__main__":
   import newGoogleBody
   newGoogleBody.main()
