import pygame
import os
import time
from collections import deque
from datetime import date

# Window
Width, Height = 700, 650
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Path Finder v1.5")

# Font
pygame.font.init()

# Icon
icon = pygame.image.load(os.path.join("assets", "pathfinder.png"))
pygame.display.set_icon(icon)

# ---- Colors ----
# Grays
light_gray = (175, 175, 175)
medium_gray = (140, 140, 140)
dark_gray = (110, 110, 110)
# Primary, black and white
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)


class Rectangle:
    objs = deque([])  # registrar

    has_start, has_end = False, False
    start_coord, end_coord = (None, None), (None, None)

    def __init__(self, win, color, x, y, width, height):
        Rectangle.objs.append(self)
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

        self._hello = 'Hello'
        self.year = 1999
        self.month = 7
        self.day = 15

    @classmethod
    def clear_all(cls):
        Rectangle.has_start, Rectangle.has_end = False, False
        Rectangle.start_coord, Rectangle.end_coord = (None, None), (None, None)
        for obj in cls.objs:
            obj.is_wall = False
            obj.is_start = False
            obj.is_end = False
            obj.is_path = False
            obj.color = white

    @classmethod
    def clear_path(cls):
        for obj in cls.objs:
            if obj.is_path and not obj.is_start and not obj.is_end:
                obj.is_path = False
                obj.color = white



    def draw(self):
        pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.height))

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


    @property
    def age(self):
        today = date.today()
        return today.year - self.year - ((today.month, today.day) < (self.month, self.day))


