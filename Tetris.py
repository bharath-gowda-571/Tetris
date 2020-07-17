import pygame
import random

pygame.init()

# Images and Text objects
screen = pygame.display.set_mode((570, 620))
pygame.display.set_caption("Tetris")
icon=pygame.image.load("tetris.png")
pygame.display.set_icon(icon)

blue=pygame.image.load("blue.png")
orange =pygame.image.load("orange.png")
red=pygame.image.load("red.png")
green=pygame.image.load("green.png")
purple=pygame.image.load("purple.png")
yellow=pygame.image.load("yellow.png")
black=pygame.image.load("black.png")
ScoreFont=pygame.font.Font("font.ttf",80)
ScoreText=ScoreFont.render("SCORE",True,(255,255,255))
clock=pygame.time.Clock()

# global variables
lis=[[0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0]]

pics={"T":red,"rect":blue,"square":green,"Z":orange,"S":purple,"J":yellow,"L":black}

start_pos={"rect":[[[0,i],[0,i+1],[0,i+2],[0,i+3]]for i in range(8)],
            "square":[[[0,i],[0,i+1],[1,i],[1,i+1]] for i in range(10)],
            "T":[[[0,i],[0,i+1],[0,i+2],[1,i+1]] for i in range(9)],
            "Z":[[[0,i],[0,i+1],[1,i+1],[1,i+2]] for i in range(9)],
            "S":[[[0,i+1],[0,i+2],[1,i],[1,i+1]]for i in range(9)],
            "J":[[[0,i],[0,i+1],[0,i+2],[1,i+2]]for i in range(9)],
            "L":[[[0,i],[0,i+1],[0,i+2],[1,i]]for i in range(9)]
           }

keys=list(start_pos.keys())
current_shape=random.choice(keys)
next_shape=random.choice(keys)
current_pos=random.choice(start_pos[current_shape])
allX, allY = zip(*current_pos)
occupied=[]
def draw():
    screen.fill((110, 122, 113))
    pygame.draw.rect(screen, (0, 0, 0), [350, 5, 500, 610], 0)
    pygame.draw.rect(screen, (255, 255, 255), [0, 0, 570, 620], 10)
    pygame.draw.line(screen, (255, 255, 255), (350, 0), (350, 620), 11)
    screen.blit(ScoreText, (390, 40))

def show():
    for i in range(20):
        for j in range(11):
            if lis[i][j]!=0:
                screen.blit(pics[lis[i][j]],(10+j*30,10+i*30))

def map_pos():
    for i in current_pos:
        lis[i[0]][i[1]]=current_shape

def move_down(x):
    for i in current_pos:
        lis[i[0]][i[1]] = 0
    current_pos[0][0]+=1
    current_pos[1][0]+=1
    current_pos[2][0]+=1
    current_pos[3][0]+=1
    map_pos()

def move_right(y):
    global current_pos
    if max(y)+1>14:
        for i in current_pos:
            lis[i[0]][i[1]] = 0
        current_pos[0][1] += 1
        current_pos[1][1] += 1
        current_pos[2][1] += 1
        current_pos[3][1] += 1
        map_pos()

def move_left(y):
    global current_pos
    if min(y)-1>=0:
        for i in current_pos:
            lis[i[0]][i[1]] = 0
        current_pos[0][1] -= 1
        current_pos[1][1] -= 1
        current_pos[2][1] -= 1
        current_pos[3][1] -= 1
    map_pos()

def check_bottom(x):
    global occupied
    if max(x) > 18:
        occupied+=current_pos
        return True
    else:
        for i in current_pos:
            if [i[0]+1,i[1]] in occupied:
                occupied+=current_pos
                return True
    return False

def move():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right(allY)
            if event.key == pygame.K_LEFT:
                move_left(allY)
            if event.key == pygame.K_DOWN:
                pass
    return True

def main():
    running=True
    global next_shape,current_shape,current_pos,allX,allY
    while running:
        print(lis)
        draw()
        show()
        move_down(allX)
        allX, allY = zip(*current_pos)
        if check_bottom(allX):
            current_shape=next_shape
            next_shape=random.choice(keys)
            current_pos=random.choice(start_pos[current_shape])
        running=move()
        pygame.display.update()
        # pygame.time.delay(500)
        clock.tick(3)
    pygame.display.quit()

if __name__ == "__main__":
    main()
