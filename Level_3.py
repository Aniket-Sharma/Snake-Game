import pygame
import math
import time
import random

pygame.init()
infoObject = pygame.display.Info()
screen_width = math.floor(infoObject.current_w * 0.7)
screen_height = math.floor(infoObject.current_h * 0.6)
win = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.display.set_caption("Snake:Classic")

#basic colors
black = (0,0,255)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
bright_green = (0,128,0)
bright_red = (128,0,0)

#side size of the food element
side = 10
food_count = 0 

#define the food

def bonus_food():
    global c,d, bonus_timer, side
    (c,d) = (random.randint(3*side,screen_width-(3*side)), random.randint(3*side,screen_height-(3*side)))
    if (pygame.Surface.get_at(win, (c,d))) == (0,0,0,255):
        bonus_timer = 200 
        return
    else:
        bonus_food()
   
    
def food():
    global a,b, food_count, side 
    (a,b) = (random.randint(3*side,screen_width-(3*side)), random.randint(3*side,screen_height-(3*side)))
    if (pygame.Surface.get_at(win, (a,b))) == (0,0,0,255):
        food_count += 1
        if food_count >= 6 :
            food_count = 0 
            bonus_food()
        return 
    else:
        food()
        
#define button
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    win.blit(textSurf, textRect)

#define the pause function
def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False

def crashed():
    global score
    msg = 'GAME OVER    You Scored :' + str(score)
    pause = True
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        win.fill(white)
        
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = (((screen_width/2)), ((screen_height/3)) )
        win.blit(textSurf, textRect)
        
        button("Play_Again",250,250,200,100,green,bright_green,quitgame)
        button("Quit",450,250,200,100,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
    
    
def froze(acc):
    while True : 
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        k = pygame.key.get_pressed()
            
        if k[pygame.K_LEFT] and (acc == 'up' or acc == 'down'):
            acc = 'left'
            pointlist.append((x, y))
            break

        if (k[pygame.K_LEFT] and (acc == 'left')) or (k[pygame.K_RIGHT] and (acc == 'right')) or (k[pygame.K_UP] and (acc == 'up')) or (k[pygame.K_DOWN] and (acc == 'down')):
            break


        if k[pygame.K_RIGHT] and (acc == 'up' or acc == 'down'):
            acc = 'right'
            pointlist.append((x, y))
            break

        if k[pygame.K_UP] and (acc == 'right' or acc == 'left'):
            acc = 'up'
            pointlist.append((x, y))
            break

        if k[pygame.K_DOWN] and (acc == 'right' or acc == 'left'):
            acc = 'down'
            pointlist.append((x, y))
            break
            

def paused():
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        
        button("Continue",250,250,100,50,green,bright_green,unpause)
        button("Quit",450,250,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    
    global run, acc, x, y, a, b, step, snake_length, clock, pointlist, outer_points, side, delay, bonus_timer, score

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (acc == 'up' or acc == 'down'):
            acc = 'left'

        if keys[pygame.K_RIGHT] and (acc == 'up' or acc == 'down'):
            acc = 'right'

        if keys[pygame.K_UP] and (acc == 'right' or acc == 'left'):
            acc = 'up'

        if keys[pygame.K_DOWN] and (acc == 'right' or acc == 'left'):
            acc = 'down'
            
        if keys[pygame.K_ESCAPE] :
            pause = True
            paused()
                
        if keys[pygame.K_SPACE] :
            froze(acc)
                

        if acc == 'left':
            x -= step
        elif acc == 'up' :
            y -= step
        elif acc == 'down' :
            y += step
        else:
            x += step

        if x > screen_width - 1 :
            x = 1
            
        if x < 1 :
            x = screen_width - 1

        if y > screen_height - 1 :
            y = 1

        if y < 1 :
            y = screen_height - 1
        
        if (pygame.Surface.get_at(win, (x,y))) == (255,255,255,255) :
            score+=10
            snake_length += side
            food()
            
        elif (pygame.Surface.get_at(win, (x,y))) == (0,255,0,255) :
            score = score + bonus_timer
            bonus_timer = 0
            
        elif (pygame.Surface.get_at(win, (x,y))) == (255,0,0,255) :
            pygame.time.delay(2000)
            crashed()
                  
        pointlist.append((x,y))
                  
        win.fill((0, 0, 0))
        
        length = 0
        j = len(pointlist) - 1 

        while j>=0 and length <= snake_length:
            pygame.draw.rect(win, red, (pointlist[j][0], pointlist[j][1], side, side), 0)
            j = j - 1
            length += side 
        
        pygame.draw.rect(win, white, (a, b, side, side), 0)
        if bonus_timer > 0 :
            pygame.draw.rect(win, green, (c, d, side+2, side+2),  0)
            bonus_timer -= 1

        for i in range(len(outer_points)):
            pygame.draw.lines(win, red, False, outer_points[i], 10)

        msg = 'Score : ' + str(score)
        smallText = pygame.font.Font("freesansbold.ttf",10)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((screen_width-30), (10) )
        win.blit(textSurf, textRect)
        pygame.display.update()

        pygame.time.delay(delay)

    return
        

if __name__=='__main__' :
     #initial postion
    bonus_timer = 0 
    x = 20
    y = int(screen_height/2)

    #one step
    step = side
    delay = 50
    
    #initial accelerating towards
    acc = 'right'

    #initial count
    snake_length = 100
    score = 0 

    run = True

    clock = pygame.time.Clock()

    #the outer layer
    outer_points = []
    outer_points.append([(0, screen_height/3), (0,0), (screen_width, 0), (screen_width, screen_height/3)])
    outer_points.append([(screen_width,screen_height - screen_height/3), (screen_width, screen_height), (0,screen_height),  (0, screen_height - screen_height/3)])
    outer_points.append([(screen_width/4, screen_height/3), (screen_width - screen_width/4, screen_height/3)])
    outer_points.append([(screen_width/4, screen_height - screen_height/3), (screen_width - screen_width/4, screen_height - screen_height/3)])

    # define the snake
    pointlist = [(x,y)]
    #for i in range(6):
        #pointlist.append((x+(i*step),y))
    food()
    game_loop()
    
    del(pointlist)
    pygame.quit()
