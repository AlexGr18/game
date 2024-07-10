import pygame

size = width, height = 1200, 600


class Backgraund():
    def __init__(self, fon):
        self.image = pygame.transform.scale(pygame.image.load(fon).convert(), size)
        self.rect = self.image.get_rect()
        self.scroll = 0
        self.speed = 1
        self.x_left = 0
        self.x_right = self.rect.width

    def update(self):
        self.x_left -= self.speed
        self.x_right -= self.speed
        if self.x_left <= - self.rect.width:
            self.x_left = self.rect.width
        if self.x_right <= - self.rect.width:
            self.x_right = self.rect.width

    def render(self, screen):
        screen.blit(self.image, (self.x_left, 0))
        screen.blit(self.image, (self.x_right, 0))
