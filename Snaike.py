
# coding: utf-8

# In[413]:

import pygame,sys
from pygame.locals import *
from random import randint


# In[414]:

#colors
WHITE = (255, 255, 255)
BLACK=(0,0,0)


# In[415]:

def desloc(x,y,ori):
    des=1
    if(ori=='r'):
        return (x+des,y)
    elif(ori=='l'):
        return (x-des,y)
    elif(ori=='u'):
        return (x,y-des)
    elif (ori=='d'):
        return (x,y+des)


# In[416]:

class food(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y


# In[417]:

#head
class head(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=pygame.rect.Rect(x,y,int(img.get_width()*0.75),int(img.get_height()+0.75))
        self.orientation=''
        self.turns=[]
    
    def get_render_rect(self):
        
        return ((self.rect.x-int(self.image.get_width()*0.25)),(self.rect.y-int(self.image.get_height()*0.25)))


# In[418]:

#body
class body(pygame.sprite.Sprite):
    def __init__(self,x,y,ori,img):
        
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=pygame.rect.Rect(x,y,int(img.get_width()*0.75),int(img.get_height()*0.75))
        self.orientation=ori
        self.turns=[]
    
    def move(self):
        
        if(len(self.turns)==0):
            self.rect.x,self.rect.y=desloc(self.rect.x,self.rect.y,self.orientation)
            
        else:
            turnx,turny,turno= self.turns[0]
            virtualx,virtualy=desloc(self.rect.x,self.rect.y,self.orientation)
            
            if(((self.orientation=='r' and virtualx>turnx) or (self.orientation=='l' and virtualx<turnx) 
               or (self.orientation=='u' and virtualy<turny) or (self.orientation=='d' and virtualy>turny))
              and self.orientation!=turno):
                
                self.rect.x,self.rect.y=desloc(self.rect.x,self.rect.y,turno)
                self.orientation=turno
                self.turns.pop(0)
                
            else:
                self.rect.x,self.rect.y=desloc(self.rect.x,self.rect.y,self.orientation)

    def get_render_rect(self):
        
        return ((self.rect.x-int(self.image.get_width()*0.25)),(self.rect.y-int(self.image.get_height()*0.25)))
                


# In[419]:

#Snake
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


# In[420]:

def renderSnake(display,snake):
    
    headImg=snake.headImg
    bodyImg=snake.bodyImg
    
    #add head
    display.blit(headImg,snake.head.get_render_rect())
    
    #add body
    for body in snake.blocks:
        display.blit(bodyImg,body.get_render_rect()) 
        


# In[421]:

def renderFood(display,food):
    
    display.blit(food.image,food.rect)


# In[422]:

def newFood(foodImg,dim):
    
    fos=5
    return food(randint(fos,(dim-foodImg.get_width()-fos)),randint(fos,(dim-foodImg.get_height()-fos)),foodImg)


# In[424]:

#init
pygame.init()
dim=300
displaysurf=pygame.display.set_mode((dim,dim))
pygame.display.set_caption('Snaike')
fpsClock = pygame.time.Clock()
FPS = 120


#emilia variables
emiliaImg = pygame.image.load('blue.png')
emiliaSnake = Snake(int(dim/2),int(dim/2),emiliaImg,ori='d')
emiliaSnake.createWalls(dim)

#subaro
subaroImg=pygame.image.load('blue.png')
emiliaSnake.bodyImg=subaroImg

#game over
gameoverImg=pygame.image.load('gameover.jpg')

#food
foodImg=pygame.image.load('hamb.png')
foood=newFood(foodImg,dim)

#emiliaSnake.addBlock()

gameOverFlag=False

#game loop
while True:   
    displaysurf.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type== QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key==K_UP and orientation!='d':
                orientation='u'
            elif event.key==K_DOWN and orientation!='u':
                orientation='d'
            elif event.key==K_RIGHT and orientation!='l':
                orientation='r'
            elif event.key==K_LEFT and orientation!='r':
                orientation='l'
            elif event.key==K_f:
                emiliaSnake = Snake(int(dim/2),int(dim/2),emiliaImg)
                emiliaSnake.createWalls(dim)
                emiliaSnake.bodyImg=subaroImg
                gameOverFlag=False
            elif event.key==K_n:
                pygame.quit()
                sys.exit()
    
    #emilia motion
    emiliaSnake.move(orientation)
    
    if(not emiliaSnake.isAlive()):
        gameOverFlag=True
        
        displaysurf.blit(gameoverImg, (int((dim-gameoverImg.get_width())/2),(int((dim-gameoverImg.get_height())/2)-50)))
        pygame.display.update()

    if(emiliaSnake.eaten(foood)):
        
        foood=newFood(foodImg,dim)
        emiliaSnake.addBlock()
    
    if(not gameOverFlag):
        renderSnake(displaysurf,emiliaSnake)
        renderFood(displaysurf,foood)
        pygame.display.update()
        
    fpsClock.tick(FPS)

            

