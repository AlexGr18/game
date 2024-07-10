import pygame


class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/rain/drop_blue.png'), (10, 30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.initial_x = x
        self.initial_y = y

    def update(self, speed_drop, sped_cloud, one_sprites, two_sprites):
        self.rect.y += speed_drop
        self.rect.x -= sped_cloud
        object = pygame.sprite.groupcollide(one_sprites, two_sprites, False, False)
        for drop in object:
            drop.rect.y = self.initial_y


class Rain(pygame.sprite.Sprite):
    def __init__(self, speed, sped_drop, cloud_sprites, all_sprites):
        super().__init__(cloud_sprites, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load('data/rain/cloud_white.png'), (150, 75)).convert_alpha()
        self.speed = speed
        self.speed_drop = sped_drop
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.drop = []

    def update(self, drop_sprites, tiles_sprites, all_sprites):
        self.rect.x -= self.speed
        for i in range(len(self.drop)):
            self.drop[i].update(self.speed_drop, self.speed, drop_sprites, tiles_sprites)
        if self.rect.x < -150:
            self.kill()

    def coord_cloud(self, drop_sprites, all_sprites, cloud_x, cloud_y):
        self.rect.x = cloud_x + 50
        self.rect.y = cloud_y
        step_drop_x = self.rect.width // 3
        step_drop_y = 50
        for i_drop in range(3):
            temp_x = self.rect.x + i_drop * step_drop_x
            temp_y = self.rect.y + i_drop * step_drop_y
            drop = Drop(temp_x, temp_y)
            self.drop.append(drop)
            drop_sprites.add(drop)
            all_sprites.add(drop)
