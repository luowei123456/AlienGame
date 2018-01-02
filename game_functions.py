import sys

from bullet import Bullet
from alien import Alien,Alien_1
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



    if ship.shooting:
        if ship.shooting_count == 0:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

        ship.shooting_count += 1
        if ship.shooting_count > ai_settings.bullet_shoot_factor:
            ship.shooting_count=0




def update_screen(ai_settings, screen,ship,aliens,bullets,aliens_1):
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    aliens.draw(screen)
    aliens_1.draw(screen)

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

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def update_aliens(ai_settings,screen,ship,aliens):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        create_fleet(ai_settings,screen,aliens)



def create_fleet_1(ai_settings,screen,aliens_1):
    alien_1=Alien_1(ai_settings,screen)
    alien_1_width=alien_1.rect.width
    alien_1_height=alien_1.rect.height
    number_aliens_1_x=2
    number_aliens_1_y=2

    for row_number in range(number_aliens_1_y):
        for alien_1_number in range(number_aliens_1_x):
            alien_1=Alien_1(ai_settings,screen)
            alien_1.x=alien_1_width+2*alien_1_width*alien_1_number
            alien_1.y=alien_1_height+2*alien_1_height*row_number
            alien_1.rect.x=alien_1.x
            alien_1.rect.y=alien_1.y
            aliens_1.add(alien_1)

def change_fleet_direction_1(ai_settings,aliens_1):
    for alien_1 in aliens_1.sprites():
        alien_1.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def check_fleet_edges_1(ai_settings,aliens_1):
    for alien_1 in aliens_1.sprites():
        if alien_1.check_edges_1():
            change_fleet_direction_1(ai_settings,aliens_1)
            break

def update_aliens_1(ai_settings,screen,ship,aliens_1):
    check_fleet_edges_1(ai_settings,aliens_1)
    aliens_1.update()
    if pygame.sprite.spritecollideany(ship,aliens_1):
        create_fleet_1(ai_settings,screen,aliens_1)


def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,aliens_1):
    stats.ship_left-=1
    aliens_1.empty()
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings,screen,aliens)
    create_fleet_1(ai_settings,screen,aliens_1)
    ship.center_ship()
    sleep(0.5)


def update_bullets(aliens,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    # print(len(bullets))