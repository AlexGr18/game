import pygame
import random
import backgraund as size


class Bird(pygame.sprite.Sprite):
    def __init__(self, speed, bird_sprites, all_sprites):
        super().__init__(bird_sprites, all_sprites)
        # анимация героя
        self.index = 0
        self.frames = []
        self.cut_sheet(pygame.transform.scale(pygame.image.load('data/bird/pt2.png'), (350, 200)).convert_alpha(),
                       5, 2, self.frames)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        # скорости перемещения по экрану
        self.speed_x = speed[0]
        self.speed_y = speed[1]

        self.rect.x = size.width + random.randint(50, 1000)
        self.rect.y = random.randint(10, 400)

    # для анимации объекта
    def cut_sheet(self, sheet, columns, rows, frames):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # Изменение объекта
    def update(self, variable_speed=True):
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y
        # постоянная скорость
        if self.rect.y < 5 or self.rect.y > size.height - 300:
            self.speed_y *= -1
        if self.rect.x < 0:
            self.kill()
        # смена кадров
        self.cur_frame = self.index // 12
        self.image = self.frames[self.cur_frame]
        if self.index < 24:
            self.index += 1
        else:
            self.index = 0
            if variable_speed:
                self.speed_y = random.randint(-3, 3)  # Для повышения сложности перемннныя скорость
