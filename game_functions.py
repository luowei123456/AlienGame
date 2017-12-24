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
                ship.shooting=True

        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT:
                ship.moving_right=False
            elif event.key==pygame.K_LEFT:
                ship.moving_left=False
            elif event.key==pygame.K_SPACE:
                ship.shooting=False


        # elif event.key==pygame.K_LEFT:
        #         ship.rect.centerx-=1
    if ship.shooting:
        if ship.shooting_count == 0:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

        ship.shooting_count += 1
        if ship.shooting_count > ai_settings.bullet_shoot_factor:
            ship.shooting_count=0




def update_screen(ai_settings, screen,ship,alien,bullets):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    alien.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    pygame.display.flip()