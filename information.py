import sqlite3
import pygame


def sql_rating_insert(name, rating):
    db = sqlite3.connect('data/rating_game.db')
    sql = db.cursor()
    sqlite_insert_user = """INSERT INTO user (name, progress) VALUES (?, ?);"""
    sql.execute(sqlite_insert_user, (name, rating))
    db.commit()
    db.close()
    return 'Результат пользователя сохранен'


def sql_select_rating(rating):
    db = sqlite3.connect('data/rating_game.db')
    sql = db.cursor()
    sql.execute('SELECT * FROM user')
    user = sql.fetchall()
    user = sorted(user, key=lambda x: x[1], reverse=True)
    db.commit()
    place_game = len(user)
    for i in range(len(user)):
        if user[i][1] >= rating:
            place_game = i + 1
    return (user[:3], place_game)


def final_game(screen, rating):
    font = pygame.font.Font(None, 30)  # задали шрифт
    inform = sql_select_rating(rating)
    game_rating = font.render("Ваш рейтинг :", True, (128, 64, 48))
    screen.blit(game_rating, (400, 50))
    user_rating = font.render(str(inform[1]), True, (128, 64, 48))
    screen.blit(user_rating, (550, 50))
    user_rating = font.render("Лучшие игроки:", True, (128, 64, 48))
    screen.blit(user_rating, (400, 100))
    y = 150
    for picture_text in inform[0]:
        user = font.render(picture_text[0] + ' -- ' + str(picture_text[1]), True, (128, 64, 48))
        screen.blit(user, (450, y))
        y += 50


def rules_game(screen):
    font = pygame.font.Font(None, 30)  # задали шрифт
    rules_file = open('data/rules.txt', 'r', encoding='utf-8').readlines()
    text = []
    icon_text = []
    flag = False
    for str_n in rules_file:
        flag = False
        str_n = str_n.rstrip()
        if '#' in str_n:
            flag = True
            picture_str = str_n[str_n.find('#') + 1:]
            str_n = str_n[:str_n.find('#')]
            icon_text.append(
                pygame.transform.scale(pygame.image.load('data/bonus/' + picture_str + '.png').convert_alpha(),
                                       (50, 50)))
        text.append((font.render(str_n, True, (128, 64, 48)), flag))
    y = 50
    count = 0
    for picture_text in text:
        if picture_text[1]:
            screen.blit(picture_text[0], (400, y))
            x = 400 + picture_text[0].get_rect().width
            screen.blit(icon_text[count], (x + 20, y - 20))
            count += 1
        screen.blit(picture_text[0], (400, y))
        y += 50
