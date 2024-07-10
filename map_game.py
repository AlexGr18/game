import pygame
import backgraund as size
import copy
import random

tile_width = tile_height = 60


def generate_level(data_game, tiles_group, all_sprites):
    image_surf = pygame.image.load('data/tile/surf.png')
    image_bot = pygame.image.load('data/tile/bot.png')

    row_count = 0
    for row in data_game:
        col_count = 0
        for tile in row:
            if tile == 1:
                Tile(image_surf, col_count, row_count, tiles_group, all_sprites)
            elif tile == 2:
                Tile(image_bot, col_count, row_count, tiles_group, all_sprites)
            col_count += 1
        row_count += 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_surf, pos_x, pos_y, tiles_group, all_sprites):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(image_surf, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.x < -150:
            self.rect.x += size.width + 240


class Level():
    def __init__(self, level):
        self.level = level
        self.data = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]]
        # пополе
        self.size = (10, 24)
        self.generator_map()
        # птицы (количество, скорость, измение скорости по y в случайном порядке)
        self.number_bird = [(2, (2, 0), False)]
        self.generator_bird()
        # облака (количество, скорость капли)
        self.number_cloud = [(1, 1)]
        self.generator_cloud()

    def generator_bird(self):
        for i in range(1, self.level):
            count = (self.number_bird[i - 1][0] + 1) % 11
            speed_x = random.randint(2, 2 + i) % 5
            speed_y = random.randint(1, i) % 4
            flag = True
            if count > 5:
                flag = False
                speed_y = 0
            if count == 0:
                count = random.randint(1, 6)
            if speed_x == 0:
                speed_x = random.randint(2, 5)

            self.number_bird.append((count, (speed_x, speed_y), flag))

    def generator_cloud(self):
        for i in range(1, self.level):
            count = (self.number_cloud[i - 1][0] + 1) % 5
            if i < 3:
                speed_drop = 1
            elif i < 6:
                speed_drop = 2
            if count == 0:
                count = 1
                speed_drop = 3
            self.number_cloud.append((count, speed_drop))

    def generator_map(self):
        number_hills = [0, 0, 0]
        for hill in range(3, self.level):
            if number_hills[hill - 1] < 6:
                number_hills.append(number_hills[hill - 1] + 1)
            else:
                number_hills.append(number_hills[hill - 1])
        height_hills = [1, 2, 3]
        width_hill = [10, 5, 2]

        for i in range(1, self.level):
            if i < 3:
                temp = copy.deepcopy(self.data[i - 1])
                self.data.append(temp)
                for x in range(self.size[0] - 1, self.size[0] - 1 - i, -1):
                    for y in range(self.size[1]):
                        self.data[i][x][y] = 2
                for y in range(self.size[1]):
                    self.data[i][self.size[0] - 1 - i][y] = 1
            else:
                temp = copy.deepcopy(self.data[i % 3])
                surface = self.size[0] - 1
                while temp[surface][0] != 1:
                    surface -= 1
                y_0 = random.randint(1, 10)
                height = height_hills[i % 3]
                if number_hills[i] < 3:
                    width = width_hill[0]
                elif number_hills[i] < 5:
                    width = width_hill[1]
                elif number_hills[i] < 7:
                    width = width_hill[2]
                for hill in range(number_hills[i]):
                    if y_0 + width > self.size[1]:
                        y_1 = self.size[1]
                    else:
                        y_1 = y_0 + width
                    for y in range(y_0, y_1):
                        for x in range(surface, surface - height - 1, -1):
                            temp[x][y] = 2
                        temp[surface - height][y] = 1
                    y_0 = (y_1 + width) % self.size[1]
                self.data.append(temp)
