# -*- coding: utf-8 -*-
class PointTween(object):
    "Repräsentiert einen Punkt-Tween zwischen dem Punkt start und end mit steps Zwischenschritten."
    def __init__(self, start, end, nsteps):
        "Konstruktor: Start-Punkt (x,y)-Tupel, End-Punkt (x,y)-Tupel, Anzahl der Schritte"
        self.start = start
        self.end = end
        self.nsteps = int(nsteps)
        # Berechne Vektor zwischen Start und Ende
        self.v = (self.end[0] - self.start[0], self.end[1] - self.start[1])
        # Berechne Zwischenschritte
        self.steps = []
        self.steps.append(self.start)
        for i in range(1, nsteps - 1):
            dstep = float(i) / (nsteps - 1)
            self.steps.append((self.start[0] + dstep * self.v[0], self.start[1] + dstep * self.v[1]))
        self.steps.append(self.end)

    def __iter__(self):
        return iter(self.steps)

if __name__ == "__main__":
    pt = PointTween((0,0), (10,10), 5)
    print pt.steps
    for point in pt:
        print point
    pt = PointTween((0,0), (10,10), 11)
    print pt.steps
