import pygame
import os
from bfs import bfs
from dfs import dfs
from dijkstra import dijkstra
from collections import deque
from random import randint
from button import Button

version = 2.0

# Icon and Init
icon = pygame.image.load(os.path.join("assets", "pathfinder.png"))
pygame.display.set_icon(icon)
pygame.font.init()

# Grays
light_gray = (175, 175, 175)
medium_gray = (140, 140, 140)
dark_gray = (110, 110, 110)
very_dark_gray = (50, 50, 50)

# Primary, black and white colors
white = (230, 230, 230)
red = (255, 0, 0)
dark_red = (215, 0, 0)
yellow = (235, 235, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)


class Rectangle:
    cells = deque([])  # registrar

    has_start, has_end = False, False
    start_coord, end_coord = (None, None), (None, None)

    def __init__(self, win, color, x, y, width, height):
        Rectangle.cells.append(self)
        self.Win = win
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_path = False
        self.is_searched = False
        self.rect_obj = pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.height))

    @classmethod
    def clear_all(cls):
        Rectangle.has_start, Rectangle.has_end = False, False
        Rectangle.start_coord, Rectangle.end_coord = (None, None), (None, None)
        for obj in cls.cells:
            obj.is_wall = False
            obj.is_start = False
            obj.is_end = False
            obj.is_path = False
            obj.color = white

    @classmethod
    def clear_path(cls):
        for obj in cls.cells:
            if obj.is_path and not obj.is_start and not obj.is_end and not obj.is_wall:
                obj.is_path = False
                obj.color = white

    @classmethod
    def clear_searched(cls):
        for obj in cls.cells:
            if obj.is_searched and not obj.is_start and not obj.is_end and not obj.is_wall:
                obj.is_searched = False
                obj.color = white
            if obj.is_end:
                obj.color = red

    @classmethod
    def fill_grid(cls):
        cls.has_start, cls.has_end = False, False
        cls.start_coord, cls.end_coord = (None, None), (None, None)
        for obj in cls.cells:
            obj.is_start = False
            obj.is_end = False
            obj.is_path = False
            obj.is_wall = True
            obj.color = black

    def resize(self, height, width, x, y, grid_x, grid_y, offset):
        self.x = width // grid_x * x + offset + 2
        self.y = height // grid_y * y + offset + 2
        self.width = width // grid_x - offset
        self.height = height // grid_y - offset

    def draw(self):
        # TODO make modular with screen
        self.rect_obj = pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.height))

    def make_wall(self):
        self.is_end = False
        self.is_start = False
        self.is_wall = True
        self.color = (0, 0, 0)

    def hover(self, mouse):
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            return True
        else:
            return False


