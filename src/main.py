import os
import random
import math
import sys
import pygame
from pygame.locals import *
from config import *
from os import listdir
from os.path import isfile, join
from buttons import Button
from levels import *


pygame.init()
clock = pygame.time.Clock()

# -- SCREEN CONFIG --
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcane Explorer: Crystal Chamber Clash")


# ------- IMAGES -------
bg_image = pygame.image.load(
    join("src", "assets", "images", "background", "bg_img.jpg"))
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# botones
start_btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "start.png")).convert_alpha()

start_hover__btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "start_hover.png")).convert_alpha()

levels_btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "levels.png")).convert_alpha()

levels_btn_hover_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "levels_hover.png")).convert_alpha()

quit_btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "quit.png")).convert_alpha()

quit_btn_hover_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "quit_hover.png")).convert_alpha()

back_to_menu_btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "back_to_menu.png")).convert_alpha()

back_to_menu_btn_hover_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "back_to_menu_hover.png")).convert_alpha()

next_level_btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "next_level.png")).convert_alpha()

next_level_btn_hover_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "next_level_hover.png")).convert_alpha()

music_btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "music_btn.png")).convert_alpha()

sound_btn_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "sound_btn.png")).convert_alpha()

#  poderes
player_shoot_img = pygame.transform.scale(pygame.image.load(
    "./src/assets/images/powers/light_blue.png").convert_alpha(), (30, 30))

boss_shoot_img = pygame.transform.scale(pygame.image.load(
    "./src/assets/images/powers/red.png").convert_alpha(), (50, 50))


# ------- SOUNDS -------
gemas_sound = pygame.mixer.Sound("./src/assets/sounds/gemas.mp3")
game_over_sound = pygame.mixer.Sound("./src/assets/sounds/game_over.mp3")
life_sound = pygame.mixer.Sound("./src/assets/sounds/vida_extra.mp3")
hurt_sound = pygame.mixer.Sound("./src/assets/sounds/colision.mp3")
player_shoot_sound = pygame.mixer.Sound("./src/assets/sounds/disparo_mago.mp3")
boss_shoot_sound = pygame.mixer.Sound("./src/assets/sounds/disparo_boss.mp3")
jump_sound = pygame.mixer.Sound("./src/assets/sounds/jump.mp3")
next_level_sound = pygame.mixer.Sound("./src/assets/sounds/next_level.mp3")


# ------- FUENTES -------
fuente = pygame.font.Font("./src/assets/fonts/scorefont.ttf", 36)
fuente_title = pygame.font.SysFont("Bowlby One SC", 58)
fuente_game_over = pygame.font.SysFont("Bowlby One SC", 85)


# ------- FUNCIONES -------
def draw_grid():
    for line in range(0, 30):
        pygame.draw.line(screen, (255, 255, 255), (0, line *
                         tile_size), (WIDTH, line*tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line *
                         tile_size, 0), (line*tile_size, HEIGHT))


def draw_player(player):
    player.draw(screen)


def draw_boss(boss):
    boss.draw(screen)


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheet(dir1, dir2, width_sprite, height_sprite, direction=False):
    path = join("src", "assets", dir1, dir2)
    # it loads every file inside the directory (it loads attack, run, idle, hurt, etc from wizard)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width_sprite):
            surface = pygame.Surface(
                (width_sprite, height_sprite), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width_sprite, 0,
                               width_sprite, height_sprite)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(surface)
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def getHighestScore():
    with open("highest_score.txt", "r") as file:
        return file.read()


