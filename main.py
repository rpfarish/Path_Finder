import pygame
import random
import os
import time

maze1 = [['|', '-', '-', '-', '-', '-', '|'],
         ['|', ' ', ' ', ' ', ' ', ' ', '|'],
         ['|', ' ', ' ', ' ', ' ', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', '+', ' ', ' ', ' ', '|'],
         ['|', ' ', '+', 'X', ' ', ' ', '|'],
         ['|', '-', '-', '-', '-', '-', '|']]
maze2 = [['|', '-', '-', '-', '-', '-', '|'],
         ['|', '+', ' ', ' ', ' ', 'X', '|'],
         ['|', '+', ' ', ' ', ' ', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', ' ', ' ', ' ', ' ', '|'],
         ['|', 'S', ' ', '+', ' ', ' ', '|'],
         ['|', '-', '-', '-', '-', '-', '|']]


def find_path(gui_maze):
    def make_maze(wall_li, start, end):
        for i in range(len(wall_li)):
            if wall_li[i] is True:
                wall_li[i] = "+"
            elif wall_li[i] is False:
                wall_li[i] = " "
        wall_li[start - 1] = "S"
        wall_li[end - 1] = "X"

        new_maze = [['|', '-', '-', '-', '-', '-', '|'],
                    ['|', wall_li[0], wall_li[1], wall_li[2], wall_li[3], wall_li[4], '|'],
                    ['|', wall_li[5], wall_li[6], wall_li[7], wall_li[8], wall_li[9], '|'],
                    ['|', wall_li[10], wall_li[11], wall_li[12], wall_li[13], wall_li[14], '|'],
                    ['|', wall_li[15], wall_li[16], wall_li[17], wall_li[18], wall_li[19], '|'],
                    ['|', wall_li[20], wall_li[21], wall_li[22], wall_li[23], wall_li[24], '|'],
                    ['|', '-', '-', '-', '-', '-', '|']]

        # for node in maze1:
        #     print(node)
        return new_maze



    # print(text_maze.readline())

    def find_start(maze):
        if maze is not None:
            for w in range(6):
                for u in range(6):
                    s = maze[w][u]
                    if s == 'S':
                        return w, u

    col, row = find_start(gui_maze)

    start = time.perf_counter()
    # Start Node
    # col = 5
    # row = 1
    gui_maze[col][row] = "S"

    # Print Maze
    for i in gui_maze:
        print(i)
    print("-" * 35)

    def is_wall(cell_val, maze, node_col, node_row):
        # ----------------------- U move --------------------------
        if cell_val == "U":
            adj_cell = maze[node_col - 1][node_row]
            if adj_cell == "-" or adj_cell == "|" or adj_cell == "+":
                return True
            else:
                return False

        # ----------------------- R move --------------------------
        if cell_val == "R":
            adj_cell = maze[node_col][node_row + 1]
            if adj_cell == "-" or adj_cell == "|" or adj_cell == "+":
                return True
            else:
                return False

        # ----------------------- D move --------------------------
        if cell_val == "D":
            adj_cell = maze[node_col + 1][node_row]
            if adj_cell == "-" or adj_cell == "|" or adj_cell == "+":
                return True
            else:
                return False

        # ----------------------- L move --------------------------
        if cell_val == "L":
            adj_cell = maze[node_col][node_row - 1]
            if adj_cell == "-" or adj_cell == "|" or adj_cell == "+":
                return True
            else:
                return False

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

    def visualize_path(maze, path):
        print(len(path), path)
        for p in path:
            if p is True:
                pass
            else:
                for s in p:
                    k = int(s[0])
                    j = int(s[1])
                    maze[k][j] = "#"
        return maze

    def check_paths(path, maze, node_col, node_row):
        # Start in node_Col and node_Row
        path += ""
        visited_nodes = []
        path = [char for char in path]
        # this is a list of what the path was to the end node

        for j in range(len(path)):

            node = path[j]

            # -------------- U move -------------------
            if node == "U":
                val = maze[node_col - 1][node_row]
                node_col -= 1
                visited_nodes.append([node_col, node_row])
                if val == "X":
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True

            # -------------- R move -------------------
            if node == "R":
                val = maze[node_col][node_row + 1]
                node_row += 1
                visited_nodes.append([node_col, node_row])
                if val == "X":
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True

            # -------------- D move -------------------
            if node == "D":
                val = maze[node_col + 1][node_row]
                node_col += 1
                visited_nodes.append([node_col, node_row])
                if val == "X":
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True

            # -------------- U move -------------------
            if node == "L":
                val = maze[node_col][node_row - 1]
                node_row -= 1
                visited_nodes.append([node_col, node_row])
                if val == "X":
                    if visited_nodes is not None:
                        return True, visited_nodes
                    else:
                        return True

    def all_paths(maze, node_col, node_row):
        queue = [""]
        while True:

            end_time = time.perf_counter()
            if end_time - start > 1:
                return None

            # queue.get
            e = queue[0]

            if len(e) > 0:
                solution = check_paths(e, maze, node_col, node_row)
                if solution:
                    return solution

            # deque
            queue.pop(0)

            # ------------------- U move ------------------------
            cur_col, cur_row = get_node_pos(e, node_col, node_row)
            wall = is_wall("U", maze, cur_col, cur_row)
            if wall:
                pass
            elif len(e) == 0:
                up = e + "U"
                queue.append(up)
            elif e[-1] != "D":
                up = e + "U"
                queue.append(up)
                solution = check_paths(e, maze, node_col, node_row)
                if solution:
                    return solution

            # ------------------ R move -------------------------
            cur_col, cur_row = get_node_pos(e, node_col, node_row)
            wall = is_wall("R", maze, cur_col, cur_row)
            if wall:
                pass
            elif len(e) == 0:
                right = e + "R"
                queue.append(right)
            elif e[-1] != "L":
                right = e + "R"
                queue.append(right)
                solution = check_paths(e, maze, node_col, node_row)
                if solution:
                    return solution

            # ----------------- D move --------------------------
            cur_col, cur_row = get_node_pos(e, node_col, node_row)
            wall = is_wall("D", maze, cur_col, cur_row)
            if wall:
                pass
            elif len(e) == 0:
                down = e + "D"
                queue.append(down)
            elif e[-1] != "U":
                down = e + "D"
                queue.append(down)
                solution = check_paths(e, maze, node_col, node_row)
                if solution:
                    return solution

            # ---------------- L move ---------------------------
            cur_col, cur_row = get_node_pos(e, node_col, node_row)
            wall = is_wall("L", maze, cur_col, cur_row)
            if wall:
                pass
            elif len(e) == 0:
                left = e + "L"
                queue.append(left)
            elif e[-1] != "R":
                left = e + "L"
                queue.append(left)
                solution = check_paths(e, maze, node_col, node_row)
                if solution:
                    return solution

    has_solution = True
    viz_maze = ""
    path_solution = all_paths(gui_maze, col, row)
    try:
        a = path_solution[1][-1][0]
        b = path_solution[1][-1][1]

        viz_maze = visualize_path(gui_maze, path_solution)
        gui_maze[a][b] = "X"
        for i in gui_maze:
            print(i)
    except TypeError:
        has_solution = False
        print("No solution")

    end = time.perf_counter()
    return end - start, viz_maze, has_solution


# --------------------------------------------------------------------gui-----------------------------------------------------------------


pygame.font.init()
icon = pygame.image.load(os.path.join("assets", "pathfinder.png"))
pygame.display.set_icon(icon)

# Window
Width, Height = 700, 650
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Path Finder v1.0")


def make_maze(wall_li, start, end):
    for i in range(len(wall_li)):
        if wall_li[i] is True:
            wall_li[i] = "+"
        elif wall_li[i] is False:
            wall_li[i] = " "
    wall_li[start - 1] = "S"
    wall_li[end - 1] = "X"

    maze1 = [['|', '-', '-', '-', '-', '-', '|'],
             ['|', wall_li[0], wall_li[1], wall_li[2], wall_li[3], wall_li[4], '|'],
             ['|', wall_li[5], wall_li[6], wall_li[7], wall_li[8], wall_li[9], '|'],
             ['|', wall_li[10], wall_li[11], wall_li[12], wall_li[13], wall_li[14], '|'],
             ['|', wall_li[15], wall_li[16], wall_li[17], wall_li[18], wall_li[19], '|'],
             ['|', wall_li[20], wall_li[21], wall_li[22], wall_li[23], wall_li[24], '|'],
             ['|', '-', '-', '-', '-', '-', '|']]

    # for node in maze1:
    #     print(node)
    return maze1


def gui_visualize_maze(maze5, grid):
    maze = make_maze_path_bool(maze5)
    print(maze)
    for pudding in range(len(maze)):
        for jello in range(1, 26):
            myobj = grid[jello]
            if maze[pudding] == "#":
                myobj.change_color((255, 255, 0))


def make_maze_path_bool(maze):
    the_li = []
    for i in range(1, 6):
        for j in range(1, 6):
            if maze[i][j] == "#":
                the_li.append(True)
            else:
                the_li.append(False)
    return the_li


class Rectangle:
    def __init__(self, win, color, x, y, width, height):
        self.Win = win
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.toggle = False
        self.is_start = False
        self.is_wall = False
        self.is_start = False
        self.is_end = False

    def draw(self):
        pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.height))

    def do_toggle(self):
        if self.toggle:
            self.color = (0, 0, 0)
        elif not self.toggle:
            self.color = (255, 255, 255)

    def toggle_start(self):
        if self.is_start:
            self.color = (0, 255, 0)
        elif not self.is_start:
            self.color = (255, 255, 255)

    def change_color(self, color):
        self.color = color

    def hover(self, mouse):
        if self.x < mouse[0] < self.x + self.width and \
                self.y < mouse[1] < self.y + self.height:
            return True
        else:
            return False


