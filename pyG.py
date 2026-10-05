from tkinter import messagebox, Tk
import pygame
import sys

window_width = 500
window_height = 500

pygame.init()
window = pygame.display.set_mode((window_width, window_height))

column = 25
rows = 25

box_width = window_width // column
box_height = window_height // rows

grid = []
queue = []
path = []


class Box():
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queue = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height,
                                      box_width - 2, box_height - 2))

    def set_neighbours(self):
        if self.x < column - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])


# Creating grid
for i in range(column):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set neighbours 
for i in range(column):
    for j in range(rows):
        grid[i][j].set_neighbours()

# Set start box
start_box = grid[0][0]
start_box.start = True
start_box.visited = True
start_box.queue = True
queue.append(start_box)


def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():
            # For quitting the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse motion 
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                x = int(pos[0] // box_width)
                y = int(pos[1] // box_height)

              #for walls
                if event.buttons[0]:
                    if 0 <= x < column and 0 <= y < rows:
                        if not grid[x][y].start and not grid[x][y].target:
                            grid[x][y].wall = True

            # Mouse button click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = int(pos[0] // box_width)
                y = int(pos[1] // box_height)

                if 0 <= x < column and 0 <= y < rows:
                    if event.button == 3 and not target_box_set:  # Right click
                        if not grid[x][y].start:
                            target_box = grid[x][y]
                            target_box.wall = False  
                            target_box.target = True
                            target_box_set = True
                            print(f"Target set at ({x}, {y})")

                    elif event.button == 2:  # Middle click 
                        grid[x][y].wall = False
                        grid[x][y].target = False
                        print(f"Box cleared at ({x}, {y})")

            # Start algo
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queue and not neighbour.wall:
                            neighbour.queue = True
                            neighbour.prior = current_box  
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution", "There is no solution")
                    searching = False  

        window.fill((0, 0, 0))

        # Draw all boxes
        for i in range(column):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50, 50, 50))  # Base color (gray)

                if box.queue:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))
                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (90, 90, 90))
                if box.target:
                    box.draw(window, (200, 200, 0))

        pygame.display.flip()


main()