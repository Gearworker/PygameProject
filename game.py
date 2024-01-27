import pygame
import random
import time
from os import path
import os
import sys
import sqlite3
from datetime import datetime

pygame.init()
width=600
height=500
list_apple = ["lk.jpg", "tt.jpg", "еда.jpg"]
mus_dir=path.join(path.dirname(__file__), 'music')
am=pygame.mixer.Sound(path.join(mus_dir, "apple_bite.ogg"))
pygame.mixer.music.load(path.join(mus_dir, "1.mp3"))
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
black=(0,0,0)
screen=pygame.display.set_mode((width, height))
img_dir=path.join(path.dirname(__file__), 'foto')
bg=pygame.image.load(path.join(img_dir, 'udHGEF.jpg')).convert()
bg_react=bg.get_rect()
xcor=width/2
ycor=height/2
x=0
y=0
snake_speed=15
clock=pygame.time.Clock()

font_style = pygame.font.SysFont(None, 32)
scorefont=pygame.font.SysFont("comicsansms", 25)
def score(score, name):
    name = scorefont.render("Ваше имя: " + name, True, red)
    value=scorefont.render("Ваш счёт: "+str(score),True,red)
    screen.blit(value, [0, 0])
    screen.blit(name, [0, 22])
def message(msg, color):

    mes = font_style.render(msg, True, color)

    screen.blit(mes, [width/16, height/2])

def messag(msg, color):

    mes = font_style.render(msg, True, color)

    screen.blit(mes, [width/2.6, height/2])
def new_block (snake_body):

    for x in snake_body:
        pygame.draw.rect(screen, red, [x[0], x[1], 20, 20])

pygame.display.set_caption('змейка')

def load_image(name, colorkey=None):
    fullname = os.path.join('foto', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def game(name):
    global list_apple
    snake_speed = 15
    x = 0
    y = 0
    xcor = width / 2
    ycor = height / 2
    snake_body = []
    length = 1
    run = True
    foodx = round(random.randrange(0, width - 30) / 10) * 10
    foody = round(random.randrange(0, height - 30) / 10) * 10
    food_img =[pygame.image.load(path.join(img_dir, list_apple[random.randint(0, 2)])).convert_alpha()]
    # food_img = load_image(list_apple[random.randint(0, 2)])
    food = pygame.transform.scale(random.choice(food_img),(20,20))
    food_react = food.get_rect(x=foodx, y=foody)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    end = False
    connection = sqlite3.connect('records.sqlite')
    cursor = connection.cursor()
    while run:

        while end == True:

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                        x = -10
                        y = 0

                elif event.key == pygame.K_RIGHT:
                        x = 10
                        y = 0


                elif event.key==pygame.K_UP:
                        x = 0
                        y = -10


                elif event.key==pygame.K_DOWN:
                        x = 0
                        y = 10



        if xcor > 600 or xcor < 0 or ycor >= 500 or ycor < 0:
            end = True
        xcor+=x
        ycor+=y

        screen.fill(blue)
        screen.blit(bg, bg_react)
        screen.blit(food, food_react)
        snake_head = []
        snake_head.append(xcor)
        snake_head.append(ycor)
        snake_body.append(snake_head)

        if len(snake_body) > length:
            del snake_body[0]

        new_block(snake_body)
        score(length-1, name)
        pygame.display.update()
        if xcor == foodx and ycor == foody or xcor == foodx + 10 and ycor == foody + 10 or xcor == foodx - 10 and ycor == foody + 10 or xcor == foodx - 10 and ycor == foody - 10 \
                or xcor == foodx + 10 and ycor == foody - 10:
            foodx = round(random.randrange(0, width - 30) / 10) * 10

            foody = round(random.randrange(0, height - 30) / 10) * 10

            food_img = [pygame.image.load(path.join(img_dir, list_apple[random.randint(0, 2)])).convert_alpha()]

            food = pygame.transform.scale(random.choice(food_img), (20, 20))
            food_react = food.get_rect(x=foodx, y=foody)
            screen.blit(food, food_react)
            length += 1
            am.play()
        pygame.display.flip()
        clock.tick(snake_speed)
    messag('Ты проиграл!', red)

    pygame.display.update()

    time.sleep(1)
    pygame.quit()


def start_screen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([600, 500])
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
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)


def record_table(name, scores, date):
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
