import pygame
from sys import exit
import time
import random
pygame.font.init()
pygame.init()
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("/Users/hardikshah/Desktop/shooting_game_pygame/retro-laser-1-236669.mp3")
shoot_sound.set_volume(0.3)
w = 500
h = 800
chances = 3
game_state = "menu"
main_font = pygame.font.SysFont("timesnewroman", 30)
player_spaceship = pygame.transform.scale(pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/Screenshot_2025-12-12_at_9.29.05_PM-removebg-preview.png"), (100, 100)) 
#enemies
blue_enemy_spaceship = pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/pixel_ship_blue_small.png")
red_enemy_spaceship = pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/pixel_ship_red_small.png")
green_enemy_spaceship = pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/pixel_ship_green_small.png")
#bg
background = pygame.transform.scale(pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/background-black.png"), (w, h))
#bullets
red_laser = pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/pixel_laser_red.png")
blue_laser = pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/pixel_laser_blue.png")
player_laser = pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/pixel_laser_yellow.png")
green_laser = pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/assets/pixel_laser_green.png")
title_image = pygame.transform.scale(pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/Screenshot_2025-12-14_at_9.09.28_AM-removebg-preview.png"), (w, 200))
player_bullet_mask = pygame.mask.from_surface(player_laser)
enemy_bullet_mask = pygame.mask.from_surface(red_laser)
loosing_bg = pygame.transform.scale(pygame.image.load("/Users/hardikshah/Desktop/shooting_game_pygame/Screenshot_2025-12-14_at_11.26.42_AM-removebg-preview.png"), (w, 200))

class Player():
    def __init__(self, x, y, img, laser):
        self.x = x
        self.y = y
        self.img = img
        self.laser = laser
        self.cooldown = 0
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.img)
        self.bullets = []
        self.bullet_speed = 8
        self.cool_down = 0
        self.max_health = 100
        self.health = 100
        self.enemy_kC = 0
        self.bx = 0
        self.by = 0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def lasers(self):
        if self.cool_down == 0:
            bx = self.x+self.img.get_width()//2 - self.laser.get_width()//2
            by = self.y
            self.bullets.append([bx, by])
            shoot_sound.play()
            self.cool_down = 20

    def cool_down_dec(self):
        if self.cool_down > 0:
            self.cool_down -= 1

    def laser_movement(self):
        for bullet in self.bullets[:]:
            bullet[1] -= self.bullet_speed
            if bullet[1] < 0:
                self.bullets.remove(bullet)

    #adding health bar toe the player
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y+self.img.get_height()+10, self.img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y+self.img.get_height()+10, self.img.get_width() * (1 - ((self.max_health - self.health)/self.max_health)), 10))


class Enemies():
    enemy_attributes = {
        "red" : [red_enemy_spaceship, red_laser],
        "blue" : [blue_enemy_spaceship, blue_laser],
        "green" : [green_enemy_spaceship, green_laser]
    }
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.speed = 3
        self.img = self.enemy_attributes[colour][0]
        self.laser = self.enemy_attributes[colour][1]
        self.mask = pygame.mask.from_surface(self.img)
        self.bullets = []
        self.cool_down = 0
        self.bx = 0
        self.by = 0
        self.bullet_speed = 5

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def movement(self):
        self.y += self.speed

    def off_screen(self):
        return self.y > h

    def shoot(self):
        if self.cool_down == 0:
            bx = self.x+self.img.get_width()//2 - self.laser.get_width()//2
            by = self.y

            self.bullets.append([bx, by])
            self.cool_down = 60

    def coool_down_control(self):
        if self.cool_down > 0:
            self.cool_down -= 1

    def laser_movement(self):
        for bullet in self.bullets[:]:
            bullet[1] += self.bullet_speed
            if bullet[1] > h:
                self.bullets.remove(bullet)
    
player = Player(300, 650, player_spaceship, player_laser)
enemies = []
batch_size = 5
def loosing_window(font):
    screen.fill((0, 0, 0))
    replay_label = font.render("Press any Key to play again.", 1, (255, 255, 255))
    stats_label = font.render(f"Total Enemies Killed : {player.enemy_kC}", 1, (255, 255, 255))
    screen.blit(loosing_bg, ((w/2 - loosing_bg.get_width()/2, 100)))
    screen.blit(stats_label, ((w/2 - stats_label.get_width()/2, 350)))
    screen.blit(replay_label, ((w/2 - replay_label.get_width()/2, 450)))
    pygame.display.update()

