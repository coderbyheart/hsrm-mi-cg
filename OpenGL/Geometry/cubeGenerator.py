from HomVec3 import HomVec3

f = open('data/cube_points.raw', 'w')

def pp(p):
    f.write("%.f %.f %.f\n" % (p.x, p.y, p.z))

steps = 10
size = 10

p = HomVec3(0,0,0,1)
pp(p)

for i in range(steps):
    p.x = p.x + size / steps
    pp(p)
    
for i in range(steps):
    p.y = p.y + size / steps
    pp(p)
    
for i in range(steps):
    p.x = p.x - size / steps
    pp(p)
    
for i in range(steps):
    p.y = p.y - size / steps
    pp(p)
    
for i in range(steps):
    p.z = p.z + size / steps
    pp(p)
    
for i in range(steps):
    p.x = p.x + size / steps
    pp(p)
    
for i in range(steps):
    p.z = p.z - size / steps
    pp(p)
    
p.y = size
p.x = 0

for i in range(steps):
    p.z = p.z + size / steps
    pp(p)
    
for i in range(steps):
    p.x = p.x + size / steps
    pp(p)
    
for i in range(steps):
    p.z = p.z - size / steps
    pp(p)

p.y = size
p.x = 0
p.z = size

for i in range(steps):
    p.y = p.y - size / steps
    pp(p)
    
p.y = size
p.x = size
p.z = size

for i in range(steps):
    p.y = p.y - size / steps
    pp(p)
    
f.close()