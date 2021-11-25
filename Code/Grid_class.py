import numpy as np

class Grid:

    def __init__(self, grid):
        self.grid = grid
        self.grid_size = len(grid)
        self.A = self.generate_A()# ??

    def render(self):
        print(self.grid)

    def change_single(self, pos, value):
        self.grid[pos[1], pos[0]] = value

    def simulate_click(self, grid, pos):
        x = pos[1]
        y = pos[0]
        grid_size = len(grid)

        if x < grid_size and y < grid_size:
            grid[x][y] = not grid[x][y]
            grid[(x + 1) % grid_size][y] = not grid[(x + 1) % grid_size][y]
            grid[(x - 1) % grid_size][y] = not grid[(x - 1) % grid_size][y]
            grid[x][(y + 1) % grid_size] = not grid[x][(y + 1) % grid_size]
            grid[x][(y - 1) % grid_size] = not grid[x][(y - 1) % grid_size]

        return grid

    def generate_A(self):
        A = np.zeros([self.grid_size**2, self.grid_size**2], int)
        counter = 0
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                action = np.zeros([self.grid_size, self.grid_size], int)
                A[counter, :] = self.simulate_click(action, [x, y]).flatten()
                counter += 1
        return A

    def get_full_solution(self):
        A = self.generate_A() # ??
        #print(A)
        b = self.grid.flatten()
        n = len(A)
        sol = []
        # main loop
        for k in range(n):
            # partial pivoting
            if A[k,k] == 0:
                for i in range(k+1, n):
                    if A[i, k] == 1:
                        for j in range(k, n):
                            A[k, j], A[i, j] = A[i, j],  A[k, j]
                        b[k], b[i] = b[i], b[k]
                        break
            # elimination
            for i in range(n):
                if i == k or A[i, k] == 0: continue
                A[i, k:n] = (A[i, k:n] + A[k, k:n])%2
                b[i] = (b[i]+b[k]) % 2

        # check if solution exists
        for i in range(n):
            if A[i, i] == 0 and b[i] == 1:
                return "No solution for this Configuration"

        for i in range(n):
            if b[i] == 1:
                row_len = len(self.grid)
                sol.append([i%row_len, int(i/row_len)])

        return sol













