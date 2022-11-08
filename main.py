#direction, move instant 8 cardinal

#move instant with turn 8 cardinal
#move with delay to 8 cardinal
#input is always 8 cardinal, or analog x,y
#normalize move distance with 8 cardinal
#static object, moving is extra
#dynamic object, includes movement, create moving object class
#entity, has input flags related to movement
#movement is limited to certain values
import math
import math
from math import sqrt
from random import *
import pygame as pg
from pygame.locals import *


def distance(theAPos, theBPos):
   aDelta = (theAPos[0] - theBPos[0], theAPos[1] - theBPos[1])
   aDist = sqrt(aDelta[0] * aDelta[0] + aDelta[1] * aDelta[1])
   return int(aDist)


def add(apos, bpos):
   return (apos[0] + bpos[0] , apos[1] + bpos[1])

#vector created is first term points to second
def sub(apos, bpos):
   return (bpos[0] - apos[0] , bpos[1] - apos[1])

def normalize(v):
   amag = v[0] * v[0] + v[1] * v[1]
   amag += 0.0001
   amag = math.sqrt(amag)
   return (v[0] / amag, v[1] / amag)

def mul(adir, ascalar):
   return (adir[0] * ascalar, adir[1] * ascalar)

WIDTH, HEIGHT = 1000, 600
PLAYER_SPEED = 1
PLAYER_SIZE = 5
FALL_SPEED = 1


class Ball:
   def __init__(self, pos, dir=(0, 0), size=PLAYER_SIZE, color='red'):
      self.pos = pos
      self.dir = dir
      self.size = size
      self.color = color
      self.tag = False

   def update(self):
      # print(f'ball:{self.pos},{self.dir}')
      self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
      global WIDTH, HEIGHT
      if self.pos[1] > HEIGHT + self.size:
         self.pos = (randrange(self.size, WIDTH - self.size), -self.size)

   def render(self, screen):
      pg.draw.circle(screen, self.color, self.pos, self.size)
      if self.tag:
         pg.draw.circle(screen, 'yellow', self.pos, self.size * 2, 3)


class Shot(Ball):
   def __init__(self, pos, dir, size=1  ):
      Ball.__init__(self,pos, dir, size )
      self.size = int(self.size)

   def update(self):
      global WIDTH, HEIGHT
      # print(f'shot:{self.pos},{self.dir}')
      Ball.update(self)
      if self.pos[0] > WIDTH or self.pos[0] < 0 or self.pos[1] < 0 or self.pos[1] > HEIGHT:
         return False
      return True

   def render(self, screen):
      pg.draw.line(screen, self.color, self.pos, add(self.pos, mul( self.dir, 3)),self.size)

#update positions and reset on scene exit
def updateBalls(npc, player):
   for i in range(len(npc)):
      if distance(player.pos, npc[i].pos) < npc[i].size + player.size:
         npc[i].tag = True
         player.size += 1

#test shots vs npcs and creatwe debris on collision
def updateShots(npc, shots, debris):
   for i in range(len(npc)):
      for j in range(len(shots)):
         if distance(shots[j].pos, npc[i].pos) < npc[i].size + shots[j].size * 2:
            npc[i].tag = True
            for k in range(randrange(20) + 1):
               aAngle = randrange(360)/360.0*2*math.pi
               aDir = mul((math.cos(aAngle), math.sin(aAngle)), uniform(PLAYER_SIZE/6, PLAYER_SIZE))
               debris.append( Debris(npc[i].pos, add(aDir, npc[i].dir), randrange(5) + 1, life=(randrange(100)+ 20)))
   return [ic for ic in npc if not ic.tag]

#debris enriches player, stuff disappears
def updateDebris(player, debris):
    for stuff in debris:
        if distance(stuff.pos, player.pos) < stuff.size + player.size:
            player.size += 1
            stuff.tag = True
    return [stuff for stuff in debris if not stuff.tag]
    
