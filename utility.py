from random import uniform
from math import sqrt, cos, sin, pi
def distance(theAPos, theBPos):
   aDelta = (theAPos[0] - theBPos[0], theAPos[1] - theBPos[1])
   aDist = sqrt(aDelta[0] * aDelta[0] + aDelta[1] * aDelta[1])
   return int(aDist)


def add(apos, bpos):
   return (apos[0] + bpos[0] , apos[1] + bpos[1])

#vector created is first term points to second
def sub(apos, bpos):
   return (bpos[0] - apos[0] , bpos[1] - apos[1])

def mag(v):
   amag = v[0] * v[0] + v[1] * v[1]
   amag += 0.0001
   amag = sqrt(amag)
   return amag


def normalize(v):
   amag = mag(v)
   return (v[0] / amag, v[1] / amag)

def mul(adir, ascalar):
   return (adir[0] * ascalar, adir[1] * ascalar)

def randPointAtDistance(thePoint, theDistance):
   randAngle = uniform(0., 359.9) / 360. * pi * 2.
   randPoint = add(mul((cos(randAngle), sin(randAngle)), theDistance), thePoint)
   return randPoint