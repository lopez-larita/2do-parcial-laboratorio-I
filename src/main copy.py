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


pygame.init()
clock = pygame.time.Clock()

# -- SCREEN CONFIG --
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")


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

nexi_level_btn_hover_img = pygame.image.load(
    join("src", "assets", "images", "buttons", "next_level_hover.png")).convert_alpha()


# ------- SOUNDS -------


# ------- FUENTES -------
fuente = pygame.font.Font("./src/assets/fonts/scorefont.ttf", 36)


# ------- FUNCIONES -------
def draw_grid():
    for line in range(0, 30):
        pygame.draw.line(screen, (255, 255, 255), (0, line *
                         tile_size), (WIDTH, line*tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line *
                         tile_size, 0), (line*tile_size, HEIGHT))


def draw_screen(player):
    player.draw(screen)
    # enemy.draw(screen)
    pygame.display.flip()


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
                    return "start game"
                if quit_btn.is_clicked():
                    pygame.quit()
                    sys.exit()

        screen.blit(bg_image, (0, 0))
        start_btn.draw(screen)
        levels_btn.draw(screen)
        quit_btn.draw(screen)
        pygame.display.flip()


def game_over(player):
    fuente_title = pygame.font.SysFont("Bowlby One SC", 85)
    highest_score = int(getHighestScore())

    while True:
        screen.blit(bg_image, (0, 0))
        back_btn = Button(WIDTH//2 - 100, HEIGHT - 200, back_to_menu_btn_img,
                          back_to_menu_btn_hover_img)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame. MOUSEBUTTONDOWN:
                if back_btn.is_clicked():
                    player.lives = 3
                    main_menu()

        back_btn.draw(screen)
        text_game_over = fuente_title.render(
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


def score_screen(player, level, current_level):
    back_btn = Button(WIDTH//2 - 400, HEIGHT - 200,
                      back_to_menu_btn_img, back_to_menu_btn_hover_img)
    next_level_btn = Button(WIDTH//2 + 400, HEIGHT - 200,
                            back_to_menu_btn_img, back_to_menu_btn_hover_img)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame. MOUSEBUTTONDOWN:
            if back_btn.is_clicked():
                player.lives = 3
                main_menu()
            if next_level_btn.is_clicked():
                level += 1
                if level == 1:
                    current_level = Level(level_1_map)
                elif level == 2:
                    current_level = Level(level_2_map)

        back_btn.draw(screen)

        next_level_btn.draw(screen)

    screen_score = pygame.Rect(415, 230, 600, 300)
    pygame.draw.rect(screen, (201, 57, 165),
                     screen_score, border_radius=10)

    text_score = fuente.render(
        f"Score: {player.score}", True, (255, 255, 255))
    screen.blit(text_score, (WIDTH // 2 - 240, 250))

    return current_level


# -- CLASSES --

class Level():
    def __init__(self, level) -> None:
        self.tile_list = []
        # load images
        stone_img = pygame.image.load(
            join("src", "assets", "images", "platforms", "stone_img.png"))

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
                    lava_group.add(lava_floor)
                    all_sprites.add(lava_floor)
                if tile == 3:
                    enemy = Enemy(col_count*tile_size,
                                  row_count*tile_size + 17, 64, 52)
                    enemies_group.add(enemy)
                    all_sprites.add(enemy)
                if tile == 4:
                    corazon_crystal = Crystal("corazon.png", col_count*tile_size,
                                              row_count*tile_size + 17)
                    crystals_group.add(corazon_crystal)
                    all_sprites.add(corazon_crystal)
                if tile == 5:
                    diamante_crystal = Crystal("diamante.png", col_count*tile_size,
                                               row_count*tile_size + 17)
                    crystals_group.add(diamante_crystal)
                    all_sprites.add(diamante_crystal)
                if tile == 6:
                    rombo_crystal = Crystal("rombo.png", col_count*tile_size,
                                            row_count*tile_size + 17)
                    crystals_group.add(rombo_crystal)
                    all_sprites.add(rombo_crystal)
                if tile == 7:
                    triple_crystal = Crystal("triple.png", col_count*tile_size,
                                             row_count*tile_size + 17)
                    crystals_group.add(triple_crystal)
                    all_sprites.add(triple_crystal)
                if tile == 8:
                    finish_door = FinishDoor(col_count*tile_size,
                                             row_count*tile_size)
                    finish_door_group.add(finish_door)
                    all_sprites.add(finish_door)

                if tile == 9:
                    torch_trap = Trap(col_count*tile_size,
                                      row_count*tile_size)
                    torch_group.add(torch_trap)
                    all_sprites.add(torch_trap)
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
            player_group, enemies_group, False, False)
        colisiones_nuevas = {player for player in colision_enemigo.keys(
        ) if player not in self.colisiones_previas}
        for _ in colisiones_nuevas:
            if self.lives > 0:
                self.lives -= 1

            # Guardar las colisiones actuales como previas para la próxima iteración
        self.colisiones_previas = colision_enemigo.copy()

        # -- check collision with torch

        colision_antorcha = pygame.sprite.groupcollide(
            player_group, torch_group, False, False)

        colisiones_nuevas_antorcha = {player for player in colision_antorcha.keys(
        ) if player not in self.colisiones_previas_antorcha}
        for _ in colisiones_nuevas_antorcha:
            if self.lives > 0:
                self.lives -= 1

            # Guardar las colisiones actuales como previas para la próxima iteración
        self.colisiones_previas_antorcha = colision_antorcha.copy()

        # --check collision with lava
        self.colision_lava = pygame.sprite.groupcollide(
            player_group, lava_group, False, False)

        if self.colision_lava:
            self.lives = 0

        # --check colision with crystals
        self.colision_crystals = pygame.sprite.groupcollide(
            crystals_group, player_group, True, False)

        for crystal in self.colision_crystals:
            if crystal.img_name == "corazon.png":
                self.lives += 1
            elif crystal.img_name == "diamante.png":
                self.score += 75
            elif crystal.img_name == "rombo.png":
                self.score += 50
            elif crystal.img_name == "triple.png":
                self.score += 100

        # -- check collision with finish door

        if pygame.sprite.spritecollide(self, finish_door_group, False):
            level += 1
        return level

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

    def loop(self, level):
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.check_collision(level)
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
        # self.shoot_sound.play()
        if self.direction == "right":
            Powers([powers_group], self.rect.midright, self.direction)
        elif self.direction == "left":
            Powers([powers_group], self.rect.midleft, self.direction)

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

    def handle_move(self, player):
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
                self.move(0, desp_y)
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
            enemies_group, powers_group, True, True)

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


class Powers(pygame.sprite.Sprite):
    def __init__(self, groups, coordenadas, direction) -> None:
        super().__init__(groups)

        self.image = pygame.transform.scale(pygame.image.load(
            "./src/assets/images/powers/light_blue.png").convert_alpha(), (30, 30))

        self.rect = self.image.get_rect(midbottom=coordenadas)
        self.speed_x = 5
        self.direction = direction

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed_x
        elif self.direction == "left":
            self.rect.x -= self.speed_x
        # if self.rect.bottom < 0:
        #     self.kill()


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


# -- LEVELS --
level_1_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 0, 0, 3, 5, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 5, 0],
    [6, 3, 7, 6, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 7, 5, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 7, 5, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 0, 0],
    [0, 0, 6, 0, 0, 3, 7, 6, 3, 5, 7, 6, 0, 0, 0, 0, 0, 6, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1]
]

