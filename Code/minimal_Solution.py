import numpy as np
import math

'''
Code that solves the "Turn all the lights off" Task.
Returns "Yes" or "No" depending on the configuration (solvable non-solvable)
supplied in the "Input.txt" 

To use:
>> is_solvable("Input.txt")

'''


def simulate_click(grid, pos):
    """
    Simulates the flipping of a switch at given position and grid

    Args:
        grid: 2D np.array that represents the grid
        pos: python list with x and y coordinate of the flipped switch

    Returns:
        2D np.array that represents the grid after the click at given position
    """
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


def generate_A(grid_size):
    """
    Generates the Action Matrix for a given Grid size

    Args:
        grid_size: int that represents the size of the grid

    Returns:
        2D np.array that represents the Action Matrix
        (Matrix of all possible actions for a Grid)
    """
    A = np.zeros([grid_size ** 2, grid_size ** 2], int)
    counter = 0
    for y in range(grid_size):
        for x in range(grid_size):
            action = np.zeros([grid_size, grid_size], int)
            A[counter, :] = simulate_click(action, [x, y]).flatten()
            counter += 1
    return A


def generate_grid_matrix(challenge_input_file):
    """
    Reads from file to create the desired grid

    Args:
        challenge_input_file: .txt file that specifies the start grid
    Returns:
        2D np.array that represents the Grid Matrix
    """
    file = open(challenge_input_file, "r")
    size = int(file.readline())
    matrix = np.zeros([size, size], int)
    file.readline()
    for line in file:
        pos = [int(x) for x in line.split()]
        matrix[pos[0]][pos[1]] = 1
    file.close()
    return matrix


def is_solvable(input_file):
    """
    Reads from file and decides whether given grid is solvable by allowed actions
    (by checking whether an Ax=b equation is solvable)

    Args:
        input_file: .txt file that specifies the start grid

    Returns:
        "Yes" or "No" depending on the configuration (solvable non-solvable)
        """
    b = generate_grid_matrix(input_file).flatten()
    A = generate_A(int(math.sqrt(len(b))))
    n = len(A)

    # main loop
    for k in range(n):
        # partial pivoting
        if A[k, k] == 0:
            #check if we have a one belowe the 0 at k,k
            for i in range(k + 1, n):
                if A[i, k] == 1:
                    #if we have a 1 switch the two rows
                    A[[k, i], :] = A[[i, k], :]
                    b[k], b[i] = b[i], b[k]
                    break

        # elimination
        for i in range(n):
            if i == k or A[i, k] == 0: continue
            # if we have a 1 at n,k add row k to n, ow we have a 0 at n,k
            A[i, k:n] = (A[i, k:n] + A[k, k:n]) % 2
            b[i] = (b[i] + b[k]) % 2

    # check if solution exists
    for i in range(n):
        if A[i, i] == 0 and b[i] == 1:
            return "No"
    return "Yes"


print(is_solvable("Input.txt"))

