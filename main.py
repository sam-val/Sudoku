import random
import os
import time
import copy
import pygame as pg
from libs import Board, MyRect, Display
from sudoku import Solver, isPossbile, generate_empty_grid
import requests

class SodokuBoard(Board):
        def draw(self):
            global display_grid
            self.draw_plain_init()
            ### draw additional sodoku numbers:
            for x in range(self.w):
                    for y in range(self.h):
                            n = display_grid[y][x]
                            text = str(n) if n != 0 else None
                            my_rect = self.array[x+y*self.w]
                            pos_x,pos_y = my_rect.rect.left, my_rect.rect.top
                            if text is not None:
                                display_ob.display_text(x=pos_x+my_rect.rect.width//2,y=pos_y+my_rect.rect.height//2,
                                                        text=text,centeredX=True,centeredY=True,
                                                        colour=WHITE,bg=None,font=num_font)

display_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                ]

def change_colour(*args, **kwargs):
    current_rect = kwargs['rect']
    current_rect.colour = activeColour if current_rect.active else inactiveColour
    if hasattr(current_rect, 'wrong'):
        if current_rect.wrong:
            current_rect.colour = BRIGHT_RED
        else:
            current_rect.colour = activeColour if current_rect.active else inactiveColour


def assign_num(rect):
    # other stuff
    x,y = rect.x, rect.y
    num = display_grid[y][x]
    # get the number input from user, to change......
    r = True
    while r:
        events = pg.event.get()
        for e in events:
            if e.type == pg.KEYDOWN:
                if rect.active:
                    if e.key in range(48,58):
                        num = e.key - 48
                        r = False
                        rect.active = False
                        break
    ## change the value in that position accordingly:
    if num != 0:
        if not isPossbile(display_grid,num, x,y):
            print("inccorect")
            rect.wrong = True
        else:
            rect.wrong = False
    else:
        rect.wrong = False

    display_grid[y][x] = num


    change_colour(rect=rect)



def solve_display():
    global temp_grid, grid_results, display_grid, original_grid
    if temp_grid != display_grid:
        print('running.........')
        original_grid = copy.deepcopy(display_grid)
        temp_grid = original_grid
        solver.set_grid(display_grid)
        grid_results = solver.solve(solver.grid)
        solve_display()
    else:
        if grid_results is None:
            print('nothing to do')
        else:
            try:
                print("try...")
                rs = next(grid_results)
                display_grid = copy.deepcopy(rs)
                temp_grid = copy.deepcopy(display_grid)
                # Solver.print(test)
                # original_grid = test
                print("YES! RESULT")
                print(display_grid)
            except StopIteration:
                print("no more results, back")
                display_grid = copy.deepcopy(original_grid)

def new_puzzle(*args, **kwargs):
    ### USING API CALL
    grid = generate_empty_grid(9, 9)
    params = {"size": 9, "level": 2}
    url = "http://www.cs.utep.edu/cheon/ws/sudoku/new"
    r = requests.get(url, params=params)
    data = r.json()
    for i in data['squares']:
        x, y, n = i['x'], i['y'], i['value']
        grid[y][x] = n
    global display_grid
    display_grid = grid


### CONSTANTS
TITLE = "SODOKU"
GRID_W = 9
GRID_H = 9
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
scr = pg.display.set_mode((GRID_W*CUBE_WIDTH, (GRID_H+1)*CUBE_WIDTH))
pg.display.set_caption(TITLE)
scr.fill(BLACK)
pg.display.flip()


###  Menu Buttons
### generate new puzzle button:
newPuzzleRect = MyRect(func=[new_puzzle], colour=WHITE)

newPuzzleButton = Board(scr, x=0,y=0, rect=newPuzzleRect, width=GRID_W, height=1,
                        cube_width=CUBE_WIDTH, cube_height=CUBE_WIDTH, border=False)

### Set up the board:
inactiveColour = BLACK
activeColour = ORANGE
# PuzzleRec = MyRect(func=None, colour=BLUE, line_colour=WHITE)
PlayingRec = MyRect(func=[change_colour], colour=inactiveColour, line_colour=WHITE)

sodoku_board = SodokuBoard(scr, x=0, y=newPuzzleButton.h*CUBE_WIDTH, rect=PlayingRec, width=GRID_W, height=GRID_H,
                           cube_width= CUBE_WIDTH, cube_height=CUBE_WIDTH, border=False)
### SET UP BEFORE GAME-LOOP:
display_ob = Display(scr)
solver = Solver(display_grid)
num_font = pg.font.SysFont("andalemono", 30)
running = True
active_rect = None
temp_grid = None
grid_results = None
original_grid = None
generate_locked = False
generate_time = 0
while running:
        ######## set-up timing:


        ####### update game states:

        if active_rect is not None:

            assign_num(active_rect)
            active_rect = None

        ######## get user-input:

        events = pg.event.get()
        for e in events:
                if e.type == pg.QUIT:
                    running = False
                if e.type == pg.MOUSEBUTTONDOWN:
                    if (e.button == 1): ## if it's left mouse click
                        active_rect = sodoku_board.click(e.pos)
                        newPuzzleButton.click(e.pos)
                    else:
                        solve_display()

        ####### draw & render:
        sodoku_board.draw()
        newPuzzleButton.draw_plain_init()
        text = "Generate New Puzzle"
        display_ob.display_text(x=(newPuzzleButton.w*CUBE_WIDTH)/2,y=(newPuzzleButton.h*CUBE_WIDTH)/2,
                                text=text,colour=BLACK,centeredY=True,centeredX=True, font=num_font)

        pg.display.flip()



