import math
class Vec:

    


    def __cmp__(self, anderer):
        return sum(map(cmp, self, anderer))


    def __getitem__(self, wert):
        return self.v[wert]

    def __len__(self):
        return len(self.v)
    
    def __init__(self, *v):
        if isinstance(v[0], list) or isinstance(v[0], tuple) or isinstance(v[0], Vec):
            v=v[0]
        self.v=[float(x) for x in v]
        


    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return "Vektor mit: " + str(self.v)

    def __sub__(self, anderer):
        return self.subtraktion(anderer)
    
    def __add__(self, anderer):
        return self.addition(anderer)

    def __mul__(self, anderer):
        if isinstance(anderer, Vec):
            return self.skalarprodukt(anderer)
        return self.skalarmultiplikation(anderer)
    
    def __div__(self, anderer):
        return self.skalarmultiplikation(1.0 / float(anderer))

    def __mod__(self, anderer):
        return self.kreuzprodukt(anderer)

    def __neg__(self):
        return self.neg()


    def multi(self, hv3):
        return Vec(map(lambda x, y: x*y, self.v, hv3.v))


    def neg(self):
        return Vec([-x for x in self.v])

    def asColor(self):
        return tuple([int(x) for x in self.v])
   
    
    def addition(self, hv3):        
        return Vec(map(lambda x, y: x+y, self.v, hv3.v))

    def subtraktion(self, hv3):        
        return Vec(map(lambda x, y: x-y, self.v, hv3.v))

    def dot(self, hv3):
        return self.skalarprodukt(hv3)
    
    def skalarprodukt(self, hv3):        
        return sum(map(lambda x, y: x*y, self.v, hv3.v))  #<v,w> #+*

    def skalarmultiplikation(self, skalar):
        return Vec([x*skalar for x in self.v])

   


    def length(self):
        return math.sqrt(sum([x*x for x in self.v]))

    def normalized(self):
        a=self.length()
        return Vec([float(x)/float(a) for x in self.v])


    def winkel(self, vec):
        d=math.acos( (vec * self)/(self.length()*vec.length()))
        return math.degrees(d)


    def kreuzprodukt(self, hv3):
        
        i=2
        j=1
        temp=[]
        for t in range(3):
            temp.append(self.v[j]*hv3.v[i] - self.v[i]*hv3.v[j])
            i=(i+1)%3
            j=(j+1)%3
        return Vec(temp)



