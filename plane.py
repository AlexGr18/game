import pygame


class Plane(pygame.sprite.Sprite):
    def __init__(self, plane_group, all_sprites):
        super().__init__(plane_group, all_sprites)
        # повреждения
        self.gravity = 0
        self.failure = 0
        # анимация героя
        self.index = 0
        self.frames_ride = []
        self.frames_left = []
        self.cut_sheet(pygame.image.load('data/plane/plane_r.png').convert_alpha(), 4, 4, self.frames_ride)
        self.cut_sheet(pygame.image.load('data/plane/plane_l.png').convert_alpha(), 4, 4, self.frames_left)
        self.cur_frame = 0
        self.image = self.frames_ride[self.cur_frame]
        self.rect = self.image.get_rect(center=(100, 100))
        self.step = 5
        self.healt = 3

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
    def update(self, *all_sprites):
        # смена кадров
        self.cur_frame = self.index // 12
        self.image = self.frames_ride[self.cur_frame]
        self.rect = self.rect.move(0, self.gravity)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 10:
            self.image = self.frames_left[self.index // 12]
            self.rect.x -= self.step
        if keys[pygame.K_RIGHT] and self.rect.x < 1050:
            self.image = self.frames_ride[self.index // 12]
            self.rect.x += self.step
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.step
        if keys[pygame.K_DOWN] and self.rect.y < 520:
            self.rect.y += self.step
        if self.index < 24:
            self.index += 1
        else:
            self.index = 0

    def bird_interaction(self, count):
        self.failure = count * 10
        self.rect.y += self.failure

    def drop_interaction(self):
        self.gravity += 1
        return self.gravity
