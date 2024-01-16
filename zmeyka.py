
import pygame,random
import time
from os import path
pygame.init()
width=500
height=500

mus_dir=path.join(path.dirname(__file__),'music')
am=pygame.mixer.Sound(path.join(mus_dir,"apple_bite.ogg"))
pygame.mixer.music.load(path.join(mus_dir,"1.mp3"))
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
black=(0,0,0)
screen=pygame.display.set_mode((width,height))
img_dir=path.join(path.dirname(__file__),'foto')
bg=pygame.image.load(path.join(img_dir,'udHGEF.jpg')).convert()
bg_react=bg.get_rect()
xcor=width/2
ycor=height/2
x=0
y=0
snake_speed=15
clock=pygame.time.Clock()

font_style = pygame.font.SysFont(None, 32)
scorefont=pygame.font.SysFont("comicsansms",25)
def score(score):
    value=scorefont.render("Ваш счёт:"+str(score),True,red)
    screen.blit(value,[0,0])
def message(msg, color):

    mes = font_style.render(msg, True, color)

    screen.blit(mes, [width/16, height/2])
def new_block (snake_body):

    for x in snake_body:
        pygame.draw.rect(screen,white, [x[0], x[1], 20, 20])

pygame.display.set_caption('змейка')
def k():
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

    food_img =[pygame.image.load(path.join(img_dir, 'еда.jpg')).convert()]
    food = pygame.transform.scale(random.choice(food_img),(20,20))
    food_react=food.get_rect(x=foodx,y=foody)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    end=False
    while run:

        while end == True:

            screen.fill(blue)

            message("Нажми 'C'-продолжить или 'Q'-выход", red)

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        run = False

                        end = False

                    if event.key == pygame.K_c:
                        k()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_LEFT:

                        x=-10
                        y=0

                elif event.key==pygame.K_RIGHT:


                        x=10
                        y=0


                elif event.key==pygame.K_UP:


                        x=0
                        y=-10


                elif event.key==pygame.K_DOWN:

                        x=0
                        y=10



        if xcor >= width or xcor < 0 or ycor >= height or ycor < 0:
            end= True
        xcor+=x
        ycor+=y

        screen.fill(blue)
        screen.blit(bg, bg_react)
        screen.blit(food,food_react)

        snake_head = []
        snake_head.append(xcor)
        snake_head.append(ycor)
        snake_body.append(snake_head)

        if len(snake_body) > length:
            del snake_body[0]

        new_block(snake_body)
        score(length-1)
        pygame.display.update()
        if xcor == foodx and ycor == foody:
            foodx = round(random.randrange(0, width - 30) / 10) * 10

            foody = round(random.randrange(0, height - 30) / 10) * 10

            food_img = [pygame.image.load(path.join(img_dir, 'еда.jpg')).convert()]

            food = pygame.transform.scale(random.choice(food_img), (20, 20))
            food_react = food.get_rect(x=foodx, y=foody)
            screen.blit(food, food_react)
            length += 1
            am.play()
        pygame.display.flip()
        clock.tick(snake_speed)
    message('Ты проиграл!', red)

    pygame.display.update()

    time.sleep(1)
    pygame.quit()
k()