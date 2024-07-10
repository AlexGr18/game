from bird import Bird
from rain import Rain
from repair import Repair
from bonus import Bonus
from sun import Sun
import music
import random
import pygame
import backgraund as size

speed = 1


# появление монет на экране
def group_bonus(bonus_sprites, tiles_sprites, all_sprites, count):
    bonus_sprites.update()
    bonus_x = size.width
    while len(bonus_sprites) < count:
        bonus_x += 90
        bonus_y = random.randint(50, 400)
        Bonus(bonus_x, bonus_y, speed, bonus_sprites, all_sprites)
        collision_objects(bonus_sprites, tiles_sprites)


# появление птицы на экране
def group_bird(speed, variable_speed, bird_sprites, all_sprites, count):
    bird_sprites.update(variable_speed)
    if len(bird_sprites) < count:
        Bird(speed, bird_sprites, all_sprites)


# появление дождя на экране
def group_rain(sped_drop, cloud_sprites, drop_sprites, tiles_sprites, all_sprites, count):
    cloud_sprites.update(drop_sprites, tiles_sprites, all_sprites)
    cloud_x = 500
    cloud_y = 15
    speed_cloud = 1
    if len(cloud_sprites) == 0:
        while len(cloud_sprites) < count:
            Rain(speed_cloud, sped_drop, cloud_sprites, all_sprites).coord_cloud(drop_sprites, all_sprites, cloud_x,
                                                                                 cloud_y)
            cloud_x += 300
            cloud_y = (cloud_y + 150) % 200


# столкновение с птицей
def bird_plane(plane, count, bird_sprites, repair_sprites, all_sprites):
    repair_sprites.update()
    interaction = pygame.sprite.spritecollide(plane, bird_sprites, True)
    if interaction:
        plane.bird_interaction(count)
        music.music_hit('data/music/bird.mp3')
        count += 1
    if count > 4:
        if len(repair_sprites) < 1:
            Repair(random.randint(size.width, size.width + 600), random.randint(10, 100), speed, repair_sprites,
                   all_sprites)
    return count


# столкновение с каплей
def drop_plane(plane, drop_sprites, sun_sprites, tiles_sprites, all_sprites):
    sun_sprites.update()
    interaction = pygame.sprite.spritecollide(plane, drop_sprites, True)
    if interaction:
        gravity = plane.drop_interaction()
        music.music_hit('data/music/drop.mp3')
        if gravity > 2:
            while len(sun_sprites) < 1:
                Sun(random.randint(size.width, size.width + 600), random.randint(200, 400), speed, sun_sprites,
                    all_sprites)
                collision_objects(sun_sprites, tiles_sprites)


# взаимодействие самолета с бонусом востановления
def recovery(plane, sprites, damage, file_musiс):
    interaction = pygame.sprite.spritecollide(plane, sprites, True)
    if interaction:
        music.music_hit(file_musiс)
        return 0
    return damage


# взаимодействие с монетами
def bonus_plane(plane, bonus_sprites):
    interaction = pygame.sprite.spritecollide(plane, bonus_sprites, True)
    if interaction:
        music.music_hit('data/music/bonus.mp3')
        return 1
    return 0


# гибель самолета
def death(plane, tiles_sprites):
    interaction = pygame.sprite.spritecollide(plane, tiles_sprites, False)
    if interaction:
        music.music_hit('data/music/death.mp3')
        plane.healt -= 1
        plane.rect.y -= 50


# пауза в игре
def pause(screen):
    pause = True
    pygame.mixer.music.pause()
    while pause:
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False
                    pygame.mixer.music.unpause()
        pause_text = pygame.font.Font(None, 100).render(str("Пауза"), True, (209, 52, 52))
        screen.blit(pause_text, (500, 250))
        pygame.display.update()


# столкновение объектов
def collision_objects(one_sprites, two_sprites):
    pygame.sprite.groupcollide(one_sprites, two_sprites, True, False)
