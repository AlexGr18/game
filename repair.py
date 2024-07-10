import pygame


class Repair(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, repair_sprites, all_sprites):
        super().__init__(repair_sprites, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load('data/bonus/repair.png'), (30, 30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -150:
            self.kill()
