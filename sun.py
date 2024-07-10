import pygame


class Sun(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, sun_sprites, all_sprites):
        super().__init__(sun_sprites, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load('data/bonus/sun.png'), (50, 50)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -150:
            self.kill()
