import pygame
import random
import os
import schedule
import shelve
import math
from copy import deepcopy
import time

pygame.init()

# Images and Text objects
icon=pygame.image.load(os.path.join("resources","icons","tetris_32x32.png"))
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((620, 620))
pygame.display.set_caption("Tetris")
# print(os.getcwd())
background=pygame.image.load(os.path.join("resources","background.jpg"))
red=pygame.image.load(os.path.join("resources","color_squares","red.png"))
green=pygame.image.load(os.path.join("resources","color_squares","green.png"))
blue=pygame.image.load(os.path.join("resources","color_squares","blue.png"))
orange=pygame.image.load(os.path.join("resources","color_squares","orange.png"))
purple=pygame.image.load(os.path.join("resources","color_squares","purple.png"))
yellow=pygame.image.load(os.path.join("resources","color_squares","yellow.png"))
pink=pygame.image.load(os.path.join("resources","color_squares","pink.png"))
transparent=pygame.image.load(os.path.join("resources","semi_transparent.png"))


upcoming_shapes={
                    "T":pygame.image.load(os.path.join("resources","shapes","T.png")),  
                    "rect":pygame.image.load(os.path.join("resources","shapes","rect.png")),
                    "square":pygame.image.load(os.path.join("resources","shapes","square.png")),
                    "L":pygame.image.load(os.path.join("resources","shapes","L.png")),
                    "J":pygame.image.load(os.path.join("resources","shapes","J.png")),
                    "S":pygame.image.load(os.path.join("resources","shapes","S.png")),
                    "Z":pygame.image.load(os.path.join("resources","shapes","Z.png"))
}

score=0
level=1
game_saved=False
paused=False
# Board is 14 x 20 so indexes are 13 x 19

Pause_and_GameOverFont=pygame.font.Font(os.path.join("resources","fonts","karma future.ttf"),120)
NextFont=pygame.font.Font(os.path.join("resources","fonts","karma future.ttf"),50)
ScoresAndLevelsFont=pygame.font.Font(os.path.join("resources","fonts","karma suture.ttf"),30)
HighScoreFont=pygame.font.Font(os.path.join("resources","fonts","karma future.ttf"),28)

NextLabel=NextFont.render("NEXT",1,(255,255,255))
ScoreLabel=NextFont.render("SCORE",1,(255,255,255))
HighScoreLabel=HighScoreFont.render("HIGH SCORE",1,(255,255,255))
LevelLabel=NextFont.render("LEVEL",1,(255,255,255))

GameOverText=Pause_and_GameOverFont.render("GAME OVER",1,(0,0,0))
PauseText=Pause_and_GameOverFont.render("PAUSED",1,(0,0,0))
LevelUpText=Pause_and_GameOverFont.render("LEVEL UP",1,(0,0,0))

controls_font=pygame.font.Font(os.path.join("resources","fonts","karma suture.ttf"),20)
# controls_font=

move_text=controls_font.render("Arrow Keys - Move and Rotate the Shape",1,(0,0,0))
# rotate_text=ScoresAndLevelsFont.render("Rotate the Shape.",1,(0,0,0))
pause_text=controls_font.render("Esc - Pause/Resume the Game",1,(0,0,0))
restart_text=controls_font.render("R - Restart the Game",1,(0,0,0))
fall_text=controls_font.render("Space - Drop the Shape Immediately",1,(0,0,0))

