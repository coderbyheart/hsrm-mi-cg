import math
from Vec import Vec

class Quaternion:

    def __init__(self,s,v):
       self.s=s
       self.v=v

    def __repr__(self):
        return str((self.s,self.v))

    def __mul__(self, anderer):
        if isinstance(anderer, Quaternion):
            return self.multQuat(anderer)
        else:
            return self.multSkalar(anderer)
        
    def __add__(self, quat):
        return self.add(quat)

    def rotationsmatrix(self):
        x,y,z=self.v
        s=self.s
        v0 = [ s*s+x*x-y*y-z*z , 2*(x*y+s*z) , 2*(x*z-s*y) , 0]
        v1 = [ 2*(x*y-s*z) , s*s-x*x+y*y-z*z , 2*(y*z+s*x) , 0]
        v2 = [ 2*(x*z+s*y) , 2*(y*z-s*x) , s*s-x*x-y*y+z*z , 0]
        v3 = [0,0,0,1]
        temp=[]
        for v in [v0,v1,v2,v3]:
            temp.append(v)
        return temp

    def multQuat(self, quat):
        s=self.s*quat.s- ( self.v * quat.v )
        v=quat.v*self.s + self.v*quat.s + self.v%quat.v
        return Quaternion(s,v)

    def multSkalar(self, skalar):
        return Quaternion(self.s*skalar, self.v*skalar)

    def add(self, quat):
        return Quaternion(self.s+quat.s, self.v+quat.v)

    def length(self):
        return math.sqrt( self.s*self.s + sum([x*x for x in self.v]))

    def konjugiert(self):
        return Quaternion(self.s, Vec(-self.v))

    def inverse(self):
        if self.length()==1.0:
            return self.konjugiert()
        return self.konjugiert() * math.pow(self.length(), -2) 


    def exp(self):
        lv=self.v.length()
        es = math.exp(self.s)
        s=math.cos(lv)
        v=(self.v/lv) * math.sin(lv)
        return Quaternion( s*es, v*es )


    def ln(self):
        return Quaternion( math.log(self.length()) , ( self.v/self.v.length() ) * math.acos(self.s/self.length() ) )

        
    def power(self, b):
        if b==0:
            b=0.00001
        return (self.ln()*b).exp()


    def rotateVec(self, vec):
        vecQuat=Quaternion(0, vec)
        return  (self*vecQuat*self.inverse()).v
        

    def dot(self, quat):
        return self.s*quat.s + sum(map(lambda x, y: x*y, self.v, quat.v))
        
    def slerp(self, q1,t):
        if self.s==q1.s and self.v==q1.v:
            return q1
        if t==0:
            t=0.0001
        return self*(self.inverse()*q1).power(t)



def slerp(q0,q1,t):
    return q0*(q0.inverse()*q1).power(t)
   
    
    

def rotationQuat( alpha, vec):
    """ liefert Quaternion  mit der angegebenen alpha um den Winkel """
    alpha=math.radians(alpha)
    quat=Quaternion(0,Vec(0,0,0))
    quat.s=math.cos(alpha/2.0)
    vec = vec.normalized()*math.sin(alpha/2.0)
    quat.v=vec
    return quat
        

