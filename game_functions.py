import sys

from bullet import Bullet
from alien import Alien
from time import sleep
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
            elif event.key==pygame.K_UP:
                ship.moving_up=True
            elif event.key==pygame.K_DOWN:
                ship.moving_down=True
            elif event.key==pygame.K_SPACE:
                ship.shooting=True

        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT:
                ship.moving_right=False
            elif event.key==pygame.K_LEFT:
                ship.moving_left=False
            elif event.key==pygame.K_UP:
                ship.moving_up=False
            elif event.key==pygame.K_DOWN:
                ship.moving_down=False
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




def update_screen(ai_settings, screen,ship,aliens,bullets):
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    aliens.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    pygame.display.flip()

def create_fleet(ai_settings,screen,aliens):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien_height=alien.rect.height
    number_aliens_x=3
    number_aliens_y=3

    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            alien=Alien(ai_settings,screen)
            alien.x=alien_width+2*alien_width*alien_number
            alien.y=alien_height+2*alien_height*row_number
            alien.rect.x=alien.x
            alien.rect.y=alien.y
            aliens.add(alien)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_setttings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_setttings.fleet_drop_speed
    ai_setttings.fleet_direction*=-1

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    stats.ship_left-=1
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings,screen,aliens)
    ship.center_ship()
    sleep(0.5)


def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

def update_bullets(aliens,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    # print(len(bullets))