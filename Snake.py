#Snake
import pygame,sys
from pygame.locals import *
from body import body
from head import head
from SnakeTools import *

class Snake:
    
    def __init__(self,x,y,headIm,ori='r'):
        
        self.head=head(x,y,headIm)
        self.head.orientation=ori
        self.blocks=[]
        self.orientation=ori   
        self.headImg=headIm
        self.bodyImg=pygame.Surface((0,0))
        self.walls=[]
        
    def move(self,ori):
        
        if(ori!=self.orientation):
            #turn happened
            turn=(self.head.rect.x,self.head.rect.y,ori)
            for block in self.blocks:
                block.turns.append(turn)
            self.orientation=ori
            self.head.orientation=ori
   
        self.head.rect.x,self.head.rect.y=desloc(self.head.rect.x,self.head.rect.y,ori)
        
        for b in self.blocks:
            b.move()

    def createWalls(self,dim):
        
        r1=pygame.rect.Rect(0,-1,dim,1)
        r2=pygame.rect.Rect(-1,0,1,dim)
        r3=pygame.rect.Rect(dim,0,1,dim)
        r4=pygame.rect.Rect(0,dim,dim,1)
        self.walls.append(r1)
        self.walls.append(r2)
        self.walls.append(r3)
        self.walls.append(r4)
    
    def isAlive(self):
        
        head_rect=self.head.rect
        
        for bloc in self.blocks:
            if(head_rect.colliderect(bloc.rect)):
                return False
        
        for wall in self.walls:
            if(head_rect.colliderect(wall)):
                return False
        return True
    
    def calcBodyPosition(self,bloc):
        
        ori=bloc.orientation
        
        #values
        spacing=int(0.70*bloc.image.get_width())
        dist=spacing+bloc.image.get_width()
        
        #virtual values
        virtualx,virtualy=0,0
        
        if(ori=='r'):
            virtualx,virtualy=(bloc.rect.x-dist),(bloc.rect.y)

        elif(ori=='l'):
            virtualx,virtualy=(bloc.rect.x+dist),(bloc.rect.y)

        elif(ori=='u'):
            virtualx,virtualy=(bloc.rect.x),(bloc.rect.y+dist)

        elif(ori=='d'):
            virtualx,virtualy=(bloc.rect.x),(bloc.rect.y-dist)
        
        return (virtualx,virtualy)
    
    def addBlock(self):
        
        lastbloc=self.head
        
        if(len(self.blocks)>0):
            lastbloc=self.blocks[-1]
        bx,by=self.calcBodyPosition(lastbloc)
        nbody= body(bx,by,lastbloc.orientation,lastbloc.image)
        nbody.turns=list(lastbloc.turns)
        self.blocks.append(nbody)
        
    def eaten(self,food):
        
        if(self.head.rect.colliderect(food.rect)):
            return True
        return False
    
    
    def obstDist(self,ori):
        
        dx,dy=0,0
        if(ori==0):
            dx=1
        elif(ori==2):
            dx=-1
        elif(ori==3):
            dy=-1
        elif(ori==1):
            dy=1
        
        virtualx,virtualy=int(self.head.rect.x+(self.head.image.get_width()*0.5)),int(self.head.rect.y+(self.head.image.get_height()*0.5))
        flag=True
        while(flag):
            virtualx+=dx
            virtualy+=dy
            for bloc in self.blocks:
                bx,by=bloc.get_render_rect()
                sp=int(bloc.image.get_width()*0.7)
                nrect=pygame.rect.Rect(bx,by,(bloc.image.get_width()+sp),(bloc.image.get_height()+sp))
                if(nrect.collidepoint(virtualx,virtualy)):
                    flag=False
                    break
            
            if(flag):    
                for wall in self.walls:
                    if(wall.collidepoint(virtualx,virtualy)):
                        flag=False
                        break
        if(ori==0 or ori==2):
            return abs((self.head.rect.x-virtualx))
        elif(ori==1 or ori==3):
            return abs((self.head.rect.y-virtualy))

    
    def getAtr(self):
        
        nori=oriNumb(self.orientation)
        return [self.obstDist((nori+3)%4),self.obstDist(nori),self.obstDist((nori+1)%4)]
    
    def normalizeData(self,features):
        
        f=[]
        for fi in features:
            f.append([int(fi[0]/self.head.image.get_width()),int(fi[1]/self.head.image.get_width()),
                     int(fi[2]/self.head.image.get_width()), int(fi[3]),int(fi[4]),fi[5]])
        return f