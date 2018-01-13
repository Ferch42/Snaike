#head
import pygame,sys
from pygame.locals import *
class head(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=pygame.rect.Rect(x,y,int(img.get_width()*0.75),int(img.get_height()+0.75))
        self.orientation=''
        self.turns=[]
    
    def get_render_rect(self):
        
        return ((self.rect.x-int(self.image.get_width()*0.25)),(self.rect.y-int(self.image.get_height()*0.25)))