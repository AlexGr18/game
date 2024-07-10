import pygame


class Scorec():
    def __init__(self, screen):
        self.image_hp = pygame.transform.scale(pygame.image.load('data/statistics/heart.png').convert_alpha(), (30, 30))
        self.image_time = pygame.transform.scale(pygame.image.load('data/statistics/time.png').convert_alpha(),
                                                 (30, 30))
        self.image_coin = pygame.transform.scale(pygame.image.load('data/statistics/coin.png').convert_alpha(),
                                                 (30, 30))
        self.screen = screen
        self.amount_coin = 0
        self.time = '0:00'
        self.game = 1
        self.index = 0

    def show_health(self, plane):
        x = 10
        for hp in range(plane.healt):
            self.screen.blit(self.image_hp, (x, 10))
            x += 30

    def draw_coin(self):
        print_coin = pygame.font.Font(None, 35).render(str(self.amount_coin), True, (209, 52, 52))
        self.screen.blit(self.image_coin, (200, 10))
        self.screen.blit(print_coin, (235, 16))

    def draw_timer(self):
        print_coin = pygame.font.Font(None, 35).render(str(self.time), True, (209, 52, 52))
        self.screen.blit(self.image_time, (110, 10))
        self.screen.blit(print_coin, (145, 16))

    def finish(self, plane, time):
        if plane.healt < 1:
            game_over = pygame.font.Font(None, 100).render(str("Вы проиграли"), True, (0, 0, 0))
            self.screen.blit(game_over, (350, 250))
            self.game = 0
        if time == 0:
            game_finish = pygame.font.Font(None, 80).render(str("Поздравляем вы добрались до финиша!"), True,
                                                            (209, 52, 52))
            self.screen.blit(game_finish, (20, 150))
            game_finish = pygame.font.Font(None, 50).render(str("Для продолжения игры нажми кнопку мыши"), True,
                                                            (209, 52, 52))
            self.screen.blit(game_finish, (200, 350))
            self.game = 2

    def timer(self, time):
        if self.index < 60:
            self.index += 1
        else:
            self.index = 0
            if time > 0:
                time -= 1
        if time % 60 < 10:
            sec = '0' + str(time % 60)
        else:
            sec = str(time % 60)
        self.time = str(time // 60) + ':' + sec
        return time
