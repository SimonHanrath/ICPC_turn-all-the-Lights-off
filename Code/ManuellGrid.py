import pygame
from Full_Solution import Grid
import numpy as np

def get_clicked_rect(click_pos, cell_size):
    return [int(click_pos[1]/cell_size), int(click_pos[0]/cell_size)]

def rect_to_pixel(pos, cell_size):
    return [cell_size*pos[1], cell_size*pos[0]]

def value_to_color(value, color1=(255, 255, 255), color2=(0, 0, 0)):
    if value:
        return color1
    else:
        return color2

def draw_grid(grid, window_size, surface, color1=(0, 0, 0), color2=(205, 205, 102), color3=(255, 255, 255)):
    grid_size = len(grid)
    cell_size = int(window_size/grid_size)
    for i in range(grid_size):
        for j in range(grid_size):
            pygame.draw.rect(surface, value_to_color(grid[i][j], color1, color2),
                             pygame.Rect(0+i*cell_size, 0+j*cell_size, cell_size, cell_size))
            pygame.draw.rect(surface, color3,
                             pygame.Rect(0 + i * cell_size, 0 + j * cell_size, cell_size, cell_size),1)

def draw_solution(surface, solution, cell_size, color):
    for pos in solution:
        upper_left_pos = rect_to_pixel(pos, cell_size)
        offset = int(cell_size/2)
        center_pos = [upper_left_pos[0]+offset, upper_left_pos[1]+offset]
        pygame.draw.circle(surface, color, center_pos, offset/2)


grid = np.zeros([3,3], int)
#grid = np.array([[1,0,1],[0,1,1],[0,1,1]])
myGrid = Grid(grid)
solution = []
show_solution = False
window_size = 500
cell_size = int(window_size/myGrid.grid_size)
pygame.init()
pygame.display.set_caption('Manuell Grid (use space to toggle solution)')
window_surface = pygame.display.set_mode((window_size, window_size))

clock = pygame.time.Clock()
is_running = True

while is_running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            clicked_rect = get_clicked_rect(event.pos, cell_size)
            myGrid.grid = myGrid.simulate_click(myGrid.grid, clicked_rect)
            if clicked_rect in solution:
                solution.remove(clicked_rect)
            else:
                solution.append(clicked_rect)
                #solution = myGrid.get_full_solution()

        if event.type == pygame.KEYDOWN:
            show_solution = not show_solution

        if event.type == pygame.QUIT:
            is_running = False

    draw_grid(myGrid.grid, window_size, window_surface)
    if show_solution:
        draw_solution(window_surface, solution, cell_size, (255, 0, 0))
    pygame.display.update()