class Button:
    # ---- Colors ----
    light_gray = (175, 175, 175)
    medium_gray = (140, 140, 140)
    dark_gray = (110, 110, 110)

    def __init__(self, win, color, x, y, width, height, text="", text_color=None, font="arial", font_size=20):
        self.Win = win
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = (0, 0, 0) if text_color is None else text_color
        self.font = font
        self.font_size = font_size
        self.font_label = pygame.font.SysFont(self.font, self.font_size)
        self.text_label = self.font_label.render(str(self.text), 1, self.text_color)
        self.clickable = True

    def draw(self):
        # Draw Button then Text
        pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.height))
        self.Win.blit(self.text_label, ((self.width // 2) + self.x - self.text_label.get_width() // 2,
                                        (self.height // 2) + self.y - self.text_label.get_height() // 2))

    def hover(self, mouse):
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            self.color = medium_gray
            return True
        else:
            self.color = light_gray
            return False

    def change_text(self, new_text):
        self.text_label = self.font_label.render(str(new_text), 1, self.text_color)

    def change_font_size(self, size):
        self.font_label = pygame.font.SysFont(self.font, int(size))

    def alt_text_state(self, click, text, color, size, alt_text, alt_text_size):
        """Uses if a button is clickable and is clicked
            to change to a text format and then back to the alternate."""
        if self.clickable and click:
            self.change_font_size(size)
            self.change_text(text)
            self.color = color
        else:
            self.change_font_size(alt_text_size)
            self.change_text(alt_text)

    def can_click(self, mouse, click):
        if not self.hover(mouse) and click:
            self.clickable = False
            return False
        if not self.hover(mouse) and not click:
            self.clickable = True
            return True

    def handle_mouse(self, mouse, click):
        self.can_click(mouse, click)
        self.hover(mouse)

    def call_func(self, func, click):
        if self.clickable and click:
            self.color = dark_gray
            self.draw()
            pygame.display.update()

            print('Hi mom')
            time.sleep(.5)
            # return  # main_gui()
            func()


def main():
    run = True
    fps = 60
    timer, delay = 0, 12
    grid_x, grid_y = 7, 7
    clock = pygame.time.Clock()

    # TODO change to bool

    # Make 7x7 grid
    grid = [[Rectangle(Win, white, ((x + 1) * 150 - 2 * (x - 10)) // 2,
                       (((y + 1) * 100 - 2 * (y - 10) + 50 * y) // 2) + 10, (140 - 2 * 2) // 2,
                       (140 - 2 * 2) // 2) for x in range(grid_x)] for y in range(grid_y)]

    def is_wall(cell_val, grid, node_col, node_row):
        """Wall has been tested and approved
        Test:
            for letter in "URDL":
                for i in range(7):
                    for j in range(7):
                        print(is_wall(letter, grid, i, j), letter, i, j)
        """
        # -------------- U move --------------
        if cell_val == "U":
            if not 6 >= node_col > 0:
                return True
            return True if grid[node_col - 1][node_row].is_wall is True else False
        # -------------- R move --------------
        if cell_val == "R":
            if not 6 > node_row >= 0:
                return True
            return True if grid[node_col][node_row + 1].is_wall is True else False
        # -------------- D move --------------
        if cell_val == "D":
            if not 6 > node_col >= 0:
                return True
            return True if grid[node_col + 1][node_row].is_wall is True else False
        # -------------- L move --------------
        if cell_val == "L":
            if not 6 >= node_row > 0:
                return True
            return True if grid[node_col][node_row - 1].is_wall is True else False

    def get_node_pos(path, node_col, node_row):
        path = [char for char in path]
        for j in range(len(path)):
            n = path[j]
            if n == "U":
                node_col -= 1
            if n == "R":
                node_row += 1
            if n == "D":
                node_col += 1
            if n == "L":
                node_row -= 1
        return node_col, node_row

    def check_paths(path, grid, node_col, node_row):
        # Start in node_Col and node_Row TODO have a linked list for each possible solution and the last coord
        path += ""
        visited_nodes = deque([])
        path = [char for char in path]
        for j in range(len(path)):
            node = path[j]
            # -------------- U move -------------------
            if node == "U":
                val = grid[node_col - 1][node_row]
                node_col -= 1
                visited_nodes.append([node_col, node_row])
                if val.is_end:
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True
            # -------------- R move -------------------
            if node == "R":
                val = grid[node_col][node_row + 1]
                node_row += 1
                visited_nodes.append([node_col, node_row])
                if val.is_end:
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True
            # -------------- D move -------------------
            if node == "D":
                val = grid[node_col + 1][node_row]
                node_col += 1
                visited_nodes.append([node_col, node_row])
                if val.is_end:
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True
            # -------------- U move -------------------
            if node == "L":
                val = grid[node_col][node_row - 1]
                node_row -= 1
                visited_nodes.append([node_col, node_row])
                if val.is_end:
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True

        else:
            return False

    def find_path(grid, node_col, node_row):
        queue = deque([""])
        while True:

            p = queue[0]

            if len(p) > 0:
                solution = check_paths(p, grid, node_col, node_row)
                if solution:
                    return solution
            # deque
            queue.popleft()

            # ------------------- U move ------------------------
            cur_col, cur_row = get_node_pos(p, node_col, node_row)
            wall = is_wall("U", grid, cur_col, cur_row)
            if wall:
                pass
            elif len(p) == 0:
                up = p + "U"
                queue.append(up)
            elif p[-1] != "D":
                up = p + "U"
                queue.append(up)
                solution = check_paths(p, grid, node_col, node_row)
                if solution:
                    return solution
            # ------------------ R move -------------------------
            cur_col, cur_row = get_node_pos(p, node_col, node_row)
            wall = is_wall("R", grid, cur_col, cur_row)
            if wall:
                pass
            elif len(p) == 0:
                right = p + "R"
                queue.append(right)
            elif p[-1] != "L":
                right = p + "R"
                queue.append(right)
                solution = check_paths(p, grid, node_col, node_row)
                if solution:
                    return solution
            # ----------------- D move --------------------------
            cur_col, cur_row = get_node_pos(p, node_col, node_row)
            wall = is_wall("D", grid, cur_col, cur_row)
            if wall:
                pass
            elif len(p) == 0:
                down = p + "D"
                queue.append(down)
            elif p[-1] != "U":
                down = p + "D"
                queue.append(down)
                solution = check_paths(p, grid, node_col, node_row)
                if solution:
                    return solution
            # ---------------- L move ---------------------------
            cur_col, cur_row = get_node_pos(p, node_col, node_row)
            wall = is_wall("L", grid, cur_col, cur_row)
            if wall:
                continue
            elif len(p) == 0:
                left = p + "L"
                queue.append(left)
            elif p[-1] != "R":
                left = p + "L"
                queue.append(left)
                solution = check_paths(p, grid, node_col, node_row)
                if solution:
                    return solution

    def redraw_window():
        Win.fill((25, 25, 25))
        for y in range(grid_y):
            for x in range(grid_x):
                grid[y][x].draw()
        pygame.display.update()

    # Next step is to generate a list of four moves and check all adjacent cells
    #    and find the end if its one cell away

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
                run = False

        # QUIT
        if keys[pygame.K_ESCAPE]:
            run = False
            quit()
        if keys[pygame.K_c]:
            Rectangle.clear_all()
        if keys[pygame.K_d]:
            # FIXME make finding path with no start and no end invalid
            if timer > delay:
                Rectangle.clear_path()
                #  TODO make all funcs accept start coord without spliting it out
                # print(check_paths("RRDDLL", grid, Rectangle.start_coord[0], Rectangle.start_coord[1]))
                # print(Rectangle.start_coord, Rectangle.end_coord, Rectangle.has_start, Rectangle.has_end)
                path = find_path(grid, Rectangle.start_coord[0], Rectangle.start_coord[1])

                for i in range(len(path[1]) - 1):
                    x, y = path[1][i]
                    # print(x, y)
                    grid[x][y].color = (255, 255, 0)
                    grid[x][y].is_path = True
                timer = 0
        if keys[pygame.K_RETURN]:
            find_path(grid, Rectangle.start_coord, Rectangle.end_coord)

        # Iterate through the grid
        for y in range(grid_y):
            for x in range(grid_x):
                # End
                if grid[x][y].hover(mouse) and keys[pygame.K_e] and Rectangle.has_end is False:
                    Rectangle.end_coord = (x, y)
                    grid[x][y].color = red
                    grid[x][y].is_wall = False
                    grid[x][y].is_start = False
                    grid[x][y].is_end = True
                    Rectangle.has_end = True

                # Start
                elif grid[x][y].hover(mouse) and keys[pygame.K_s] and Rectangle.has_start is False:
                    Rectangle.start_coord = (x, y)
                    grid[x][y].color = green
                    grid[x][y].is_wall = False
                    grid[x][y].is_start = True
                    grid[x][y].is_end = False
                    Rectangle.has_start = True

                # Walls
                elif grid[x][y].hover(mouse) and click[0] and not keys[pygame.K_s] and not keys[pygame.K_e]:
                    grid[x][y].color = black
                    grid[x][y].is_wall = True
                    Rectangle.has_end = False if grid[x][y].is_end is True else Rectangle.has_end
                    Rectangle.has_start = False if grid[x][y].is_start is True else Rectangle.has_start
                    grid[x][y].is_start = False
                    grid[x][y].is_end = False

                # Clear
                elif grid[x][y].hover(mouse) and click[2] and not keys[pygame.K_s] and not keys[pygame.K_e]:
                    grid[x][y].color = white
                    grid[x][y].is_wall = False
                    Rectangle.has_end = False if grid[x][y].is_end is True else Rectangle.has_end
                    Rectangle.has_start = False if grid[x][y].is_start is True else Rectangle.has_start
                    grid[x][y].is_start = False
                    grid[x][y].is_end = False

        # print(is_wall("L", grid, 5, 5))
        timer += 1


# ------------------- Main Menu ---------------------

def main_menu():
    run = True
    info = False
    fps = 60
    timer, delay = 0, 12

    clock = pygame.time.Clock()

    # Main Fonts
    main_font = pygame.font.SysFont("comicsans", 60)
    info_font = pygame.font.SysFont("sans", 15)
    main_label = main_font.render("Pathfinder v1", 1, (119, 209, 225))

    # Info text
    info_color = (255, 255, 225)
    info_label = info_font.render("Press i for info or Space to continue.", 1, info_color)
    info_text_label = info_font.render("Use the mouse to hover over the cell that you want to change.", 1, info_color)
    info_text_label2 = info_font.render(
        "Left click puts down walls, Right click clears the cell, and while hovering over a cell", 1, info_color)
    info_text_label3 = info_font.render("press the S and E keys to put down the Start and End nodes respectively.", 1,
                                        info_color)
    info_text_label4 = info_font.render("The C key clears the screen.", 1, info_color)

    # Buttons
    bfs_b = Button(Win, (175, 175, 175), Width // 2 - 50 - 75, Height - 200, 100, 25, "BFS", font_size=20)
    dfs_b = Button(Win, (175, 175, 175), Width // 2 - 50 + 75, Height - 200, 100, 25, "Dijkstra", font_size=20)

    def redraw_window():
        Win.fill((0, 0, 0))
        bfs_b.draw()
        dfs_b.draw()

        Win.blit(main_label, (Width // 2 - main_label.get_width() // 2, Height // 2 - main_label.get_height() // 2))
        Win.blit(info_label,
                 (Width // 2 - info_label.get_width() // 2, Height // 2 - info_label.get_height() // 2 + 50))
        if info:
            Win.blit(info_text_label, (
                Width // 2 - info_text_label.get_width() // 2,
                Height // 2 - info_text_label.get_height() // 2 + 100 + 12))
            Win.blit(info_text_label2, (
                Width // 2 - info_text_label2.get_width() // 2,
                Height // 2 - info_text_label2.get_height() // 2 + 150 + 12))
            Win.blit(info_text_label3, (
                Width // 2 - info_text_label3.get_width() // 2,
                Height // 2 - info_text_label3.get_height() // 2 + 200 + 12))
            Win.blit(info_text_label4, (
                Width // 2 - info_text_label4.get_width() // 2,
                Height // 2 - info_text_label4.get_height() // 2 + 250 + 12))
        pygame.display.update()

    def foo():
        print('sleeping for 3 seconds')
        time.sleep(3)
        print('In foo, just slept, leaving foo')
        return

    while run:
        clock.tick(fps)
        redraw_window()

        # Get mouse and keys events
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # DFS Button
        dfs_b.handle_mouse(mouse, click[0])
        dfs_b.alt_text_state(click[0], "Coming Soon...", (255, 0, 0), size=12,
                             alt_text='Dijkstra', alt_text_size=20)

        # BFS Button
        bfs_b.handle_mouse(mouse, click[0])

        # Call BFS Main Func
        if timer > delay:
            bfs_b.call_func(main, click[0])
            timer = 0

        # QUIT
        if keys[pygame.K_ESCAPE]:
            quit()

        # Display Info Toggle
        if keys[pygame.K_i]:
            if timer >= delay:
                info = not info
            timer = 0

        timer += 1


# main_menu()
if __name__ == "__main__":
    main_menu()
