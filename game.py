import pygame
import random
import time
from os import path
import os
import sys
import sqlite3
from datetime import datetime

pygame.init()
width = 600
height = 500
list_apple = ["lk.jpg", "tt.jpg", "еда.jpg"]  # файлы с едой
mus_dir = path.join(path.dirname(__file__), 'music')
am = pygame.mixer.Sound(path.join(mus_dir, "apple_bite.ogg"))  # файл со звуком поедания яблока
pygame.mixer.music.load(path.join(mus_dir, "1.mp3"))
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
screen = pygame.display.set_mode((width, height))
img_dir = path.join(path.dirname(__file__), 'foto')
bg = pygame.image.load(path.join(img_dir, 'udHGEF.jpg')).convert()
bg_react = bg.get_rect()
xcor = width / 2
ycor = height / 2
x = 0
y = 0
snake_speed = 15
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 32)
scorefont = pygame.font.SysFont("comicsansms", 25)


def score(scor, name):  # функция подсчета и вывода очков во время игрового процесса
    name = scorefont.render("Ваше имя: " + name, True, red)
    value = scorefont.render("Ваш счёт: " + str(scor), True, red)
    screen.blit(value, [0, 0])
    screen.blit(name, [0, 22])


def message(msg, color):
    mes = font_style.render(msg, True, color)

    screen.blit(mes, [width / 16, height / 2])


def messag(msg, color):
    mes = font_style.render(msg, True, color)

    screen.blit(mes, [width / 2.6, height / 2])


def new_block(snake_body):  # увеличение змейки

    for i in snake_body:
        pygame.draw.rect(screen, red, [i[0], i[1], 20, 20])


pygame.display.set_caption('змейка')


def load_image(name):  # обработка изображений
    fullname = os.path.join('foto', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def game(name):  # основаная функция игры с обработкой игровых процессов
    global list_apple
    snake_speeds = 15
    xx = 0
    yy = 0
    xcords = width / 2
    ycords = height / 2
    snake_body = []
    length = 1
    run = True
    foodx = round(random.randrange(0, width - 30) / 10) * 10
    foody = round(random.randrange(0, height - 30) / 10) * 10
    food_img = [pygame.image.load(path.join(img_dir, list_apple[random.randint(0, 2)])).convert_alpha()]
    food = pygame.transform.scale(random.choice(food_img), (20, 20))
    food_react = food.get_rect(x=foodx, y=foody)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    end = False
    connection = sqlite3.connect('records.sqlite')
    cursor = connection.cursor()
    while run:

        while end:  # обработка завершения игры

            screen.fill(blue)

            message("'C'-продолжить,'Q'-выход,'R' - таблица рекордов", red)

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        sub = datetime.now()
                        game_date = sub.strftime("%H:%M:%S %D")
                        cursor.execute('''INSERT INTO Records (name, score, date) VALUES (?, ?, ?)''',
                                       (name, length - 1, game_date))
                        connection.commit()
                        connection.close()
                        run = False
                        end = False

                    if event.key == pygame.K_c:
                        game(name)

                    if event.key == pygame.K_r:
                        sub = datetime.now()
                        game_date = sub.strftime("%H:%M:%S %D")
                        cursor.execute('''INSERT INTO Records (name, score, date) VALUES (?, ?, ?)''',
                                       (name, length - 1, game_date))
                        connection.commit()
                        connection.close()
                        record_table(name, length - 1, game_date)

        for event in pygame.event.get():  # обработка клавиш для управления змейкой
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xx = -10
                    yy = 0
                elif event.key == pygame.K_RIGHT:
                    xx = 10
                    yy = 0
                elif event.key == pygame.K_UP:
                    xx = 0
                    yy = -10
                elif event.key == pygame.K_DOWN:
                    xx = 0
                    yy = 10
        if xcords > 600 or xcords < 0 or ycords >= 500 or ycords < 0:  # обработка координат змейки, отслеживание границ
            end = True
        xcords += xx
        ycords += yy

        screen.fill(blue)
        screen.blit(bg, bg_react)
        screen.blit(food, food_react)
        snake_head = [xcords, ycords]
        snake_body.append(snake_head)

        if len(snake_body) > length:
            del snake_body[0]

        new_block(snake_body)
        score(length - 1, name)
        pygame.display.update()
        if xcords == foodx and ycords == foody or xcords == foodx + 10 and ycords == foody + 10 or \
                xcords == foodx - 10 and ycords == foody + 10 or xcords == foodx - 10 and ycords == foody - 10 \
                or xcords == foodx + 10 and ycords == foody - 10:  # обработка поедания еды змейкой
            foodx = round(random.randrange(0, width - 30) / 10) * 10
            foody = round(random.randrange(0, height - 30) / 10) * 10
            food_img = [pygame.image.load(path.join(img_dir, list_apple[random.randint(0, 2)])).convert_alpha()]
            food = pygame.transform.scale(random.choice(food_img), (20, 20))
            food_react = food.get_rect(x=foodx, y=foody)
            screen.blit(food, food_react)
            length += 1
            am.play()
        pygame.display.flip()
        clock.tick(snake_speeds)
    messag('Ты проиграл!', red)
    pygame.display.update()
    time.sleep(1)
    pygame.quit()


def start_screen():  # начальный экран с вводом никнейма
    pygame.init()
    clocks = pygame.time.Clock()
    screens = pygame.display.set_mode([600, 500])
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(200, 200, 140, 32)
    color = pygame.Color('black')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    return user_text
                else:
                    user_text += event.unicode
        screens.fill((255, 255, 255))
        pygame.draw.rect(screens, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screens.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clocks.tick(60)


def record_table(name, scores, date):  # вывод таблицы с результатами
    pygame.init()
    scree = pygame.display.set_mode([600, 500])
    base_font = pygame.font.Font(None, 32)
    connection = sqlite3.connect('records.sqlite')
    cursor = connection.cursor()
    table = cursor.execute('''SELECT * FROM Records WHERE score - ? > 0 or ? - score > 0''',
                           (scores, scores)).fetchall()
    current_user = (name, scores, date)
    table.append(current_user)
    table = sorted(table, key=lambda l: l[1], reverse=True)
    table = [i for i in enumerate(table, 1)]
    print(table)
    for i in table:
        if i[1] == current_user:
            current_user = i
            break
    input_rect = pygame.Rect(200, 200, 140, 32)
    index = table.index(current_user)
    to_render = table[index - 3:index + 4]
    print(to_render)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        text_surface = base_font.render('', True, (0, 0, 0))
        scree.fill((255, 255, 255))
        c = 0
        for i in to_render:
            st = f'{i[0]}) {i[1][0]} {i[1][1]} {i[1][2]}'
            text_surface = base_font.render(st, True, (0, 0, 0))
            scree.blit(text_surface, (0, c * 25))
            c += 1
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
