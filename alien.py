import  pygame

from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self,ai_settings,screen):
        super().__init__()
        self.ai_setting=ai_settings
        self.screen=screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

        self.type='h'
        self.h_speed=0.0
        self.v_speed=0.0
        self.direction=1

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def update(self):
        self.move_pattern()

    def move_pattern(self):
        self.x+=(self.h_speed*self.direction)
        self.rect.x=self.x

        if self.type != 'z':
            self.y+=(self.v_speed)
            self.rect.y=self.y


    def check_edge_z(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True

        return False

    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.left>=screen_rect.right:
            return True
        elif self.rect.right<=0:
            return True
        elif self.rect.bottom<=0:
            return True
        elif self.rect.top>=screen_rect.bottom:
            return True
        return False

