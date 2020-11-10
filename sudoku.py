import copy
import random

def generate_empty_grid(width, height):
    g = []
    for y in range(height):
        g.append([])
        for x in range(width):
            g[y].append(0)
    return g

def isPossbile(grid, n, x, y):
    # check horozontally aka. x:
    for i in range(0, 9):
        if n == grid[y][i]:
            if i != x:
                return False
    # check vertically:
    for i in range(0, 9):
        if n == grid[i][x]:
            if i != y:
                return False
    # check the square:
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if n == grid[y0 + i][x0 + j]:
                if not (((y0 + i) == y) and ((x0 + j) == x)):
                    return False
    return True



class Solver:
    def __init__(self, grid):
        self.set_grid(grid)

    def set_grid(self,grid):
        self.grid = copy.deepcopy(grid)

    @classmethod
    def solve(self, grid):
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1,10):
                        if isPossbile(grid, n,x,y):
                            grid[y][x] = n
                            yield from self.solve(grid)
                            grid[y][x] = 0
                    return
        yield grid

    @classmethod
    def check_unique(self, board):
        ### check if grid has one unique solution
        grid = copy.deepcopy(board)
        rs = self.solve(grid)
        times = 0
        for _ in range(2):
            if times > 1:
                return False
            try:
                next(rs)
                times += 1
            except StopIteration:
                if times == 1:
                    return True

        return False

    @classmethod
    def print(self, grid):
        for line in grid:
            for num in line:
                if num == 0:
                    print(".", end="  ")
                else:
                    print(num, end="  ")
            print()

    @classmethod
    def generate_filled_board(cls):
        def fill_random(grid):
            ### fill a full square
            for x in range(3):
                for y in range(3):
                    while True:
                        ran_num = random.randint(1, 9)
                        if isPossbile(grid=grid,x=x,y=y,n=ran_num):
                            grid[y][x] = ran_num
                            break

        grid = generate_empty_grid(9,9)
        fill_random(grid)
        # cls.print(grid)
        results = cls.solve(grid)
        return next(results)

    @classmethod
    def find_opposite_square(cls, x,y):
        x = x // 3
        y = y // 3
        opp_x0 = abs(x-2) * 3
        opp_y0 = abs(y-2) * 3

        return opp_x0, opp_y0

    @classmethod
    def generate_puzzle(self):
        board = Solver.generate_filled_board()
        times = 0
        ### remove a random num
        priv_x = None
        priv_y = None
        first = True
        while times < 51:
            if first:
                x = random.randint(0,8)
                y = random.randint(0,8)
            else:
                x0, y0 = Solver.find_opposite_square(priv_x, priv_y)
                x = x0 + random.randint(0,2)
                y = y0 + random.randint(0,2)
            spot = board[y][x]
            if spot != 0:
                board[y][x] = 0
                ### solve the new board and check for solutions
                if self.check_unique(board):
                    times += 1
                    if first:
                        priv_x = x
                        priv_y = y
                    first = not first
                else:
                    board[y][x] = spot
            else:
                continue

        return board





