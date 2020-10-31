import random
import os
import pygame as pg
from libs import Board, MyRect, Display

class SodokuBoard(Board):
        def draw(self):
                self.draw_plain_init()
                ### draw additional sodoku numbers:
                for x in range(self.w):
                        for y in range(self.h):
                                n = grid[y][x]
                                text = str(n) if n != 0 else ""
                                rect = self.array[x+y*self.w].rect
                                pos_x,pos_y = rect.left, rect.top
                                display_ob.display_text(x=pos_x+rect.width//2,y=pos_y+rect.height//2,
                                                        text=text,centeredX=True,centeredY=True,
                                                        colour=WHITE,bg=BLACK,font=num_font)

grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        ]

def assign_num(*args, **kwargs):
    # current_rect = kwargs['currentRect']
    x,y = kwargs['pos_x'], kwargs['pos_y']
    num = grid[y][x]
    # get the number input from user, to change......
    while True:
        try:
            num = int(input("enter num: ")[0])
        except ValueError:
            continue
        break

    ## change the value in that position accordingly:
    if num != grid[y][x]:
        grid[y][x] = num


def display_grid(grid):
        pass



### CONSTANTS
TITLE = "SODOKU"
GRID_W = len(grid[0])
GRID_H = len(grid)
CUBE_WIDTH = 75

### COLOURS:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 26, 0)
BRIGHT_RED = (170,1,20)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
BEIGE = (250, 175, 0)
AQUA = (128, 206, 207)
DARK_GREY = (64, 64, 64)
YELLOW = (255, 204, 0)
PURPLE = (148,0,211)
ORANGE = (255,106,2)
INDIGO = (75,0,130)
VIOLET = (238,130,238)
PINK = (231,84,128)
BROWN = (102,51,0)
CYAN = 0,173,238
SHAPE_COLOUR = ORANGE
CLICK_BUTTON_COLOUR = PINK
SIDE_SHAPE_COLOUR = ORANGE

### Set up pygame:

pg.mixer.pre_init()
pg.init()
pg.font.init()
scr = pg.display.set_mode((GRID_W*CUBE_WIDTH, GRID_H*CUBE_WIDTH))
pg.display.set_caption(TITLE)
scr.fill(BLACK)
pg.display.flip()

### Set up the board:

PuzzleRec = MyRect(func=None, colour=BLUE, line_colour=WHITE)
PlayingRec = MyRect(func=[assign_num], colour=BLACK, line_colour=WHITE)

sodoku_board = SodokuBoard(scr, x=0, y=0, rect=PlayingRec, width=GRID_W, height=GRID_H,
                     cube_width= CUBE_WIDTH, cube_height=CUBE_WIDTH, border=False)

## set rec for the puzzle RECT, so that they are different:
# for y in range(GRID_H):
#         for x in range(GRID_W):
#                 if grid[y][x] != 0:
#                         print(f"x = {x}; y = {y}")
#                         sodoku_board.assign_rect_to_array(sodoku_board.array,x,y,PuzzleRec)


### SET UP BEFORE GAME-LOOP:
display_ob = Display(scr)
num_font = pg.font.SysFont("andalemono", 30)
running = True
while running:
        ######## set-up timing:

        ######## get user-input:
        events = pg.event.get()
        for e in events:
                if e.type == pg.QUIT:
                        running = False
                if e.type == pg.MOUSEBUTTONDOWN:
                        sodoku_board.click(e.pos)

        ####### update game states:

        ####### draw & render:
        sodoku_board.draw()

        pg.display.flip()