class CellBorder(Rectangle):
    def __init__(self, win, color, x, y, width, height):
        super().__init__(win, color, x, y, width, height)
        self.on = True
        self.line_width = 2

    def draw(self):
        #              x,  y,   w,   h
        # (Win, red, 100, 50, 100, 100)
        pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.line_width))  # U
        pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.line_width, self.height))  # L
        pygame.draw.rect(self.Win, self.color,
                         (self.x, self.y + self.height - self.line_width, self.width, self.line_width))  # D
        pygame.draw.rect(self.Win, self.color,
                         (self.x + self.width - self.line_width, self.y, self.line_width, self.height))  # R

    def right(self):
        self.x += self.width - self.line_width

    def down(self):
        self.y += self.height - self.line_width

    def up(self):
        self.y -= self.height - self.line_width

    def left(self):
        self.x -= self.width - self.line_width


class Button:
    # main_font = pygame.font.SysFont("comicsans", 50)
    # main_label = main_font.render(f"{cursor_x}", 1, (119, 209, 225))

    def __init__(self, win, color, x, y, width, height, text="", text_color=None, font="arial", font_size=20):
        self.Win = win
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        if text_color is None:
            self.text_color = (0, 0, 0)
        else:
            self.text_color = text_color
        self.font = font
        self.font_size = font_size
        self.font_label = pygame.font.SysFont(self.font, self.font_size)
        self.r_val = self.text_color[0]
        self.g_val = self.text_color[1]
        self.b_val = self.text_color[2]

        self.text_label = self.font_label.render(str(self.text), 1, (self.r_val, self.g_val, self.b_val))

    def draw(self):
        pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.height))

    def change_color(self, color):
        self.color = color

    def change_text_color(self, color):
        self.text_color = color

    def hover(self, mouse):
        if self.x < mouse[0] < self.x + self.width and \
                self.y < mouse[1] < self.y + self.height:
            return True
        else:
            return False

    def blit_text(self):
        self.Win.blit(self.text_label, ((self.width // 2) + self.x - self.text_label.get_width() // 2,
                                        (self.height // 2) + self.y - self.text_label.get_height() // 2))

    def change_text(self, new_text):
        self.text_label = self.font_label.render(str(new_text), 1, (self.r_val, self.g_val, self.b_val))


def main_gui():
    run = True

    BLUE = (0, 0, 255)
    white = (255, 255, 255)
    grey = (175, 175, 175)
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    red = (255, 0, 0)
    white = (255, 255, 255)
    white2 = (235, 235, 235)
    color1 = white
    button1 = Button(Win, grey, 250, 5, 200, 25, "Find Path", text_color=(0, 0, 0))
    button2 = Button(Win, grey, 50+5*2+400, 5, 100, 25, "Clear", text_color=(0, 0, 0))
    border = CellBorder(Win, red, 100, 50, 100, 100)

    # Make 1st Row
    highlight_box1 = Rectangle(Win, color1, 1 * 100 - 2 * -1, 50 + 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box2 = Rectangle(Win, color1, 2 * 100 - 2 * 0, 50 + 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box3 = Rectangle(Win, color1, 3 * 100 - 2 * 1, 50 + 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box4 = Rectangle(Win, color1, 4 * 100 - 2 * 2, 50 + 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box5 = Rectangle(Win, color1, 5 * 100 - 2 * 3, 50 + 2, 100 - 2 * 2, 100 - 2 * 2)

    # Make 2nd Row
    highlight_box6 = Rectangle(Win, color1, 1 * 100 - 2 * -1, 100 + 50, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box7 = Rectangle(Win, color1, 2 * 100 - 2 * 0, 100 + 50, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box8 = Rectangle(Win, color1, 3 * 100 - 2 * 1, 100 + 50, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box9 = Rectangle(Win, color1, 4 * 100 - 2 * 2, 100 + 50, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box10 = Rectangle(Win, color1, 5 * 100 - 2 * 3, 100 + 50, 100 - 2 * 2, 100 - 2 * 2)

    # Make 3nd Row
    highlight_box11 = Rectangle(Win, color1, 1 * 100 - 2 * -1, 2 * 100 + 50 - 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box12 = Rectangle(Win, color1, 2 * 100 - 2 * 0, 2 * 100 + 50 - 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box13 = Rectangle(Win, color1, 3 * 100 - 2 * 1, 2 * 100 + 50 - 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box14 = Rectangle(Win, color1, 4 * 100 - 2 * 2, 2 * 100 + 50 - 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box15 = Rectangle(Win, color1, 5 * 100 - 2 * 3, 2 * 100 + 50 - 2, 100 - 2 * 2, 100 - 2 * 2)

    # Make 4nd Row
    highlight_box16 = Rectangle(Win, color1, 1 * 100 - 2 * -1, 3 * 100 + 50 - 2 * 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box17 = Rectangle(Win, color1, 2 * 100 - 2 * 0, 3 * 100 + 50 - 2 * 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box18 = Rectangle(Win, color1, 3 * 100 - 2 * 1, 3 * 100 + 50 - 2 * 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box19 = Rectangle(Win, color1, 4 * 100 - 2 * 2, 3 * 100 + 50 - 2 * 2, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box20 = Rectangle(Win, color1, 5 * 100 - 2 * 3, 3 * 100 + 50 - 2 * 2, 100 - 2 * 2, 100 - 2 * 2)

    # Make 5nd Row
    highlight_box21 = Rectangle(Win, color1, 1 * 100 - 2 * -1, 4 * 100 + 50 - 2 * 3, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box22 = Rectangle(Win, color1, 2 * 100 - 2 * 0, 4 * 100 + 50 - 2 * 3, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box23 = Rectangle(Win, color1, 3 * 100 - 2 * 1, 4 * 100 + 50 - 2 * 3, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box24 = Rectangle(Win, color1, 4 * 100 - 2 * 2, 4 * 100 + 50 - 2 * 3, 100 - 2 * 2, 100 - 2 * 2)
    highlight_box25 = Rectangle(Win, color1, 5 * 100 - 2 * 3, 4 * 100 + 50 - 2 * 3, 100 - 2 * 2, 100 - 2 * 2)

    the_grid = {
        1: highlight_box1,
        2: highlight_box2,
        3: highlight_box3,
        4: highlight_box4,
        5: highlight_box5,
        6: highlight_box6,
        7: highlight_box7,
        8: highlight_box8,
        9: highlight_box9,
        10: highlight_box10,
        11: highlight_box11,
        12: highlight_box12,
        13: highlight_box13,
        14: highlight_box14,
        15: highlight_box15,
        16: highlight_box16,
        17: highlight_box17,
        18: highlight_box18,
        19: highlight_box19,
        20: highlight_box20,
        21: highlight_box21,
        22: highlight_box22,
        23: highlight_box23,
        24: highlight_box24,
        25: highlight_box25,
    }

    lost = False
    timer = 0
    button1_can_click = True
    button2_can_click = True
    delay = 12
    cursor_x = 1
    time_took = 0
    main_label = main_font.render(f"{time_took} Seconds", 1, (119, 209, 225))

    current_start = []
    current_end = []
    timer_click = 0
    off_click = True

    def redraw_window():
        # Draw everything here if it happens during the game
        # for balloon in balloons:
        #     balloon.draw(Win)
        Win.fill((0, 0, 0))
        # Win.fill((21, 104, 207))
        button1.draw()
        button2.draw()
        # Draw 5x5 grid; might make it a 5X9 grid idk
        # Rect params: x, y, width, height
        v_x = 100
        v_y = 50
        v_width = 2
        v_height = 500
        v_line_dist = 100 - v_width
        x_grid_width = 0
        # TOP LEFT CORNER (100,50)
        # TOP LEFT CORNER 1 TO THE RIGHT (200,50)

        # should = 100; (100*i+1) - (v_x-v_width)
        # Draw vertical lines
        for i in range(6):
            pygame.draw.rect(Win, grey, (v_x + v_line_dist * i, v_y, v_width, v_height - 8))
            x_grid_width = ((v_x + v_line_dist * i) - v_x)

        h_height = v_width
        h_width = x_grid_width
        # Draw horizontal lines
        for i in range(6):
            pygame.draw.rect(Win, grey, (v_x, v_y + v_line_dist * i, h_width, h_height))

        # Need to put each square location into a class
        highlight_box1.draw()
        highlight_box2.draw()
        highlight_box3.draw()
        highlight_box4.draw()
        highlight_box5.draw()
        highlight_box6.draw()
        highlight_box7.draw()
        highlight_box8.draw()
        highlight_box9.draw()
        highlight_box10.draw()
        highlight_box11.draw()
        highlight_box12.draw()
        highlight_box13.draw()
        highlight_box14.draw()
        highlight_box15.draw()
        highlight_box16.draw()
        highlight_box17.draw()
        highlight_box18.draw()
        highlight_box19.draw()
        highlight_box20.draw()
        highlight_box21.draw()
        highlight_box22.draw()
        highlight_box23.draw()
        highlight_box24.draw()
        highlight_box25.draw()

        # border.draw()

        if lost:
            quit()

        Win.blit(main_label, (0, 0))
        button1.blit_text()
        button2.blit_text()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        main_label = main_font.render(f"{time_took} Seconds", 1, (119, 209, 225))
        keys = pygame.key.get_pressed()
        keys_mod = pygame.key.get_mods()
        cell = the_grid[cursor_x]
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        # print(mouse)

        for jello in range(1, 26):
            myobj = the_grid[jello]
            if myobj.hover(mouse):
                cursor_x = jello
                pass

        if timer_click >= delay:
            for jello in range(1, 26):
                myobj = the_grid[jello]
                if myobj.color == (255, 0, 0):
                    myobj.is_start = True
                if myobj.hover(mouse) and click[0] and myobj.color != (0, 0, 0):
                    myobj.change_color((0, 0, 0))
                    myobj.is_wall = True
                    myobj.is_start = False
                    myobj.is_end = False
                elif myobj.hover(mouse) and click[2]:
                    myobj.change_color((255, 255, 255))
                    myobj.is_wall = False
                    myobj.is_start = False
                    myobj.is_end = False

                timer_click = 0

        # print(cell.color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not button1.hover(mouse) and click[0]:
            button1_can_click = False
        if not button1.hover(mouse) and not click[0]:
            button1_can_click = True

        if not button1.hover(mouse):
            button1.change_color((175, 175, 175))
        # 250, 5, 200, 25
        if button1.hover(mouse) and button1_can_click:
            if timer >= delay:
                button1.change_color((140, 140, 140))
                if button1.hover(mouse) and click[0] and button1_can_click:
                    button1.change_text("Find Path")
                    button1.change_color((110, 110, 110))
                    maze = []
                    if len(current_start) == 1 and len(current_end) == 1:
                        for i in the_grid:
                            maze.append(the_grid[i].is_wall)
                            if the_grid[i].color == (255, 255, 0):
                                the_grid[i].change_color((255, 255, 255))
                        new_maze = make_maze(maze, current_start[0], current_end[0])
                        time_took, got_maze, has_sol = find_path(new_maze)

                        time_took = time_took.__round__(3)
                        bool_maze = make_maze_path_bool(new_maze)
                        for wj in range(len(bool_maze)):
                            mi_obj = the_grid[wj+1]
                            if bool_maze[wj]:

                                mi_obj.change_color((255,255,0))
                    else:
                        button1.change_text("Error")

                        button1.change_color((255, 0, 0))
                        button1.change_text_color((0, 0, 0))
                if not click[0]:
                    button1.change_text("Find Path")
            else:
                button1.change_color((175, 175, 175))
                if not click[0] or not button1.hover(mouse):
                    button1.change_text("Find Path")

                timer = 0
        if keys[pygame.K_s]:
            if timer >= delay:
                cell.is_wall = False
                if len(current_start) == 0:
                    cell.is_start = True
                    cell.change_color((0, 255, 0))
                    current_start.append(cursor_x)
                else:
                    lst_cell = current_start[0]
                    lst_cell_obj = the_grid[lst_cell]
                    lst_cell_obj.change_color((255, 255, 255))
                    current_start.pop(0)
                    cell.change_color((0, 255, 0))
                    current_start.append(cursor_x)
                timer = 0
        if keys[pygame.K_BACKSPACE]:
            cell.color = (255, 255, 255)
        if keys[pygame.K_e]:
            if timer >= delay:
                cell.is_wall = False
                if len(current_end) == 0:
                    cell.is_start = True
                    cell.change_color((255, 0, 0))
                    current_end.append(cursor_x)
                else:
                    lst_cell = current_end[0]
                    lst_cell_obj = the_grid[lst_cell]
                    lst_cell_obj.change_color((255, 255, 255))
                    current_end.pop(0)
                    cell.change_color((255, 0, 0))
                    current_end.append(cursor_x)

                timer = 0

        if keys[pygame.K_SPACE]:
            # get the state of the current box
            if timer >= delay:
                # highlight_box1.change_color((255, 255, 255))
                if cell.toggle:
                    cell.toggle = False
                    cell.is_wall = False
                elif not cell.toggle:
                    cell.is_wall = True
                    cell.toggle = True
                cell.do_toggle()
                timer = 0
        if keys[pygame.K_ESCAPE]:
            quit()

        if keys[pygame.K_RIGHT]:
            if timer >= delay:
                if 0 < cursor_x < 25 and cursor_x % 5 != 0:
                    cursor_x += 1
                    border.right()
                timer = 0
        if keys[pygame.K_LEFT]:
            if timer >= delay:
                if 0 < cursor_x <= 25 and cursor_x != 1 and cursor_x != 6 and cursor_x != 11 and cursor_x != 16 and cursor_x != 21:
                    cursor_x -= 1
                    border.left()
                timer = 0
        if keys[pygame.K_UP]:
            if timer >= delay:
                if 6 <= cursor_x <= 25:
                    cursor_x -= 5
                    border.up()
                timer = 0
        if keys[pygame.K_DOWN]:
            if timer >= delay:
                if 0 < cursor_x <= 20:
                    cursor_x += 5
                    border.down()
                timer = 0

        if not button2.hover(mouse) and click[0]:
            button2_can_click = False
        if not button2.hover(mouse) and not click[0]:
            button2_can_click = True

        if not button2.hover(mouse):
            button2.change_color((175, 175, 175))
        # 250, 5, 200, 25
        if button2.hover(mouse) and button2_can_click:
            if timer >= delay:
                button2.change_color((140, 140, 140))
                if button2.hover(mouse) and click[0] and button2_can_click:
                    button2.change_text("Clear")
                    button2.change_color((110, 110, 110))
                    current_start.clear()
                    current_end.clear()
                    for jello in range(1, 26):
                        myobj = the_grid[jello]
                        myobj.change_color((255, 255, 255))
                        myobj.is_wall = False
                        myobj.is_start = False
                        myobj.is_end = False

        if keys[pygame.K_c]:
            current_start.clear()
            current_end.clear()
            for jello in range(1, 26):
                myobj = the_grid[jello]
                myobj.change_color((255, 255, 255))
                myobj.is_wall = False
                myobj.is_start = False
                myobj.is_end = False

        # print("\n" * 3)

        timer += 1
        timer_click += 5


def main_menu():
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 60)
    info_font = pygame.font.SysFont("sans", 15)
    main_label = main_font.render("Pathfinder v1", 1, (119, 209, 225))
    info_color = (255, 255, 225)
    # info_color = (119, 209, 225)
    info_label = info_font.render("Press i for info or Space to continue.", 1, info_color)
    info_text_label = info_font.render("Use the mouse to hover over the cell that you want to change.", 1, info_color)
    info_text_label2 = info_font.render("Left click puts down walls, Right click clears the cell, and while hovering over a cell", 1, info_color)
    info_text_label3 = info_font.render("press the S and E keys to put down the Start and End nodes respectively.", 1, info_color)
    info_text_label4 = info_font.render("The C key clears the screen.", 1, info_color)

    run = True
    info = False

    def redraw_window():
        Win.fill((0, 0, 0))
        Win.blit(main_label, (Width // 2 - main_label.get_width() // 2, Height // 2 - main_label.get_height() // 2))
        Win.blit(info_label,
                 (Width // 2 - info_label.get_width() // 2, Height // 2 - info_label.get_height() // 2 + 50))
        if info:
            Win.blit(info_text_label, (
                Width // 2 - info_text_label.get_width() // 2, Height // 2 - info_text_label.get_height() // 2 + 100))
            Win.blit(info_text_label2, (
                Width // 2 - info_text_label2.get_width() // 2, Height // 2 - info_text_label2.get_height() // 2 + 150))
            Win.blit(info_text_label3, (
                Width // 2 - info_text_label3.get_width() // 2, Height // 2 - info_text_label3.get_height() // 2 + 200))
            Win.blit(info_text_label4, (
                Width // 2 - info_text_label4.get_width() // 2, Height // 2 - info_text_label4.get_height() // 2 + 250))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()

        # print(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_SPACE]:
            # TODO Make a loading bar
            return main_gui()
        if keys[pygame.K_ESCAPE]:
            quit()
        if keys[pygame.K_i]:
            info = True


maze = main_menu()
