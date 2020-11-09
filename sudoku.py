import copy

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
    def check_unique(self, grid):
        ### check if grid has one unique solution
        grid = copy.deepcopy(grid)
        rs = self.solve(grid)
        times = 0
        for _ in range(2):
            if times > 1:
                return False
            try:
                next(rs)
            except StopIteration:
                if times == 1:
                    return True
            times += 1

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
    def generate_random_puzzle(self):
        def fill_random(grid, n=30):
            ### n is the number of random numbers to be filled
            ### check validity as you fill
            pass
        grid = generate_empty_grid(9,9)
        fill_random(grid)
        if not self.check_unique(grid):
            grid = self.generate_random_puzzle()
        return grid