class Debris(Shot):
   def __init__(self, pos, dir, size, life=20):
      Shot.__init__(self, pos, dir, size)
      self.life  = life
      self.dampen = uniform(.75, 1.)

   def update(self):
      Shot.update(self)
      self.dir = mul( self.dir, self.dampen)
      if self.life > 0:
         self.life -= 1
      else:
         return False
      return True

   def render(self, screen):
      Shot.render(self,screen)
      Ball.render(self,screen)


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
PLAYER_FIRE = False
PLAYER_FIRE2 = False
MOVE_L, MOVE_R, MOVE_U, MOVE_D = 0, 0, 0, 0
playerPos = (WIDTH/2, HEIGHT/2)
player = Ball(playerPos, size=PLAYER_SIZE)

clock = pg.time.Clock()
shots = [] #shots player fires
debris = []    #debris from npcs fires
npc = []
for i in range(100):
   # npc.append( {'pos':( randrange(10,WIDTH - 10), randrange(10, HEIGHT - 10) ),'tag':False} )
   npc.append( Ball(( randrange(10,WIDTH - 10), randrange(10, HEIGHT - 10) ), (0, FALL_SPEED), PLAYER_SIZE, color='white' ))
running = True
while running:
   for event in pg.event.get():
      if event.type == QUIT:
         running = False
      elif event.type == KEYDOWN:
         if event.key == K_ESCAPE:
            running = False
         elif event.key == K_LEFT:
            MOVE_L = True
            MOVE_R = False
         elif event.key == K_RIGHT:
            MOVE_R = True
            MOVE_L = False
         elif event.key == K_UP:
            MOVE_U = True
            MOVE_D = False
         elif event.key == K_DOWN:
            MOVE_U = False
            MOVE_D = True
         elif event.key == K_SPACE:
            PLAYER_FIRE = True
      elif event.type == KEYUP:
         if event.key == K_DOWN:
            MOVE_D = False
         if event.key == K_UP:
            MOVE_U = False
         if event.key == K_LEFT:
            MOVE_L = False
         if event.key == K_RIGHT:
            MOVE_R = False
         if event.key == K_SPACE:
            PLAYER_FIRE = False
      elif event.type == MOUSEBUTTONDOWN:
         print(f"mDown:{pg.mouse.get_pressed()}")
         PLAYER_FIRE2 = True

   if PLAYER_FIRE2 and player.size > 6:
      adelta = sub(player.pos, pg.mouse.get_pos())
      adir = mul(normalize(adelta ) , PLAYER_SIZE)
      print(f'Mouse:{pg.mouse.get_pos()}, dir:{adir}, delta:{adelta}')
      shots.append( Shot(player.pos, adir, player.size) )
      player.size -= 1
   PLAYER_FIRE2 = False
#update
   dx, dy = 0, 0
   if MOVE_L:
      dx = -PLAYER_SPEED
   if MOVE_R:
      dx = PLAYER_SPEED
   if MOVE_U:
      dy = -PLAYER_SPEED
   if MOVE_D:
      dy = PLAYER_SPEED
   player.dir = (dx, dy)
   player.update()
   #fire a shot if all good
   if (dx != 0 or dy != 0) and PLAYER_FIRE and player.size > 6:
      print("shot fire")
      shots.append( Shot(player.pos, mul(player.dir, (player.size / 6) + 1 ), (player.size / 6) + 1))
      player.size -= (player.size / 6) + 1
      PLAYER_FIRE = False
   for i in range(len(npc)):
      npc[i].update()
   updateBalls(npc, player)
   shots = [shot for shot in shots if shot.update()]
   npc = updateShots(npc, shots, debris)    #check if we hit any npcs
   if len(npc) < 100:
      npc.append(Ball(( randrange(10,WIDTH - 10), - 10 - randrange(0,10) ), (0, FALL_SPEED), PLAYER_SIZE, color='white' ))
   debris = [stuff for stuff in debris if stuff.update()]
   debris = updateDebris(player, debris)
#RENDER
   screen.fill('black')
   player.render(screen)
   for i in range(len(npc)):
      npc[i].render(screen)
   for shot in shots:
      shot.render(screen)
   for stuff in debris:
      stuff.render(screen)
   pg.display.flip()
   clock.tick(60)
print("Exited")
pg.quit()
#exit()