lis=[   [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]


pics={"T":red,"rect":blue,"square":green,"Z":orange,"S":purple,"J":yellow,"L":pink}
keys=['T', 'rect', 'square', 'Z', 'S', 'J', 'L']

occupied=[]
speeds={1:0.5,2:0.4,3:0.3,4:0.25,5:0.2,6:0.175,7:0.15,8:0.125,9:0.1}
temp_level=1
game_over=False
high_score=0
current_pos=[]
shapes=[]

def map_pos():
    global current_pos
    for i in current_pos:
        lis[i[0]][i[1]]=current_shape

def reset_board():
    global lis,occupied,shapes,keys
    lis=[   [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]

    occupied=[]
    shapes=[]+keys


def get_high_score():
    global high_score
    shelve_file=shelve.open(os.path.join("resources","my_data"))
    try:
        high_score=shelve_file["high score"]
    except KeyError:
        high_score=0
    shelve_file.close()

def start_pos(shape):
    if shape=="rect":
        return random.choice([([0,i],[0,i+1],[0,i+2],[0,i+3])for i in range(11)])
    if shape=="square":
        return random.choice([([0,i],[0,i+1],[1,i],[1,i+1]) for i in range(13)])
    if shape=="T":
        return random.choice([([1,i+1],[0,i+1],[0,i+2],[0,i]) for i in range(12)])
    if shape=="Z":
        return random.choice([([0,i],[0,i+1],[1,i+1],[1,i+2]) for i in range(12)])
    if shape=="S":
        return random.choice([([0,i+2],[0,i+1],[1,i+1],[1,i])for i in range(12)])
    if shape=="J":
        return random.choice([([1,i+2],[0,i+2],[0,i+1],[0,i])for i in range(12)])
    if shape=="L":
        return random.choice([([1,i],[0,i],[0,i+1],[0,i+2])for i in range(12)])

def save_high_score():
    global score,high_score 
    if score>high_score:
        shelve_file=shelve.open(os.path.join("resources","my_data"))
        shelve_file["high score"]=score
        shelve_file.close()   

def check_bottom(x):
    global occupied
    if max(x) >18:
        occupied+=current_pos
        return True
    else:
        for i in current_pos:
            if [i[0]+1,i[1]] in occupied:
                occupied+=list(current_pos)
                return True
    return False

def fall_down():
    global shapes,level
    temp_len=len(shapes)
    temp_level=level
    while len(shapes)==temp_len and not game_over and level==temp_level:
        move_down()

def rotate_rect(x,y):
        global current_pos,allX,allY
        temp_pos=[]
        if list(x).count(x[0])==len(list(x)):
            flag=False
            for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]+2,i[1][1]-2])
            for x in temp_pos:
                if x in occupied:
                    flag=True
            temp_x,temp_y=zip(*temp_pos)
            if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
                flag=True
            if not flag:
                for i in current_pos:
                    lis[i[0]][i[1]] = 0
                current_pos=deepcopy(temp_pos)
                map_pos()
                allX, allY = zip(*current_pos)

        else:
            flag=False
            for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]-2,i[1][1]+2])
            for x in temp_pos:
                if x in occupied:
                    flag=True
            temp_x,temp_y=zip(*temp_pos)
            if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
                flag=True
            if not flag:
                for i in current_pos:
                    lis[i[0]][i[1]] = 0
                current_pos=deepcopy(temp_pos)
                map_pos()
                allX, allY = zip(*current_pos)

def rotate_S(x,y):
    global current_pos,allX,allY
    temp_pos=[]
    if x[0]==x[1] and x[2]==x[3]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0],i[1][1]+2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    else:
        flag=False
        for i in enumerate(current_pos):
            if i[0]==1:
                temp_pos.append(i[1])
            elif i[0]==0:
                temp_pos.append([i[1][0]+1,i[1][1]+1])
            elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
            elif i[0]==3:
                    temp_pos.append([i[1][0],i[1][1]-2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

def rotate_Z(x,y):
    global current_pos,allX,allY
    temp_pos=[]
    if x[0]==x[1] and x[2]==x[3]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0],i[1][1]-2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    else:
        flag=False
        for i in enumerate(current_pos):
            if i[0]==1:
                temp_pos.append(i[1])
            elif i[0]==0:
                temp_pos.append([i[1][0]+1,i[1][1]-1])
            elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
            elif i[0]==3:
                    temp_pos.append([i[1][0],i[1][1]+2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

def rotate_J(x,y):
    global current_pos,allX,allY
    temp_pos=[]
    if x[1]==x[2]==x[3] and x[0]>x[1]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]-2,i[1][1]+2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)


    elif y[1]==y[2]==y[3] and y[1]>y[0]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]+2,i[1][1]+2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    elif x[1]==x[2]==x[3] and x[0]<x[1]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]+2,i[1][1]-2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    elif y[1]==y[2]==y[3] and y[1]<y[0]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]-2,i[1][1]-2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)
 
def rotate_L(x,y):
    global current_pos,allX,allY
    temp_pos=[]
    if x[1]==x[2]==x[3] and x[0]>x[1]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]+2,i[1][1]-2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)


    elif y[1]==y[2]==y[3] and y[1]>y[0]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]-2,i[1][1]-2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    elif x[1]==x[2]==x[3] and x[0]<x[1]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]-2,i[1][1]+2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    elif y[1]==y[2]==y[3] and y[1]<y[0]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]+2,i[1][1]+2])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)
 