level_2_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 3, 4],
    [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 9, 0, 0, 0],
    [3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 9, 5, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 6, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 0, 3, 6, 3, 5, 9, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
]

level_3_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
]


# CREO GRUPO DE SPRITES
enemies_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
powers_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
crystals_group = pygame.sprite.Group()
finish_door_group = pygame.sprite.Group()
torch_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# -- INSTANCIO CLASES --
player = Player(100, HEIGHT - tile_size, 64, 58)
player_group.add(player)
level_1 = Level(level_1_map)
level_2 = Level(level_2_map)
# -- SETEO VARIABLES INICIALES
run = True

current_level = None
level = 1

if level == 1:
    level_1 = Level(level_1_map)

elif level == 2:
    level_2 = Level(level_2_map)


##############################################
while True:
    if main_menu() == "start game":

        while run:
            clock.tick(FPS)
            screen.blit(bg_image, (0, 0))
            if level == 1:
                current_level = level_1
            elif level == 2:
                current_level = level_2

            current_level.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_x:
                        player.shoot()

            text_lives = fuente.render(f"Lives: {player.lives}", True, white)
            rect_text_lives = text_lives.get_rect(topleft=(30, 20))
            screen.blit(text_lives, rect_text_lives)

            text_score = fuente.render(f"Score: {player.score}", True, white)
            rect_text_score = text_score.get_rect(topleft=(200, 20))
            screen.blit(text_score, rect_text_score)

            # draw_grid()
            player.loop(level)
            player.handle_move()

            powers_group.draw(screen)

            for enemy in enemies_group:
                enemy.loop()
                enemy.handle_move(player)

            powers_group.update()

            lava_group.draw(screen)
            crystals_group.draw(screen)
            enemies_group.draw(screen)
            torch_group.draw(screen)
            finish_door_group.draw(screen)

            draw_screen(player)
            level = player.check_collision(level)

            if player.lives < 1:
                game_over(player)