def reset_game():
    global chances, enemies
    chances = 3
    enemies.clear()
    player.health = player.max_health
    player.enemy_kC = 0
    player.bullets.clear()
    player.x, player.y = 300, 650


def draw(chances):
    screen.blit(background, (0, 0))

    if len(enemies) == 0:
        for lp_counter in range(batch_size):
            enemy_color = random.choice(["red", "blue", "green"])
            enemy = Enemies(random.randrange(100, w-100), random.randrange(-1500, -100), enemy_color)
            enemies.append(enemy)

    for enemy in enemies:
        enemy.movement()
        enemy.draw(screen)

        if enemy.off_screen():
            enemies.remove(enemy)

            chances -= 1
        enemy.coool_down_control()
        if enemy.y > 0 and enemy.y < h:
            enemy.shoot()
        enemy.laser_movement()
        for bullets in enemy.bullets[:]:
            screen.blit(enemy.laser, [bullets[0], bullets[1]])


    for bullet in player.bullets:
        screen.blit(player.laser, [bullet[0], bullet[1]])
    
    for enemy in enemies[:]:
        for bullet in player.bullets[:]:
            if enemy.y>0 and enemy.y<h:
                offset_x = enemy.x - bullet[0]
                offset_y = enemy.y - bullet[1]

                #when player bullets hit enemy
                if enemy.mask.overlap(player_bullet_mask, (offset_x, offset_y)):
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    player.enemy_kC += 1
                    break

    #when bullets hit player
    for enemy in enemies:
        for bullet in enemy.bullets[:]:
            ox = player.x - bullet[0]
            oy = player.y - bullet[1]
            if player.mask.overlap(enemy_bullet_mask, (ox, oy)):
                enemy.bullets.remove(bullet)
                player.health -= 5
                break #so that same bullet is not removed from the list again so it doenst crash

    #player hitting enemies
    for enemy in enemies[:]:
        ox = player.x - enemy.x
        oy = player.y - enemy.y
        if player.mask.overlap(enemy.mask, (ox, oy)):
            enemies.remove(enemy)
            print("hit")
            player.health -= 10
            break

    label_enemy_kill_count = main_font.render(f"Kill Count : {player.enemy_kC}", 1, (255, 255, 255))
    screen.blit(label_enemy_kill_count, (w-10 - label_enemy_kill_count.get_width(), 10))
    player.healthbar(screen)
    label = main_font.render(f"Chances : {chances}", 1, (255, 255, 255))
    screen.blit(label, (10, 10))
    player.draw(screen)
    pygame.display.update()
    return chances

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

def main():
    global chances, game_state
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_state == "menu" and event.type == pygame.KEYDOWN:
                game_state = "playing"
            
            if game_state == "lose" and event.type == pygame.KEYDOWN:
                reset_game()
                game_state = "playing"
        if game_state == "menu":
            main_menu()
        if game_state == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player.speed > 0:
                player.x -= player.speed
            if keys[pygame.K_d] and player.x + player.speed + player_spaceship.get_width()< w:
                player.x += player.speed
            if keys[pygame.K_w] and player.y - player.speed > 0:
                player.y -= player.speed
            if keys[pygame.K_s] and player.y + player.speed + player_spaceship.get_height() +15 < h:
                player.y += player.speed
            player.cool_down_dec()

            if keys[pygame.K_SPACE]:
                player.lasers()
            player.laser_movement()
            chances = draw(chances)
        
            if chances <= 0 or player.health == 0:
                game_state = "lose"

        if game_state == "lose":
            loosing_window(main_font)

        clock.tick(60)

def main_menu():
    heading_font = pygame.font.SysFont("timesnewroman", 20)

    screen.blit(background, (0, 0))
    title_lable = heading_font.render("Press any Key to start the game..", 1, (255, 255, 255))
    screen.blit(title_lable, (w/2 - title_lable.get_width()/2, 600))
    screen.blit(title_image, (w/2 - title_image.get_width()/2, 100))
    pygame.display.update()

main()