def rotate_T(x,y):
    global current_pos,allX,allY
    temp_pos=[]
    if x[1]==x[2]==x[3] and x[0]>x[1]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)


    elif y[1]==y[2]==y[3] and y[1]>y[0]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    elif x[1]==x[2]==x[3] and x[0]<x[1]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]-1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

    elif y[1]==y[2]==y[3] and y[1]<y[0]:
        flag=False
        for i in enumerate(current_pos):
                if i[0]==1:
                    temp_pos.append(i[1])
                elif i[0]==0:
                    temp_pos.append([i[1][0]+1,i[1][1]-1])
                elif i[0]==2:
                    temp_pos.append([i[1][0]+1,i[1][1]+1])
                elif i[0]==3:
                    temp_pos.append([i[1][0]-1,i[1][1]-1])
        for x in temp_pos:
            if x in occupied:
                flag=True
        temp_x,temp_y=zip(*temp_pos)
        if min(temp_x)<0 or max(temp_x)>19 or min(temp_y)<0 or max(temp_y)>13:
            flag=True
        if not flag:
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos=deepcopy(temp_pos)
            map_pos()
            allX, allY = zip(*current_pos)

def draw():
    global game_over,paused,level
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for i in range(20):
        for j in range(14):
            if lis[i][j]!=0:
                screen.blit(pics[lis[i][j]],(10+j*30,10+i*30))
    screen.blit(NextLabel,(475,30))
    screen.blit(upcoming_shapes[next_shape],(455+(150-upcoming_shapes[next_shape].get_width())//2,115+(80-upcoming_shapes[next_shape].get_height())//2))
    screen.blit(ScoreLabel,(455,210))
    scoreText=ScoresAndLevelsFont.render(str(score),1,(0,0,0))
    screen.blit(scoreText,(455+(150-scoreText.get_width())//2,295+(50-scoreText.get_height())//2))
    screen.blit(HighScoreLabel,(455,360))
    # print()
    if high_score>=score:
        HighScoreText=ScoresAndLevelsFont.render(str(high_score),1,(0,0,0))
    else:
        HighScoreText=ScoresAndLevelsFont.render(str(score),1,(0,0,0))
    # print(HighScoreText.get_width())
    screen.blit(HighScoreText,(455+(150-HighScoreText.get_width())//2,405+(50-HighScoreText.get_height())//2))

    screen.blit(LevelLabel,(460,450))

    if not level:
        level=1
    LevelText=ScoresAndLevelsFont.render(str(level),1,(0,0,0))
    screen.blit(LevelText,(455+(150-LevelText.get_width())//2,535+(50-LevelText.get_height())//2))


    if game_over:
        screen.blit(transparent,(10,10))
        screen.blit(GameOverText,((620-GameOverText.get_width())//2,00))
    elif paused:
        screen.blit(transparent,(10,10))
        screen.blit(PauseText,((620-PauseText.get_width())//2,200))
    
    if game_over or paused:
        screen.blit(move_text,(30,450))
        screen.blit(pause_text,(30,480))
        screen.blit(restart_text,(30,510))
        screen.blit(fall_text,(30,540))
    pygame.display.update()

def move_right(y):
    global current_pos,allX,allY
    flag=True
    if max(y)+1<14:
        for i in current_pos:
            if [i[0],i[1]+1] in occupied:
                flag=False
        if flag:     
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos[0][1] += 1
            current_pos[1][1] += 1
            current_pos[2][1] += 1
            current_pos[3][1] += 1
            allX, allY = zip(*current_pos)
            map_pos()

def move_left(y):
    global current_pos,allX,allY
    flag=True
    if min(y)-1>=0:
        for i in current_pos:
            if [i[0],i[1]-1] in occupied:
                flag=False
        if flag:    
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos[0][1] -= 1
            current_pos[1][1] -= 1
            current_pos[2][1] -= 1
            current_pos[3][1] -= 1
            allX, allY = zip(*current_pos)
            map_pos()

def move_down():
    global lis,current_shape,current_pos,next_shape,allX,allY,game_over,shapes,speeds,keys,occupied,score,level,temp_level,game_saved
    if (not game_saved) and game_over:
        save_high_score()
        game_saved=True
    if not (game_over or paused):
        if check_bottom(allX):
            score+=20
            temp_lis_completed_rows=[]
            for x in enumerate(lis):
                if 0 not in x[1]:
                    score+=50
                    temp_lis_completed_rows.append(x[0])
                    temp_occupied=[]
                    for y in occupied:
                        if y[0]==x[0]:
                            continue
                        temp_occupied.append(y)
                    occupied=deepcopy(temp_occupied)
                    for y in range(len(occupied)):
                        if occupied[y][0]<x[0]:
                            occupied[y][0]+=1
            for z in temp_lis_completed_rows:
                del lis[z]
                lis=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]+lis

             # switching shapes happens after this 
            current_shape=next_shape
            if len(shapes)==0:
                shapes+=keys
            next_shape=shapes.pop(random.randint(0,len(shapes)-1))
            current_pos=start_pos(current_shape)
            # map_pos()
            allX, allY = zip(*current_pos)
            for i in current_pos:
                if [i[0]+1,i[1]] in occupied:
                    game_over=True
                    break
        level=math.ceil(score/2000)

        if not (game_over or paused) :
            for i in current_pos:
                lis[i[0]][i[1]] = 0
            current_pos[0][0]+=1
            current_pos[1][0]+=1
            current_pos[2][0]+=1
            current_pos[3][0]+=1
            map_pos()
            allX, allY = zip(*current_pos)

            if temp_level<level and level:
                screen.blit(transparent,(10,10))
                screen.blit(LevelUpText,(75,200))
                pygame.display.update()
                time.sleep(2)
                reset_board()
                current_shape=shapes.pop(random.randint(0,len(shapes)-1))
                next_shape=shapes.pop(random.randint(0,len(shapes)-1))
                current_pos=start_pos(current_shape)
                allX, allY = zip(*current_pos)
                schedule.clear("move_down")
                try:
                    schedule.every(speeds[level]).seconds.do(move_down).tag("move_down")
                except KeyError:
                    schedule.every(speeds[9]).seconds.do(move_down).tag("move_down")
                temp_level=level
        draw()

def main():
    global next_shape,current_shape,current_pos,allX,allY,shapes,high_score,paused,game_over,keys,score,temp_level
    # keys=['T', 'rect', 'square', 'Z', 'S', 'J', 'L']
    shapes=[]+keys
    current_shape=shapes.pop(random.randint(0,len(shapes)-1))
    next_shape=shapes.pop(random.randint(0,len(shapes)-1))
    current_pos=start_pos(current_shape)
    map_pos()
    allX, allY = zip(*current_pos)
    paused=False
    high_score=0
    game_saved=False
    schedule.every(speeds[1]).seconds.do(move_down).tag("move_down")
    get_high_score()
    running=True
    while running:
        schedule.run_pending()
        # draw()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT and not (game_over or paused):
                    move_right(allY)
                    draw()
                if event.key==pygame.K_LEFT and not (game_over or paused):
                    move_left(allY)
                    draw()
                if event.key==pygame.K_UP and not (game_over or paused):
                    if current_shape=="rect":
                        rotate_rect(allX,allY)
                    if current_shape=="S":
                        rotate_S(allX,allY)
                    if current_shape=="Z":
                        rotate_Z(allX,allY)
                    if current_shape=="J":
                        rotate_J(allX,allY)
                    if current_shape=="L":
                        rotate_L(allX,allY)
                    if current_shape=="T":
                        rotate_T(allX,allY)
                    draw()
                if event.key==pygame.K_DOWN and not (game_over or paused):
                    move_down()
                    # draw()
                if event.key==pygame.K_SPACE:
                    fall_down()
                if event.key==pygame.K_ESCAPE:
                    paused=not paused
                    draw()
                if event.key==pygame.K_r:
                    save_high_score()
                    reset_board()
                    current_shape=shapes.pop(random.randint(0,len(shapes)-1))
                    next_shape=shapes.pop(random.randint(0,len(shapes)-1))
                    current_pos=start_pos(current_shape)
                    allX, allY = zip(*current_pos)
                    game_over=False
                    paused=False
                    score=0
                    temp_level=1
                    schedule.clear("move_down")
                    schedule.every(speeds[1]).seconds.do(move_down).tag("move_down")
                    get_high_score()
    pygame.display.quit()

if __name__ == "__main__":
    main()
