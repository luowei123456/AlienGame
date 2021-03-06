import sys

from bullet import Bullet
from alien import Alien
from time import sleep
import pygame

def check_events(ai_settings, screen,stats,play_button, ship, aliens,bullets):

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

        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        # elif event.key==pygame.K_LEFT:
        #         ship.rect.centerx-=1
    if ship.shooting:
        if ship.shooting_count == 0:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

        ship.shooting_count += 1
        if ship.shooting_count > ai_settings.bullet_shoot_factor:
            ship.shooting_count=0

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active=True
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,aliens)
        ship.center_ship()


def update_screen(ai_settings, screen,stats,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def create_fleet(ai_settings,screen,aliens):
    fleet_data=load_data('alienData.txt')

    alien = Alien(ai_settings, screen)
    alien_width=alien.rect.width
    alien_height=alien.rect.height

    number_aliens_x=2
    number_aliens_y=2

    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            alien=Alien(ai_settings,screen)

            alien.x=alien_width+2*alien_width*alien_number
            alien.y=alien_height+2*alien_height*row_number

            alien.rect.x=alien.x
            alien.rect.y=alien.y

            t,s = fleet_data.popitem()
            alien.type = t.strip()
            alien.h_speed = float(s[0])
            alien.v_speed = float(s[1])

            aliens.add(alien)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edge_z() and 'z' == alien.type:
            change_fleet_direction(alien)
            break

def change_fleet_direction(alien):
    alien.rect.y+=alien.v_speed
    alien.direction*=-1

def remove_aliens(aliens):
    for al in aliens.copy():
        if al.check_edges():
            aliens.remove(al)
    # print(len(aliens))

def ship_hit(ai_settings,screen,stats,ship,aliens,bullets):
    if stats.ship_left>0:
        stats.ship_left-=1
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)



def update_aliens(ai_settings,screen,stats,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    remove_aliens(aliens)

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,ship,aliens,bullets)

def update_bullets(aliens,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    # print(len(bullets))

def load_data(filename):
    result={}
    f=open(filename)
    for line in f.readlines():
        h_speed,v_speed,f_type=line.split(' ')
        print(h_speed,v_speed,f_type)
        result[f_type]=[h_speed,v_speed]
    return result

