#body
import pygame,sys
from pygame.locals import *
from SnakeTools import *
        
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
               