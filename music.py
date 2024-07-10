import pygame


def fon_music(route):
    pygame.mixer.music.load(route)
    pygame.mixer.music.play(-1)


def music_hit(route):
    sound = pygame.mixer.Sound(route)
    sound.play()
