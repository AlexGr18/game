import pygame
import music
from button import ImageButton
from plane import Plane
from backgraund import Backgraund, size
import map_game
import events
import sys
import information
from scores import Scorec

FPS = 60
rating = 0


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Аэроплан')
    icon = pygame.image.load('data/screen/icon.png')
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load('data/screen/screensaver.jpg').convert(), (800, 600))
    screen.blit(fon, (0, 0))
    # кнопка правила
    rules = ImageButton(100, 520, 300, 60, 'ПРАВИЛА ИГРЫ', 'data/button/button.png',
                        'data/button/button_rules_after.png', 'data/music/button.mp3')
    # кнопка запуска игры
    start = ImageButton(450, 520, 300, 60, 'НАЧАТЬ ИГРУ', 'data/button/button.png',
                        'data/button/button_start_after.png', 'data/music/button.mp3')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if rules.event_mous(event):
                return False
            if start.event_mous(event):
                return True
        rules.check_hover(pygame.mouse.get_pos())
        rules.draw(screen)
        start.check_hover(pygame.mouse.get_pos())
        start.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    terminate()


# изменить
def inform_screen(itog_game=False):
    print(rating)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Аэроплан')
    icon = pygame.image.load('data/screen/icon.png')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load('data/screen/complexio.jpg').convert(), size)
    screen.blit(fon, (0, 0))
    close = ImageButton(850, 520, 300, 60, 'ВЫХОД', 'data/button/button.png',
                        'data/button/button_start_after.png', 'data/music/button.mp3')
    rules = ImageButton(400, 340, 300, 60, "", 'data/button/button.png', None, 'data/music/button.mp3')

    if not itog_game:
        information.rules_game(screen)
    else:
        information.final_game(screen, rating)

    input_user = False

    name = ""
    font = pygame.font.Font(None, 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # код ввода текста
            if input_user and event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_user = False
                        name = ""
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 10:
                            name += event.unicode
            if rules.event_mous(event):
                input_user = True
                if len(name) > 0:
                    information.sql_rating_insert(name, rating)
            if close.event_mous(event):
                if not itog_game:
                    return
                else:
                    terminate()

        if itog_game:
            rules.check_hover(pygame.mouse.get_pos())
            rules.draw(screen)
            user_name = font.render(name, True, (128, 64, 48))
            screen.blit(user_name, (450, 360))
            last_name = font.render('Имя игрока', True, (128, 64, 48))
            screen.blit(last_name, (450, 300))
            help_1 = font.render("Чтобы ввести имя нажмите лвой кнопкой мыши на поле 'ИМЯ'", True, (128, 64, 48))
            screen.blit(help_1, (450, 420))
            help_2 = font.render("Чтобы сохранить нажмите повторно", True, (128, 64, 48))
            screen.blit(help_2, (450, 480))
        close.check_hover(pygame.mouse.get_pos())
        close.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    terminate()


def run_game():
    global rating
    # количество уровней
    level_count = 10

    # создание окна игры
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Аэроплан')
    icon = pygame.image.load('data/screen/icon.png')
    pygame.display.set_icon(icon)

    # генерация уровней
    game_levels = map_game.Level(level_count)
    # количество пойманных монет
    amount_bonuses = 0

    # основной цикл игры
    for level in range(level_count):
        if level % 2 == 0:
            musik_fon = 'data/music/track_2.mp3'
            pict_fon = 'data/screen/fon.jpg'
        else:
            musik_fon = 'data/music/track_1.mp3'
            pict_fon = 'data/screen/fon2.png'
        # время одного тура игры
        timer = 120
        # поле
        data_game = game_levels.data[level]
        # количество созданных птиц
        count_bird = game_levels.number_bird[level][0]
        # случайная скорость по y
        variable_speed = game_levels.number_bird[level][2]
        # скорость птицы по x, y
        speed = game_levels.number_bird[level][1]
        # количество облаков
        count_cloud = game_levels.number_cloud[level][0]
        # скорость капли
        sped_drop = game_levels.number_cloud[level][1]
        # количество созданных монет
        count_bonus = 5
        # попаданий птицы
        amount_bird = 1

        clock = pygame.time.Clock()

        # создание групп спрайтов
        all_sprites = pygame.sprite.Group()
        plane_group = pygame.sprite.Group()
        bird_sprites = pygame.sprite.Group()
        cloud_sprites = pygame.sprite.Group()
        drop_sprites = pygame.sprite.Group()
        repair_sprites = pygame.sprite.Group()
        sun_sprites = pygame.sprite.Group()
        bonus_sprites = pygame.sprite.Group()
        tiles_sprites = pygame.sprite.Group()

        # основные объекты игры
        backgraund = Backgraund(pict_fon)
        plane = Plane(plane_group, all_sprites)
        health = Scorec(screen)
        # создаю карту
        map_game.generate_level(data_game, tiles_sprites, all_sprites)

        # отрисовка счетчиков
        health.timer(timer)
        # фоновая музыка
        music.fon_music(musik_fon)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        events.pause(screen)
                if health.game == 2 and event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            if health.game == 1:
                backgraund.update()
                backgraund.render(screen)
                plane_group.draw(screen)
                tiles_sprites.draw(screen)
                all_sprites.draw(screen)
                plane.update()
                tiles_sprites.update(1)
                # статистика
                health.show_health(plane)
                health.draw_coin()
                health.draw_timer()
                health.finish(plane, timer)
                # создание монет
                events.group_bonus(bonus_sprites, tiles_sprites, all_sprites, count_bonus)
                # создание птиц
                events.group_bird(speed, variable_speed, bird_sprites, all_sprites, count_bird)
                # создание облаков
                events.group_rain(sped_drop, cloud_sprites, drop_sprites, tiles_sprites, all_sprites, count_cloud)
                # гибель самолета
                events.death(plane, tiles_sprites)
                # столкновение птицы и земли
                events.collision_objects(bird_sprites, tiles_sprites)
                # взаимодействие с каплями
                events.drop_plane(plane, drop_sprites, sun_sprites, tiles_sprites, all_sprites)
                # взаимодействие с птицами
                amount_bird = events.bird_plane(plane, amount_bird, bird_sprites, repair_sprites, all_sprites)
                # ремонт самолета после птиц
                plane.failure = events.recovery(plane, repair_sprites, plane.failure, 'data/music/repair.mp3')
                # ремонт самолета после дождя
                plane.gravity = events.recovery(plane, sun_sprites, plane.gravity, 'data/music/sun.mp3')
                # считаем пойманные монеты
                amount_bonuses += events.bonus_plane(plane, bonus_sprites)
                health.amount_coin = amount_bonuses

                timer = health.timer(timer)
            elif health.game == 2:
                pygame.mixer.music.stop()
                music.music_hit('data/music/level.mp3')
            else:
                pygame.mixer.music.stop()
                rating = amount_bonuses
                inform_screen(True)

            pygame.display.update()
            clock.tick(FPS)
    rating = amount_bonuses
    pygame.quit()


if __name__ == '__main__':
    while True:
        if start_screen():
            run_game()
            inform_screen(True)
            break
        else:
            inform_screen(False)