def main(Width, Height, Win, alg='BFS'):
    run = True
    fps = 60
    clock = pygame.time.Clock()
    timer, delay = 0, 12
    grid_x, grid_y = 44, 22
    offset = 3

    grid = [[Rectangle(Win, white,
                       Height // grid_y * x + offset + 2,
                       Height // grid_y * y + offset + 2,
                       Height // grid_y - offset, Height // grid_y - offset)
             for y in range(grid_y)] for x in range(grid_x)]

    def redraw_window():
        Win.fill(very_dark_gray)
        for x in range(grid_x):
            for y in range(grid_y):
                grid[x][y].draw()
        pygame.display.update()

    def use_bfs(start_coord, wall_li, grid_x, grid_y):
        # Find Path
        level, parent_dict = bfs(start_coord, wall_li, (grid_x, grid_y))

        searched_nodes = []

        if Rectangle.end_coord not in parent_dict:
            level[Rectangle.end_coord] = float("INF")

        for i, j in level.items():
            if 0 < j <= level[Rectangle.end_coord]:
                searched_nodes.append(i)
        for i in range(len(searched_nodes)):
            x, y = searched_nodes[i]
            if grid[x][y].is_end:
                grid[x][y].color = dark_red
                break
            else:
                grid[x][y].color = dark_gray
                grid[x][y].is_searched = True
                redraw_window()
        if Rectangle.end_coord in parent_dict:
            end_node = Rectangle.end_coord
            end_parent = parent_dict[end_node]
            path = [end_parent]

            # trace back through parent_dict nodes to find the shortest path
            while end_parent is not None:
                end_parent = parent_dict[end_parent]
                path.append(end_parent)

            for cell in reversed(range(len(path) - 2)):
                x, y = path[cell]
                grid[x][y].color = yellow
                grid[x][y].is_path = True
                redraw_window()
        else:
            print('No Solution')

    def use_dfs(start_coord, wall_li, grid_x, grid_y, end):
        # Find Path
        visited, has_path = dfs(start_coord, wall_li, (grid_x, grid_y), end)

        for cell in range(1, len(visited)):
            x, y = visited[cell]
            grid[x][y].color = yellow
            grid[x][y].is_path = True
            redraw_window()
        if has_path:
            x, y = Rectangle.end_coord
            grid[x][y].color = dark_red
        else:
            print("No solution")

    def use_dijkstra(start_coord, wall_li, grid_x, grid_y):
        # Find Path
        level, parent_dict = dijkstra(start_coord, wall_li, (grid_x-1, grid_y-1))

        searched_nodes = []
        #
        # if Rectangle.end_coord not in parent_dict:
        #     level[Rectangle.end_coord] = float("INF")
        #
        # for i, j in level.items():
        #     if 0 < j <= level[Rectangle.end_coord]:
        #         searched_nodes.append(i)
        # for i in range(len(searched_nodes)):
        #     try:
        #         x, y = searched_nodes[i]
        #         if grid[x][y].is_end:
        #             grid[x][y].color = dark_red
        #             break
        #         else:
        #             grid[x][y].color = dark_gray
        #             grid[x][y].is_searched = True
        #             redraw_window()
        #     except IndexError:
        #         pass
        if Rectangle.end_coord in parent_dict:
            end_node = Rectangle.end_coord
            end_parent = parent_dict[end_node]
            path = [end_parent]

            # trace back through parent_dict nodes to find the shortest path
            while end_parent is not None:
                end_parent = parent_dict[end_parent]
                path.append(end_parent)

            for cell in reversed(range(len(path) - 2)):
                x, y = path[cell]
                grid[x][y].color = yellow
                grid[x][y].is_path = True
                redraw_window()
        else:
            print('No Solution')

    def draw_stairs(Width, Height):

        curr_x_id = 0
        curr_y_id = Height - 1

        while curr_x_id >= 0 and curr_y_id >= 0:
            grid[curr_x_id][curr_y_id].color = black
            grid[curr_x_id][curr_y_id].is_wall = True
            curr_x_id += 1
            curr_y_id -= 1
            redraw_window()

        curr_y_id += 2

        while curr_y_id <= Height - 2:
            grid[curr_x_id][curr_y_id].color = black
            grid[curr_x_id][curr_y_id].is_wall = True
            curr_x_id += 1
            curr_y_id += 1
            redraw_window()

        else:
            x, y = 42, 19
            grid[x][y].color = black
            grid[x][y].is_wall = True
            redraw_window()


    while run:
        # Update window
        clock.tick(fps)
        redraw_window()

        # Get mouse and keys events
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.VIDEORESIZE:
                Win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                Width = event.w
                Height = event.h

                for x in range(grid_x):
                    for y in range(grid_y):
                        grid[x][y].resize(Height, Width, x, y, grid_x, grid_y, offset)

        # QUIT
        if keys[pygame.K_ESCAPE]:
            raise SystemExit
        # Clear all cells
        if keys[pygame.K_c] and keys[pygame.K_LSHIFT]:
            Rectangle.clear_all()
        if keys[pygame.K_m]:
            # TODO make a full maze maker
            if timer > delay:
                for node in range(len(Rectangle.cells)):
                    r = randint(0, 100)
                    if r < 20 and not Rectangle.cells[node].is_start and not Rectangle.cells[node].is_end:
                        Rectangle.cells[node].is_wall = True
                        Rectangle.cells[node].color = black
                        Rectangle.cells[node].is_start = False
                        Rectangle.cells[node].is_end = False
                        Rectangle.cells[node].is_path = False
                timer = 0

        if keys[pygame.K_b] and keys[pygame.K_LSHIFT]:
            Rectangle.fill_grid()
        if keys[pygame.K_q]:
            draw_stairs(grid_x, grid_y)

        # Find path
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            if timer > delay and Rectangle.has_start and Rectangle.has_end:

                Rectangle.clear_path()
                Rectangle.clear_searched()
                wall_li = [(x, y) for y in range(grid_y) for x in range(grid_x) if grid[x][y].is_wall]
                # TODO make the main_menu accessible from main
                if alg == 'BFS':
                    use_bfs(Rectangle.start_coord, wall_li, grid_x - 1, grid_y - 1)

                elif alg == 'DFS':
                    use_dfs(Rectangle.start_coord, wall_li, grid_x - 1, grid_y - 1, Rectangle.end_coord)
                elif alg == 'DIJKSTRA':
                    use_dijkstra(Rectangle.start_coord, wall_li, grid_x, grid_y)
                timer = 0

        # Iterate through the grid
        # todo make this more efficient
        for x in range(grid_x):
            for y in range(grid_y):

                # Walls
                if grid[x][y].hover(mouse) and click[0] and not keys[pygame.K_s] and not keys[pygame.K_e]:
                    grid[x][y].color = black
                    grid[x][y].is_wall = True
                    Rectangle.has_end = False if grid[x][y].is_end else Rectangle.has_end
                    Rectangle.has_start = False if grid[x][y].is_start else Rectangle.has_start
                    grid[x][y].is_start = False
                    grid[x][y].is_end = False

                # End
                elif grid[x][y].hover(mouse) and not grid[x][y].is_start and keys[pygame.K_e] and not Rectangle.has_end:
                    Rectangle.end_coord = (x, y)
                    grid[x][y].color = red
                    grid[x][y].is_wall = False
                    grid[x][y].is_start = False
                    grid[x][y].is_end = True
                    Rectangle.has_end = True

                # Start
                elif grid[x][y].hover(mouse) and not grid[x][y].is_end and keys[pygame.K_s] and not Rectangle.has_start:
                    Rectangle.start_coord = (x, y)
                    grid[x][y].color = green
                    grid[x][y].is_wall = False
                    grid[x][y].is_start = True
                    grid[x][y].is_end = False
                    Rectangle.has_start = True

                # Clear
                elif grid[x][y].hover(mouse) and click[2] and not keys[pygame.K_s] and not keys[pygame.K_e]:
                    grid[x][y].color = white
                    grid[x][y].is_wall = False
                    Rectangle.has_end = False if grid[x][y].is_end is True else Rectangle.has_end
                    Rectangle.has_start = False if grid[x][y].is_start is True else Rectangle.has_start
                    grid[x][y].is_start = False
                    grid[x][y].is_end = False

        timer += 1


# ------------------- Main Menu ---------------------
def main_menu(ver):
    run = True
    info = False
    fps = 60
    timer, delay = 0, 12
    Width, Height = 1400, 700
    clock = pygame.time.Clock()
    Win = pygame.display.set_mode((Width, Height), pygame.RESIZABLE, 32)
    pygame.display.set_caption(f"Path Finder v{ver}")
    # Main Fonts
    main_font = pygame.font.SysFont("comicsans", 60)
    info_font = pygame.font.SysFont("sans", 15)
    main_label = main_font.render(f"Pathfinder v{ver}", 1, (119, 209, 225))

    # Info text
    info_color = (255, 255, 225)
    info_label = info_font.render("Press i for info or Space to continue.", 1, info_color)
    info_text_label = info_font.render("Use the mouse to hover over the cell that you want to change.", True,
                                       info_color)

    # Buttons
    bfs_b = Button(Win, light_gray, x=Width // 2 - 50 - 75, y=Height - 200, width=100, height=25, win_w=Width,
                   win_h=Height, text="BFS", font_size=20)
    dfs_b = Button(Win, light_gray, x=Width // 2, y=Height - 200, width=100, height=25, win_w=Width,
                   win_h=Height, text="DFS", font_size=20)
    dijkstra_b = Button(Win, light_gray, x=Width // 2 - 50 + 75, y=Height - 200, width=100, height=25, win_w=Width,
                        win_h=Height, text="Dijkstra", font_size=20)

    def redraw_window():
        Win.fill((0, 0, 0))
        bfs_b.draw_resize(Width, Height, -.05, .15)
        dfs_b.draw_resize(Width, Height, 0, .225)
        dijkstra_b.draw_resize(Width, Height, .05, .15)

        Win.blit(main_label, (Width // 2 - main_label.get_width() // 2, Height // 2 - main_label.get_height() // 2))
        Win.blit(info_label,
                 (Width // 2 - info_label.get_width() // 2, Height // 2 - info_label.get_height() // 2 + 50))
        if info:
            Win.blit(info_text_label, (0, 0))

        pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.VIDEORESIZE:
                Win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                Width = event.w
                Height = event.h
        clock.tick(fps)
        redraw_window()

        # Get mouse and keys events
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # BFS Button
        bfs_b.handle_mouse(mouse, click[0])

        # Call BFS Main Func
        if bfs_b.clickable:
            bfs_b.call_func(main, click[0], Width, Height, Win, "BFS")

        # DFS Button
        dfs_b.handle_mouse(mouse, click[0])

        # Call DFS Main Func
        if dfs_b.clickable:
            dfs_b.call_func(main, click[0], Width, Height, Win, "DFS")

        # Dijkstra Button
        dijkstra_b.handle_mouse(mouse, click[0])
        # dijkstra_b.alt_text_state(click[0], "Coming Soon...", (255, 0, 0), size=12,
        #                           alt_text='Dijkstra', alt_text_size=20)
        if dijkstra_b.clickable:
            dijkstra_b.call_func(main, click[0], Width, Height, Win, "DIJKSTRA")

        if keys[pygame.K_ESCAPE]:
            raise SystemExit

        # Display Info Toggle
        if keys[pygame.K_i]:
            if timer >= delay:
                info = not info
                timer = 0

        timer += 1


if __name__ == "__main__":
    main_menu(version)
