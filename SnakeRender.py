import pygame,sys
from pygame.locals import *
from Snake import Snake
from food import food
from random import randint
import math
import numpy as np

def renderSnake(display,snake):
    
    headImg=snake.headImg
    bodyImg=snake.bodyImg
    
    #add head
    display.blit(headImg,snake.head.get_render_rect())
    
    #add body
    for body in snake.blocks:
        display.blit(bodyImg,body.get_render_rect()) 
        

def renderFood(display,food):
    
    display.blit(food.image,food.rect)

def newFood(foodImg,dim):
    
    fos=5
    return food(randint(fos,(dim-foodImg.get_width()-fos)),randint(fos,(dim-foodImg.get_height()-fos)),foodImg)

def foodPos(snake,food):
    
    hip=math.sqrt((snake.head.rect.x-food.rect.x)**2+(snake.head.rect.y-food.rect.y)**2)
    cat=0
    if(snake.orientation=='r'):
        cat=food.rect.x-snake.head.rect.x
        if(food.rect.y>=snake.head.rect.y):
            return (360-math.degrees(np.arccos(cat/hip))),hip
        else:
            return math.degrees(np.arccos(cat/hip)),hip

    elif(snake.orientation=='l'):
        cat=snake.head.rect.x-food.rect.x
        if(food.rect.y<=snake.head.rect.y):
            return (360-math.degrees(np.arccos(cat/hip))),hip
        else:
            return math.degrees(np.arccos(cat/hip)),hip
    
    elif(snake.orientation=='u'):
        cat=snake.head.rect.y-food.rect.y
        if(food.rect.x<=snake.head.rect.x):
            return (360-math.degrees(np.arccos(cat/hip))),hip
        else:
            return math.degrees(np.arccos(cat/hip)),hip
    
    elif(snake.orientation=='d'):
        cat=food.rect.y-snake.head.rect.y
        if(food.rect.x>=snake.head.rect.x):
            return (360-math.degrees(np.arccos(cat/hip))),hip
        else:
            return math.degrees(np.arccos(cat/hip)),hip
     