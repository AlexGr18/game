import pygame


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, bonus_sprites, all_sprites):
        super().__init__(bonus_sprites, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load('data/bonus/bonus.png'), (30, 30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -50:
            self.kill()
