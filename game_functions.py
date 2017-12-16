import sys

from bullet import Bullet

import pygame

def check_evets(ai_settings, screen, ship, bullets):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type ==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key==pygame.K_LEFT:
                ship.moving_left=True
            elif event.key==pygame.K_SPACE:
                new_bullet=Bullet(ai_settings,screen,ship)
                bullets.add(new_bullet)

        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT:
                ship.moving_right=False
            elif event.key==pygame.K_LEFT:
                ship.moving_left=False

        # elif event.key==pygame.K_LEFT:
        #         ship.rect.centerx-=1


def update_screen(ai_settings, screen,ship,alien,bullets):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    alien.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    pygame.display.flip()