
# coding: utf-8

# # Snaike game with neural nets

# ## Importing modules

# In[1]:

from Snake import Snake
from body import body
from head import head
from food import food
from SnakeTools import *
from SnakeRender import *
from pygame.locals import *
from SnakeAi import *
from PopulationTools import *
import pygame,sys
import pickle
import tensorflow as tf
import matplotlib.pyplot as plt
import time
import gc
import os


# In[2]:

#colors
WHITE = (255, 255, 255)
BLACK=(0,0,0)
RED= (220,20,60)


# In[3]:

#init
print("Initializing game")
pygame.init()
score=0
attempt=1
attempt_flag=True

#Font config
pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 25)
game_name = myfont.render('Snaike Game', False, (220,20,60))
myfont2 = pygame.font.SysFont('Comic Sans MS', 25)

#Screen config
dim=500
dim2=int(dim/2)
displaysurf=pygame.display.set_mode((dim,dim+150))
pygame.display.set_caption('Snaike')

#FPS
fpsClock = pygame.time.Clock()
FPS = 45
framecount=0


#emilia variables
emiliaImg = pygame.image.load('blue.png')
emiliaSnake = Snake(int(dim/2),int(dim/2),emiliaImg,ori='r')
emiliaSnake.createWalls(dim)

#subaro
subaroImg=pygame.image.load('blue.png')
emiliaSnake.bodyImg=subaroImg

#game over image
gameoverImg=pygame.image.load('gameover.jpg')

#food image
foodImg=pygame.image.load('hamb.png')
foood=newFood(foodImg,dim)

#orientation
lastorientation=emiliaSnake.orientation
orientation=emiliaSnake.orientation
gameOverFlag=False


# In[4]:

#Session
session = tf.Session()
session.run(tf.global_variables_initializer())


# In[5]:

#Neural net configuration
inputlayer=4
layer1=10
layer2=3
chromsize=83


# In[6]:

#Placeholder
x=tf.placeholder(tf.float32,shape=[None,inputlayer], name='x')

def CreateNeuralNet(chromossome):
    #The first (inputlayer*layer1) numbers are the weights of the first layer, and the next (layer1) numbers are their biases
    #This logic is applyied to the next layers
    w1=chromossome[0:(inputlayer*layer1)].reshape([inputlayer,layer1])
    b1=chromossome[(inputlayer*layer1):(inputlayer*layer1+layer1)]
    w2=chromossome[(inputlayer*layer1+layer1):(inputlayer*layer1+layer1+layer1*layer2)].reshape([layer1,layer2])
    b2=chromossome[(inputlayer*layer1+layer1+layer1*layer2):(inputlayer*layer1+layer1+layer1*layer2+layer2)]
    
    #Neural net definition
    w1=tf.Variable(w1,dtype=tf.float32)
    b1=tf.Variable(b1,dtype=tf.float32)
    first_layer=tf.nn.relu(tf.matmul(x,w1)+b1)
    w2=tf.Variable(w2,dtype=tf.float32)
    b2=tf.Variable(b2,dtype=tf.float32)
    second_layer=tf.nn.softmax(tf.matmul(first_layer,w2)+b2)
    out_layer=tf.argmax(second_layer,axis=1)
    session.run(tf.global_variables_initializer())
    
    #The tensor that is returned outputs the class directly
    return out_layer


# In[7]:

#Pool
pool=SubjectPool()
subject=pool.get_subj()
neural_net=CreateNeuralNet(subject[1])

#Defined as time + score*time
fitness=0
timeout=1.5
food_time=time.time()
hamb=0
emiliaSnake.addBlock()
garbage_time=time.time()


# In[8]:

#game loop
print("game starts")
Snake_time=time.time()

while True:   
    
    #Ordinary display
    displaysurf.fill(WHITE)
    pygame.draw.line(displaysurf,BLACK,(0,dim),(dim,dim))
    displaysurf.blit(game_name,(10,dim+10))
    game_score= myfont2.render('Score: '+str(score), False, (0, 0, 0))
    displaysurf.blit(game_score,(10,dim+40))
    now=time.time()
    game_time= myfont2.render('Time: '+str(int(now-Snake_time)), False, (0, 0, 0))
    displaysurf.blit(game_time,(10,dim+70))
    game_attempt= myfont2.render('Attempt: '+str(attempt), False, (0, 0, 0))
    displaysurf.blit(game_attempt,(10,dim+100))
    game_subject= myfont2.render('Subject: '+subject[0], False, (0, 0, 0))   
    displaysurf.blit(game_subject,(dim2-50,dim+10))
    timedelta=now-Snake_time
    game_fitness=myfont2.render('Fitness: '+str(round(fitness,3)), False, (0, 0, 0))   
    displaysurf.blit(game_fitness,(dim2-50,dim+40))
    game_hamb=myfont2.render('Hamb eaten: '+str(hamb), False, (0, 0, 0))   
    displaysurf.blit(game_hamb,(dim2-50,dim+70))
    
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
                emiliaSnake.addBlock()
                gameOverFlag=False
                attempt_flag=True
                food_time=time.time()
                subject=pool.get_subj()
                neural_net=CreateNeuralNet(subject[1])
                
            elif event.key==K_n:
                pygame.quit()
                sys.exit()
    
    framecount=(framecount+1)%2
    fitness=timedelta*(score+1)
    fooddelta=now-food_time
    if(fooddelta>=timeout):
        emiliaSnake.alive=False
    
    #emilia motion
    if(emiliaSnake.isAlive()):
        
        
        if(framecount==0):
            atr1,atr2,atr3=emiliaSnake.getAtr()
            ang,_= foodPos(emiliaSnake,foood)
            ang=int(ang)
            features=[[atr1,atr2,atr3,ang]] 
            
            mv=session.run(neural_net,feed_dict={x:features})-1
            if(orientation=='u' and mv==1):
                orientation='r'
            elif(orientation=='r' and mv==-1):
                orientation='u'
            else:
                orientation=numbOri(mv+oriNumb(orientation))
            
        emiliaSnake.move(orientation)
        emiliaSnake.move(orientation)
    
    if(not emiliaSnake.isAlive()):
        gameOverFlag=True
        
        #displaysurf.blit(gameoverImg, (int((dim-gameoverImg.get_width())/2),(int((dim-gameoverImg.get_height())/2)-50)))
        #pygame.display.update()
        score=0
        if(attempt_flag):
            attempt+=1
            attempt_flag=False
            pool.set_fitness(fitness)
        
        #### Automated Evolution ##########
        emiliaSnake = Snake(int(dim/2),int(dim/2),emiliaImg)
        emiliaSnake.createWalls(dim)
        emiliaSnake.bodyImg=subaroImg
        emiliaSnake.addBlock()
        gameOverFlag=False
        attempt_flag=True
        subject=pool.get_subj()
        
        t1=time.time()
        if(t1-garbage_time>360):
            print("Restarting... gg")
            pygame.quit()
            sys.exit()
        

        neural_net=CreateNeuralNet(subject[1])
        Snake_time=time.time()
        food_time=time.time()
        
    if(emiliaSnake.eaten(foood)):
        
        foood=newFood(foodImg,dim)
        score+=1
        hamb+=1
        food_time=time.time()
        emiliaSnake.addBlock()
    
    if(not gameOverFlag):
        
        renderSnake(displaysurf,emiliaSnake)
        renderFood(displaysurf,foood)
        pygame.display.update()
        

    

            

