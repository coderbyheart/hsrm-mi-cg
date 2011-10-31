# -*- coding: utf-8 -*-
from OpenGL.GLUT import *
from Quaternion import *
from Vec import Vec
import math
import time
import Picking
class InputDevice():
    

    def __init__(self, model, reshape,  worldTrans, doProjectionMatrix):
        """ init"""
        self.doProjectionMatrix=doProjectionMatrix
        self.model = model
        self.worldTrans=worldTrans
        self.leftPress = False
        self.rightPress = False
        self.midPress = False
        self.mouseXY = 0.0, 0.0
        self.bgColor = 1,1,1
        self.ortho=False
        self.moveZ=False
        self.fadenkreuz=False
        self.reshape=reshape
        self.world=False
        self.drawText=False
        self.text="nothing"
        self.shadow = False
    
    def mouseMotion(self,  x, y):
        """ Maus bewegung wenn Maustaste gedrückt ist"""
        self.drawText=False
        xx =   x - self.mouseXY[0]   
        yy =   self.mouseXY[1] -y
        #Linke Maustaste
        if self.leftPress:
            if self.world:
                self.worldRotateXY(x,y)
            else:
                self.modelRotateXY(x,y)
        #Mittlere Maustaste
        if self.midPress:
            if self.world:
                self.worldZoomZ(yy)
            else:
                if self.moveZ:
                    self.modelTranslateZ( yy)
                else:
                    self.modelScale( yy)
        #Rechte Maustaste
        if self.rightPress:
            
            if self.world:
               self.worldTranslateXY(xx,yy)
            else:
               self.modelTranslateXY(xx,yy)
               
        self.mouseXY=x,y
        glutPostRedisplay()


        
        
            

    def mouseClick(self, button,  state,  x,  y):
        """ Maustaste druecken / loslassen"""
        self.drawText=False
        #MausTAste druecken
        if state == GLUT_DOWN :
            self.mouseXY = x,y
            self.clickXY=x,y
            if button == GLUT_LEFT_BUTTON:
                self.leftPress = True
            if button == GLUT_MIDDLE_BUTTON:
                self.midPress=True
            if button == GLUT_RIGHT_BUTTON:
                self.rightPress=True
        #Maustaste loslassen
        if state == GLUT_UP :
            if button == GLUT_LEFT_BUTTON:
                self.leftPress = False
                #Picking
                xx,yy=self.clickXY
                if x == xx and y == yy:
                    self.doPick(x,y)
            if button == GLUT_MIDDLE_BUTTON:
                self.midPress=False
            if button == GLUT_RIGHT_BUTTON:
                self.rightPress=False
        
        glutPostRedisplay()



    def doPick(self,x,y):
        """ picking"""
        self.text = Picking.pick(x,y,self.worldTrans, self.model, self.doProjectionMatrix)
        if self.text is not None:
            self.drawText=True
    
    def keyRelease(self, key, x, y):
        """ Keyboardtaste loslassen """
        # 'n' -> z-Achse-Verschiebung anstatt skalieren
        if key=='n':
           self.moveZ=False
    

    def keyPressed(self, key, x, y):
       """ handle keypress events """
      
       self.drawText=False

       # umschalten Welt/Model Bewegung
       if key == 'm':
          if self.world:
             self.world = False
          else:
             self.world = True

            
      
        
       # Alles auf Anfang
       elif key==' ':
           self.worldTrans.initIdle()
           self.model.initIdle(rotationQuat(0.0, Vec(1 ,1,1)) , Vec(0,0,0), 1.0)

        # 'n' -> z-Achse-Verschiebung anstatt skalieren
       elif key=='n':
           self.moveZ=True
       #escape
       elif key == chr(27): # chr(27) = ESCAPE
           sys.exit()

       #translate
       elif key == 'w':
           self.modelTranslateXY(0, 10)
       elif key == 's':
           self.modelTranslateXY(0, -10)
       elif key == 'a':
           self.modelTranslateXY(-10, 0)
       elif key == 'd':
           self.modelTranslateXY(10, 0)
       elif key == 'q':
           self.modelTranslateZ(-10)
       elif key == 'e':
           self.modelTranslateZ(10)
       
        
           
       #rotate
           
       elif key == 'x':
          self.modelRotateX(1)
       elif key == 'X':
          self.modelRotateX(-1)
       elif key == 'y':
          self.modelRotateY(1)
       elif key == 'Y':
          self.modelRotateY(-1)
       elif key == 'c':
          self.modelRotateZ(1)
       elif key == 'C':
          self.modelRotateZ(-1)

    

       #backcolor
       elif key == '1':
          self.bgColor = 0.0,0.0,1.0  #blue
       elif key == '2':
          self.bgColor = 0.0,1.0,0.0  #green
       elif key == '3':
          self.bgColor = 1.0,0.0,0.0  #red
       elif key == '4':
          self.bgColor = 0.0,0.0,0.0  #black
       elif key == '5':
          self.bgColor = 1.0,1.0,1.0  #white
       elif key == '6':
          self.bgColor = 1.0,1.0,0.0  #yellow

       #zoom
       elif key == 'r':
          self.modelScale(1)
       elif key == 'f':
          self.modelScale(-1)

       #Perpektive 
       elif key == 'o':
          if self.ortho:
             self.ortho = False
             print 'Kamera pers'
          else:
             self.ortho = True
             print 'Kamera ortho'
          self.reshape(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))


       #Fadenkreuz
       elif key== 'p':
          if self.fadenkreuz:
             self.fadenkreuz = False
          else:
             self.fadenkreuz = True
       #Schatten
       elif key== 'j':
          if self.shadow:
             self.shadow = False
          else:
             self.shadow = True


       glutPostRedisplay()


   
        

    def rotateXY(self,mouseX,mouseY):
        """ rotieren weiterleiten """
        if self.world:
            worldRotateXY(mouseX,mouseY)
        else:
            modelRotateXY(mouseX,mouseY)



   
    def worldRotateXY(self, mouseX, mouseY):
        """ Welt-Rotierung anhand Mausbewegung festlegen"""
        #Distancen
        x =   mouseX - self.mouseXY[0] 
        y =   self.mouseXY[1] - mouseY
        #Winkel
        alpha = math.hypot(x,y)
        
        dirX = self.worldTrans.directionX
        dirY = self.worldTrans.directionY
        up= self.worldTrans.up
        #Achse
        achse=dirX*y+dirY*x
        #PruefWinkel
        winkel = dirY.winkel(up)
        # Pruef-Winkel pruefen: begrenzt rotierung
        if winkel>85 or winkel < -85:
            #Falls begrezung eintrifft: nur um Y-Achse rotieren
            alpha=x
            achse=dirY
            
        self.worldRotateAxe(-alpha, achse)
      

    def worldZoomZ(self,skalar):
        """ Welt-Zoom, Distance zum Blickpunkt"""
        self.worldTrans.zoom(skalar*0.02)  



    def modelRotateXY(self,mouseX,mouseY):
        """ Model-Rotierung festlegen """
        #distancen
        xx, yy =   self.mouseXY 
        x,y=mouseX-xx,yy-mouseY
        #Winkel
        alpha= math.hypot(x,y)
        
        dirZ=self.worldTrans.directionZ
        dirX=self.worldTrans.directionX
        dirY=self.worldTrans.directionY
        #Achse
        achse=dirX*-x+dirY*y
        achse = achse % dirZ
        
        self.modelRotateAxe(alpha, achse )
       

        
    def modelRotateZ(self,z):
        self.modelRotateAxe(z, self.worldTrans.directionZ )
      
    def modelRotateX(self,x):
        self.modelRotateAxe(x, self.worldTrans.directionX )
      
    def modelRotateY(self,y):
        self.modelRotateAxe(y, self.worldTrans.directionY )
      
    
    
    def modelRotateAxe(self, alpha, achse):
        """ rotierung des Models um den Winkel und Achse """
        self.model.modTrans.rotate(rotationQuat( alpha, achse))

    def worldRotateAxe(self, alpha, achse):
        """ rotierung der Welt um den Winkel und Achse """
        self.worldTrans.rotate(rotationQuat( alpha, achse))


    def modelTranslateZ(self, z):
        """ verschiebung des Models um die Z Achse """
        scale=-0.01
        translation=self.worldTrans.directionZ*(z*scale)
        self.model.modTrans.translate(translation)
        
    def modelTranslateXY(self, x,y):
        """ verschiebung des Models um die X,Y Achsen """
        scale=-0.01
        translation=self.worldTrans.directionX*(x*scale) + self.worldTrans.directionY*(y*-scale)
        self.model.modTrans.translate(translation)


    def worldTranslateXY(self, x,y):
        """ verschiebung der Kamera um die X,Y Achsen """
        scale=-0.01
        translation=self.worldTrans.directionX*(x*scale) + self.worldTrans.directionY*(y*-scale)
        self.worldTrans.translate(translation)



    def modelScale(self, skalar):
        """ Model skalieren """
        self.model.modTrans.scale(skalar*0.02)
   
        


if __name__ == "__main__":
   import newGoogleBody
   newGoogleBody.main()