def main_menu():
    start_btn = Button(WIDTH // 2 - 100, 250,
                       start_btn_img, start_hover__btn_img)
    levels_btn = Button(WIDTH // 2 - 100, 340,
                        levels_btn_img, levels_btn_hover_img)
    quit_btn = Button(WIDTH // 2 - 100, 430, quit_btn_img, quit_btn_hover_img)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame. MOUSEBUTTONDOWN:
                if start_btn.is_clicked():
                    countdown()
                    return "start game"
                if quit_btn.is_clicked():
                    pygame.quit()
                    sys.exit()

        screen.blit(bg_image, (0, 0))

        text_title = fuente_title.render(
            "Arcane explorer: Crystal Chamber Clash", True, white)
        rect_text_title = text_title.get_rect(topleft=(20, 80))
        screen.blit(text_title, rect_text_title)

        start_btn.draw(screen)
        levels_btn.draw(screen)
        quit_btn.draw(screen)
        pygame.display.flip()


def game_over(player):
    game_over_sound.play()
    highest_score = int(getHighestScore())
    back_btn = Button(WIDTH//2 - 100, HEIGHT - 200,
                      back_to_menu_btn_img, back_to_menu_btn_hover_img)

    while True:
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame. MOUSEBUTTONDOWN:
                if back_btn.is_clicked():
                    player.lives = 3
                    main_menu()

        back_btn.draw(screen)
        text_game_over = fuente_game_over.render(
            "Game Over", True, (255, 255, 255))
        screen.blit(text_game_over, (WIDTH // 2 - 260, 90))

        screen_score = pygame.Rect(415, 230, 600, 300)
        pygame.draw.rect(screen, (201, 57, 165),
                         screen_score, border_radius=10)

        text_score = fuente.render(
            f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(text_score, (WIDTH // 2 - 240, 250))

        if highest_score < player.score:
            highest_score = player.score

        with open("highest_score.txt", "w") as file:
            file.write(str(highest_score))
        text_highest_score = fuente.render(
            f"Highest score: {highest_score}", True, (255, 255, 255))
        screen.blit(text_highest_score, (WIDTH // 2 - 240, 300))

        pygame.display.flip()


def you_won(player):
    fuente_winner = pygame.font.SysFont("Bowlby One SC", 70)
    highest_score = int(getHighestScore())
    back_btn = Button(WIDTH//2 - 100, HEIGHT - 200,
                      back_to_menu_btn_img, back_to_menu_btn_hover_img)

    while True:
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame. MOUSEBUTTONDOWN:
                if back_btn.is_clicked():
                    player.lives = 3
                    main_menu()

        back_btn.draw(screen)
        text_winner = fuente_game_over.render(
            "Congratulations! you won", True, (255, 255, 255))
        screen.blit(text_winner, (78, 90))

        screen_score = pygame.Rect(415, 230, 600, 300)
        pygame.draw.rect(screen, (201, 57, 165),
                         screen_score, border_radius=10)

        text_score = fuente.render(
            f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(text_score, (WIDTH // 2 - 240, 250))

        if highest_score < player.score:
            highest_score = player.score

        with open("highest_score.txt", "w") as file:
            file.write(str(highest_score))
        text_highest_score = fuente.render(
            f"Highest score: {highest_score}", True, (255, 255, 255))
        screen.blit(text_highest_score, (WIDTH // 2 - 240, 300))

        pygame.display.flip()


def score_screen(player):
    back_btn = Button(WIDTH//2 - 250, HEIGHT - 200,
                      back_to_menu_btn_img, back_to_menu_btn_hover_img)
    next_level_btn = Button(WIDTH//2, HEIGHT - 200,
                            next_level_btn_img, next_level_btn_hover_img)

    run = True

    while run:
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame. MOUSEBUTTONDOWN:
                if back_btn.is_clicked():
                    main_menu()
                if next_level_btn.is_clicked():
                    run = False

        back_btn.draw(screen)
        next_level_btn.draw(screen)

        screen_score = pygame.Rect(415, 230, 600, 300)
        pygame.draw.rect(screen, (201, 57, 165),
                         screen_score, border_radius=10)

        text_score = fuente.render(
            f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(text_score, (WIDTH // 2 - 240, 250))

        pygame.display.flip()


def countdown():
    time_level = 60
    # Actualizar el cronómetro
    current_time = pygame.time.get_ticks() / 1000  # Tiempo en segundos
    time_left = time_level - int(current_time)

    # Mostrar el contador en la ventana

    countdown_rect = pygame.Rect(WIDTH // 2 - 6, 10, 90, 42)

    font = pygame.font.Font(None, 40)
    text = font.render(f"00:{time_left}", True, (255, 255, 255))

    pygame.draw.rect(screen, (201, 57, 165), countdown_rect, border_radius=5)
    screen.blit(text, (WIDTH // 2, 18))

    return time_left


# -- CLASSES --


class Level():
    def __init__(self, level) -> None:
        self.tile_list = []
        # load images
        stone_img = pygame.image.load(
            join("src", "assets", "images", "platforms", "stone_img.png"))

        self.enemies_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.crystals_group = pygame.sprite.Group()
        self.finish_door_group = pygame.sprite.Group()
        self.torch_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        row_count = 0
        for row in level:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(
                        stone_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    lava_floor = Lava(col_count*tile_size,
                                      row_count*tile_size)
                    self.lava_group.add(lava_floor)
                    self.all_sprites.add(lava_floor)
                if tile == 3:
                    enemy = Enemy(col_count*tile_size,
                                  row_count*tile_size + 17, 64, 52)
                    self.enemies_group.add(enemy)
                    self.all_sprites.add(enemy)
                if tile == 4:
                    corazon_crystal = Crystal("corazon.png", col_count*tile_size,
                                              row_count*tile_size + 17)
                    self.crystals_group.add(corazon_crystal)
                    self.all_sprites.add(corazon_crystal)
                if tile == 5:
                    diamante_crystal = Crystal("diamante.png", col_count*tile_size,
                                               row_count*tile_size + 17)
                    self.crystals_group.add(diamante_crystal)
                    self.all_sprites.add(diamante_crystal)
                if tile == 6:
                    rombo_crystal = Crystal("rombo.png", col_count*tile_size,
                                            row_count*tile_size + 17)
                    self.crystals_group.add(rombo_crystal)
                    self.all_sprites.add(rombo_crystal)
                if tile == 7:
                    triple_crystal = Crystal("triple.png", col_count*tile_size,
                                             row_count*tile_size + 17)
                    self.crystals_group.add(triple_crystal)
                    self.all_sprites.add(triple_crystal)
                if tile == 8:
                    finish_door = FinishDoor(col_count*tile_size,
                                             row_count*tile_size)
                    self.finish_door_group.add(finish_door)
                    self.all_sprites.add(finish_door)

                if tile == 9:
                    torch_trap = Trap(col_count*tile_size,
                                      row_count*tile_size)
                    self.torch_group.add(torch_trap)
                    self.all_sprites.add(torch_trap)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheet("images", "wizard", 64, 58, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.x_vel = 0
        self.y_vel = 0
        self.jumped = False
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0  # how long we've been falling

        self.colisiones_previas = set()
        self.colision_lava = None
        self.colision_crystals = None
        self.colisiones_previas_antorcha = set()

        self.new_level = 1

        self.score = 0
        self.lives = 3

    def handle_move(self):
        desp_y = 0
        desp_x = 0

        keys = pygame.key.get_pressed()

        self.x_vel = 0
        if keys[pygame.K_LEFT]:
            self.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT]:
            self.move_right(PLAYER_VEL)
        if keys[pygame.K_SPACE] and self.jumped == False:
            jump_sound.play()
            self.y_vel = -15
            self.jumped = True
        if keys[pygame.K_SPACE] == False:
            self.jumped = False

        # add gravity
        self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)
        desp_y += self.y_vel

        # limites de la pantalla
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        # check collision with platforms
        for tile in current_level.tile_list:
            # direccion horizontal
            if tile[1].colliderect(self.rect.x + desp_x, self.rect.y, self.width, self.height):
                self.move(0, desp_y)

            # direccion vertical
            if tile[1].colliderect(self.rect.x, self.rect.y + desp_y, self.width, self.height):
                if desp_y < 0:  # pego desde abajo (jump)
                    desp_y = tile[1].bottom - self.rect.top
                    self.y_vel = 0
                elif desp_y > 0:  # pego desde arriba (fall)
                    desp_y = tile[1].top - self.rect.bottom
                    self.y_vel = 0

    def check_collision(self, level):
        # --check collision with enemies
        colision_enemigo = pygame.sprite.groupcollide(
            player_group, level.enemies_group, False, False)
        colisiones_nuevas = {player for player in colision_enemigo.keys(
        ) if player not in self.colisiones_previas}
        for _ in colisiones_nuevas:
            if self.lives > 0:
                self.lives -= 1
                hurt_sound.play()

            # Guardar las colisiones actuales como previas para la próxima iteración
        self.colisiones_previas = colision_enemigo.copy()

        # -- check collision with torch

        colision_antorcha = pygame.sprite.groupcollide(
            player_group, level.torch_group, False, False)

        colisiones_nuevas_antorcha = {player for player in colision_antorcha.keys(
        ) if player not in self.colisiones_previas_antorcha}
        for _ in colisiones_nuevas_antorcha:
            if self.lives > 0:
                self.lives -= 1
                hurt_sound.play()

            # Guardar las colisiones actuales como previas para la próxima iteración
        self.colisiones_previas_antorcha = colision_antorcha.copy()

        # --check collision with lava
        self.colision_lava = pygame.sprite.groupcollide(
            player_group, level.lava_group, False, False)

        if self.colision_lava:
            self.lives = 0

        # --check colision with crystals
        self.colision_crystals = pygame.sprite.groupcollide(
            level.crystals_group, player_group, True, False)

        for crystal in self.colision_crystals:
            if crystal.img_name == "corazon.png":
                self.lives += 1
                life_sound.play()
            elif crystal.img_name == "diamante.png":
                self.score += 75
                gemas_sound.play()
            elif crystal.img_name == "rombo.png":
                self.score += 50
                gemas_sound.play()
            elif crystal.img_name == "triple.png":
                self.score += 100
                gemas_sound.play()

        # -- check collide with boss powers
        colision_powers = pygame.sprite.spritecollide(
            self, powers_group_boss, True)

        if colision_powers:
            self.lives -= 1
            hurt_sound.play()

        # -- check collision with finish door

        if pygame.sprite.spritecollide(self, level.finish_door_group, False):
            score_screen(self)
            self.new_level += 1
        return self.new_level

    def move(self, desp_x, desp_y):  # update player coordenates
        self.rect.x += desp_x
        self.rect.y += desp_y

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self):
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        self.sprite_sheet = "idle"
        if self.x_vel != 0:
            self.sprite_sheet = "run"

        if self.y_vel != 0:
            self.sprite_sheet = "jump"

        if self.lives < 1:
            self.sprite_sheet = "die"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            self.sprite_sheet = "attack"

        if keys[pygame.K_SPACE]:
            self.sprite_sheet = "jump"

        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def shoot(self):
        player_shoot_sound.play()
        if self.direction == "right":
            Powers(player_shoot_img, [powers_group_player],
                   self.rect.midright, self.direction)
            # Powers([powers_group], self.rect.midright, self.direction)
        elif self.direction == "left":
            Powers(player_shoot_img, [powers_group_player],
                   self.rect.midleft, self.direction)

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))


class Enemy(Player):
    GRAVITY = 1
    SPRITES = load_sprite_sheet("images", "enemy", 64, 52, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.x_vel = 2
        self.y_vel = 0
        self.image = pygame.Surface((width, height), SRCALPHA, 32)
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.move_direction = 1
        self.move_counter = 1
        self.colision_powers = None

    def handle_move(self, player, level):
        desp_y = 0
        desp_x = 0
        keys = pygame.key.get_pressed()

        self.x_vel = 0
        if self.move_direction < 0:
            self.move_left(2)
        if self.move_direction > 0:
            self.move_right(2)
        # check collision
        for tile in current_level.tile_list:
            # direccion horizontal
            if tile[1].colliderect(self.rect.x + desp_x, self.rect.y, self.width, self.height):
                self.move(0)
                # self.update()
            # direccion vertical
            if tile[1].colliderect(self.rect.x, self.rect.y + desp_y, self.width, self.height):
                if desp_y < 0:  # pego desde abajo (jump)
                    desp_y = tile[1].bottom - self.rect.top
                    self.y_vel = 0
                elif desp_y > 0:  # pego desde arriba (fall)
                    desp_y = tile[1].top - self.rect.bottom
                    self.y_vel = 0

        self.colision_powers = pygame.sprite.groupcollide(
            level.enemies_group, powers_group_player, True, True)

        if self.colision_powers:
            player.score += 50

    def move(self, desp_x):  # update player coordenates
        self.rect.x += desp_x

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self):
        self.move(self.x_vel)
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "walk"
        if self.x_vel != 0:
            sprite_sheet = "walk"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter = 0

        # if self.move_counter > 0:
        #     self.x_vel = 2
        # else:
        #     self.x_vel *= -1


class Boss(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheet("images", "boss", 433, 350, True)
    ANIMATION_DELAY = 7

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.rect_hit_box = pygame.Rect(350, 115, 100, 240)

        self.direction = "right"
        self.animation_count = 0
        self.shoot_timer = pygame.time.get_ticks()
        self.lives = 10

        self.sprite_temporal = pygame.sprite.Sprite()
        self.sprite_temporal.rect = self.rect_hit_box

    def check_collision(self, player):
        colision_powers = pygame.sprite.spritecollide(
            self.sprite_temporal, powers_group_player, True)

        if colision_powers:
            player.score += 100
            self.lives -= 1
            print(self.lives)

    def move(self, desp_x, desp_y):  # update player coordenates
        self.rect.x += desp_x
        self.rect.y += desp_y

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, player):
        self.update_sprite()
        self.check_collision(player)

        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer >= 3000:  # 5000 milisegundos = 5 segundos
            self.shoot()
            self.shoot_timer = current_time  # Reiniciar el temporizador

    def update_sprite(self):
        self.sprite_sheet = "attack"

        if self.lives < 2:
            self.sprite_sheet = "die"

        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def shoot(self):
        boss_shoot_sound.play()
        if self.direction == "right":
            Powers(boss_shoot_img, [powers_group_boss],
                   (self.rect_hit_box.right, 290), self.direction)
            Powers(boss_shoot_img, [powers_group_boss],
                   (self.rect_hit_box.right, 345), self.direction)
            # Powers(boss_shoot_img, [powers_group_boss],
            #        self.rect.midright, self.direction)
            Powers(boss_shoot_img, [powers_group_boss],
                   self.rect_hit_box.midbottom, "down")

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # pygame.draw.rect(screen, "orange", self.rect_hit_box, 3)
        # pygame.draw.rect(screen, "red", self.rect, 3)


class Powers(pygame.sprite.Sprite):
    def __init__(self, image,  groups, coordenadas, direction) -> None:
        super().__init__(groups)

        self.image = image

        self.rect = self.image.get_rect(midbottom=coordenadas)
        self.speed_x = 5
        self.speed_y = 5
        self.direction = direction

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed_x
        elif self.direction == "left":
            self.rect.x -= self.speed_x
        elif self.direction == "down":
            self.rect.y += self.speed_y


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            join("src", "assets", "images", "platforms", "lava_floor_img.png")), (tile_size, tile_size))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Crystal(pygame.sprite.Sprite):
    def __init__(self, img_name, x, y) -> None:
        super().__init__()

        self.img_name = img_name
        self.image = pygame.transform.scale(pygame.image.load(
            join("src", "assets", "images", "crystals", img_name)), (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            join("src", "assets", "images", "traps", "torch3.png")), (tile_size, tile_size))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class FinishDoor(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            join("src", "assets", "images", "finish_door.png")), (tile_size, tile_size))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# CREO GRUPO DE SPRITES
player_group = pygame.sprite.Group()
powers_group_player = pygame.sprite.Group()

boss_group = pygame.sprite.Group()
powers_group_boss = pygame.sprite.Group()


# -- INSTANCIO CLASES --
player = Player(100, HEIGHT - tile_size, 64, 58)
player_group.add(player)
boss = Boss(200, 100, 64, 58)
level_1 = Level(level_1_map)
level_2 = Level(level_2_map)
level_3 = Level(level_3_map)
level_4 = Level(level_4_map)

# -- SETEO VARIABLES INICIALES
run = True
time_level = 60


current_level = None
level = 1


# Musica de fondo
pygame.mixer.music.load("./src/assets/sounds/fondo.mp3")
pygame.mixer.music.play(-1)

playing_music = True


def blit_text(screen, texto, fuente, color, coordenada):
    render_texto = fuente.render(texto, True, color)
    rect_texto = render_texto.get_rect()
    rect_texto.center = coordenada
    screen.blit(render_texto, rect_texto)


def wait_user():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                return


##############################################
while True:

    if main_menu() == "start game":

        while run and time_level > 0:
            clock.tick(FPS)
            screen.blit(bg_image, (0, 0))
            if level == 1:
                current_level = level_1
            elif level == 2:
                current_level = level_2
            elif level == 3:
                current_level = level_3
            elif level == 4:
                current_level = level_4
                boss.loop(player)
                draw_boss(boss)

            current_level.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_x:
                        player.shoot()

            # text vidas y score
            text_lives = fuente.render(f"Lives: {player.lives}", True, white)
            rect_text_lives = text_lives.get_rect(topleft=(30, 20))
            screen.blit(text_lives, rect_text_lives)

            text_score = fuente.render(f"Score: {player.score}", True, white)
            rect_text_score = text_score.get_rect(topleft=(200, 20))
            screen.blit(text_score, rect_text_score)

            if current_level == level_4:
                text_lives_boss = fuente.render(
                    f"Lives enemy: {boss.lives}", True, white)
                rect_text_boss_lives = text_lives_boss.get_rect(
                    topleft=(WIDTH - 410, 20))
                screen.blit(text_lives_boss, rect_text_boss_lives)

            # botones musica y  sonido
            music_btn = Button(WIDTH - 160, 20, music_btn_img, music_btn_img)
            sound_btn = Button(
                WIDTH - 90, 20, sound_btn_img, sound_btn_img)

            music_btn.draw(screen)
            sound_btn.draw(screen)

            if music_btn.is_clicked():
                if playing_music:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

                playing_music = not playing_music

            # draw_grid()
            player.loop()
            player.handle_move()

            powers_group_player.draw(screen)
            powers_group_player.update()
            powers_group_boss.draw(screen)
            powers_group_boss.update()

            for enemy in current_level.enemies_group:
                enemy.loop()
                enemy.handle_move(player, current_level)

            current_level.lava_group.draw(screen)
            current_level.crystals_group.draw(screen)
            current_level.enemies_group.draw(screen)
            current_level.torch_group.draw(screen)
            current_level.finish_door_group.draw(screen)

            level = player.check_collision(current_level)

            draw_player(player)

            pygame.display.flip()

            if boss.lives < 1:
                you_won(player)

            if player.lives < 1:
                game_over(player)
