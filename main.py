import pygame
import os
import time

pygame.font.init()
icon = pygame.image.load(os.path.join("assets", "pathfinder.png"))
pygame.display.set_icon(icon)

# Window
Width, Height = 700, 650
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Path Finder v1.0")

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


def find_path(gui_maze, width=7, height=7):
    start = time.perf_counter()

    # TODO rename with BFS

    def find_start(maze, width=7, height=7):
        # print(maze)
        if maze is not None:
            for w in range(1, height + 1):
                for u in range(1, width + 1):
                    s = maze[w][u]
                    if s == 'S':
                        return w, u

    # for i in gui_maze:
    #     print(i)
    col, row = find_start(gui_maze)

    # col, row = 5, 1
    gui_maze[col][row] = "S"

    # Print Maze
    # for i in gui_maze:
    #     print(i)
    # print("-" * 35)

    def is_wall(cell_val, maze, node_col, node_row):
        wall = ["-", "|", "+"]
        # -------------- U move --------------
        if cell_val == "U":
            adj_cell = maze[node_col - 1][node_row]
            if adj_cell in wall:
                return True
            else:
                return False
        # -------------- R move --------------
        if cell_val == "R":
            adj_cell = maze[node_col][node_row + 1]
            if adj_cell in wall:
                return True
            else:
                return False
        # -------------- D move --------------
        if cell_val == "D":
            adj_cell = maze[node_col + 1][node_row]
            if adj_cell in wall:
                return True
            else:
                return False
        # -------------- L move --------------
        if cell_val == "L":
            adj_cell = maze[node_col][node_row - 1]
            if adj_cell in wall:
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
        for p in path:
            if p is not True:
                for s in p:
                    k = s[0]
                    j = s[1]
                    maze[k][j] = "#"
        return maze

    def check_paths(path, maze, node_col, node_row):
        # Start in node_Col and node_Row
        path += ""
        visited_nodes = []
        path = [char for char in path]
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
            if end_time - start > 100:
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
        # print(path_solution)
        a = path_solution[1][-1][0]
        b = path_solution[1][-1][1]
        # print(path_solution)
        viz_maze = visualize_path(gui_maze, path_solution)
        gui_maze[a][b] = "X"
        for i in gui_maze:
            # print(i)pass
            pass
    except TypeError:
        has_solution = False
        print("No solution, none")

    end = time.perf_counter()
    return (end - start).__round__(3), viz_maze, has_solution


# --------------------------------------------------------------------gui-----------------------------------------------------------------
def make_maze(wall_li, start, end, grid_width=7, grid_height=7):
    for i in range(len(wall_li)):
        if wall_li[i] is True:
            wall_li[i] = "+"
        elif wall_li[i] is False:
            wall_li[i] = " "
    wall_li[start] = "S"
    wall_li[end] = "X"

    for sy in range(grid_width):
        pass

    end_wall = ['|']
    for sy in range(grid_width):
        end_wall.append('-')
    end_wall.append('|')
    # outer for loop can hold the cols and inner holds rows
    maze1 = [end_wall]
    num = 0
    for a in range(grid_height):
        add_var = ['|']
        for v in range(num, grid_width + num):
            add_var.append(wall_li[v])
        add_var += '|'
        maze1.append(add_var)
        num += grid_width

    maze1.append(end_wall)
    # for node in maze1:
    #     print(node)
    return maze1


def gui_visualize_maze(maze5, grid):
    maze = make_maze_path_bool(maze5)
    # print(maze)
    for p in range(len(maze)):
        for j in range(1, 50):
            myobj = grid[j]
            if maze[p] == "#":
                myobj.change_color((255, 255, 0))


#                 TODO make obj classes  change colors with words and rgb

def make_maze_path_bool(maze, grid_width=7, grid_height=7):
    the_li = []
    # print(maze)
    for i in range(1, grid_height + 1):
        for j in range(1, grid_width + 1):
            if maze[i][j] == "#":
                the_li.append(True)
            else:
                the_li.append(False)
    # print(the_li)
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
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_path = False

    def draw(self):
        pygame.draw.rect(self.Win, self.color, (self.x, self.y, self.width, self.height))

    def do_toggle(self):
        if self.toggle:
            self.is_wall = False
            self.is_start = False
            self.is_end = False
            self.color = (0, 0, 0)
        elif not self.toggle:
            self.is_wall = True
            self.is_start = False
            self.is_end = False
            self.color = (255, 255, 255)

    def make_wall(self):
        self.is_end =False
        self.is_start = False
        self.is_wall = True
        self.color = (0, 0, 0)

    def change_color(self, color):
        self.color = color

    def hover(self, mouse):
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            return True
        else:
            return False

    def clear(self):
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.change_color((255, 255, 255))


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
        self.clickable = True

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

    def change_text_size(self, size):
        self.font_label = pygame.font.SysFont(self.font, int(size))

    def can_click(self, mouse, click):

        if not self.hover(mouse) and click[0]:
            self.clickable = False
            return False
        if not self.hover(mouse) and not click[0]:
            self.clickable = True
            return True


def main_gui():
    run = True
    # todo MAKE A COLOR DICT
    BLUE = (0, 0, 255)
    white = (255, 255, 255)
    grey = (175, 175, 175)
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("arial", 50)
    red = (255, 0, 0)
    white = (255, 255, 255)
    white2 = (235, 235, 235)
    color1 = white
    # Find path
    button1 = Button(Win, grey, 250, 5, 200, 25, "Find Path", text_color=(0, 0, 0))

    # Clear
    button2 = Button(Win, grey, 50 + 5 * 2 + 400, 5, 100, 25, "Clear", text_color=(0, 0, 0))
    clearb = Button(Win, grey, 50 + 5 * 2 + 400, 35, 100, 25, "Clear Path", text_color=(0, 0, 0))

    # Menu
    button3 = Button(Win, grey, 140, 5, 100, 25, "Menu", text_color=(0, 0, 0))
    border = CellBorder(Win, red, 100, 50, 100, 100)

    the_grid = []
    for y in range(7):
        for x in range(7):
            the_grid.append(Rectangle(Win, color1, ((x + 1) * 150 - 2 * (x - 10)) // 2,
                                      (((y + 1) * 100 - 2 * (y - 10) + 50 * y) // 2)+10, (140 - 2 * 2) // 2,
                                      (140 - 2 * 2) // 2))
            # highlight_box25 = Rectangle(Win, color1, 5 * 100 - 2 * 3, 4 * 100 + 50 - 2 * 3, 100 - 2 * 2, 100 - 2 * 2)

    len_grid =  len(the_grid)

    lost = False
    timer = 0
    button1_can_click = True
    button2_can_click = True
    delay = 12
    cursor_x = 0
    time_took = 0
    main_label = main_font.render(f"{time_took} Seconds", 1, (119, 209, 225))
    # TODO add depth label
    # todo add error on screen: no solution
    # todo add can click to the button class
    current_start = []
    current_end = []
    timer_click = 0

    def redraw_window():
        # Draw everything here if it happens during the game
        # for balloon in balloons:
        #     balloon.draw(Win)
        Win.fill((0, 0, 0))
        # Win.fill((21, 104, 207))
        button1.draw()
        button2.draw()
        button3.draw()
        clearb.draw()
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
        # for i in range(6):
        #     pygame.draw.rect(Win, grey, (v_x + v_line_dist * i, v_y, v_width, v_height - 8))
        #     x_grid_width = ((v_x + v_line_dist * i) - v_x)

        # h_height = v_width
        # h_width = x_grid_width
        # Draw horizontal lines
        # for i in range(6):
        #     pygame.draw.rect(Win, grey, (v_x, v_y + v_line_dist * i, h_width, h_height))

        # Need to put each square location into a class
        for box in the_grid:
            box.draw()

        if lost:
            quit()

        # todo blit text after rect in class method draw
        Win.blit(main_label, (0, Height - main_label.get_height()))
        button1.blit_text()
        button2.blit_text()
        button3.blit_text()
        clearb.blit_text()
        pygame.display.update()

    while run:
        # todo add hover state to grid cells?
        clock.tick(FPS)
        redraw_window()
        main_label = main_font.render(f"{time_took} Seconds", 1, (119, 209, 225))
        keys = pygame.key.get_pressed()
        cell = the_grid[cursor_x]
        # todo move the grid into a list
        #  then auto make objs for that class
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        # print(mouse)

        for jello in range(len_grid):
            myobj = the_grid[jello]
            if myobj.hover(mouse):
                cursor_x = jello
                pass

        # todo make a mouse class?

        if timer_click >= delay:
            for jello in range(len_grid):
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
        # if
        if button1.hover(mouse) and button1_can_click:
            if timer >= delay:

                button1.change_color((140, 140, 140))
                if button1.hover(mouse) and click[0] and button1_can_click:
                    time_took = 0
                    button1.change_text("Find Path")
                    button1.change_color((110, 110, 110))
                    maze = []
                    if len(current_start) == 1 and len(current_end) == 1:
                        for i in the_grid:
                            maze.append(i.is_wall)
                            if i.color == (255, 255, 0):
                                i.change_color((255, 255, 255))
                        new_maze = make_maze(maze, current_start[0], current_end[0])
                        time_took, got_maze, has_sol = find_path(new_maze)

                        time_took = time_took
                        redraw_window()
                        bool_maze = make_maze_path_bool(new_maze)
                        for wj in range(len(bool_maze)):
                            mi_obj = the_grid[wj]
                            if bool_maze[wj]:
                                mi_obj.change_color((255, 255, 0))
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

        if keys[pygame.K_e]:
            if timer >= delay:
                cell.is_wall = False
                if len(current_end) == 0:
                    cell.is_end = True
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
        # TOOO make a random wall generator
        if keys[pygame.K_LSHIFT] and keys[pygame.K_w]:
            import random
            if timer >= delay:
                for i in range(len_grid):
                    if random.random() < .2:
                        the_grid[i].make_wall()
                timer = 0
        if keys[pygame.K_w]:
            if timer >= delay:
                for i in range(len_grid):
                    if the_grid[i].is_wall:
                        the_grid[i].clear()

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

        if clearb.hover(mouse):
            clearb.color = (140, 140, 140)
        else:
            clearb.color = (175, 175, 175)
        clearb.can_click(mouse, click)
        if clearb.clickable:
            if True:

                if click[0]:
                    for i in the_grid:

                        if i.color == (255, 255, 0):
                            i.change_color((255, 255, 255))
                    timer_click = 0
        if not button2.hover(mouse) and click[0]:
            button2_can_click = False
        if not button2.hover(mouse) and not click[0]:
            button2_can_click = True

        if not button2.hover(mouse):
            button2.change_color((175, 175, 175))
        # 250, 5, 200, 25
        if button2.hover(mouse) and button2_can_click:
            button2.change_color((140, 140, 140))
            if button2.hover(mouse) and click[0] and button2_can_click:
                button2.change_text("Clear")
                button2.change_color((110, 110, 110))
                current_start.clear()
                current_end.clear()
                time_took = 0
                for jello in range(len_grid):
                    myobj = the_grid[jello]
                    myobj.clear()
        # TODO add clear to highlight class
        if keys[pygame.K_c]:
            current_start.clear()
            current_end.clear()
            time_took = 0
            for jello in range(len_grid):
                myobj = the_grid[jello]
                myobj.clear()

        if button3.hover(mouse):
            button3.color = (140, 140, 140)
        else:
            button3.color = (175, 175, 175)
        button3.can_click(mouse, click)
        if button3.clickable:
            if timer_click >= delay:

                if click[0]:
                    button3.color = (110, 110, 110)

                    main_menu()

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
    info_text_label2 = info_font.render(
        "Left click puts down walls, Right click clears the cell, and while hovering over a cell", 1, info_color)
    info_text_label3 = info_font.render("press the S and E keys to put down the Start and End nodes respectively.", 1,
                                        info_color)
    info_text_label4 = info_font.render("The C key clears the screen.", 1, info_color)

    bfs_b = Button(Win, (175, 175, 175), Width // 2 - 50 - 75, Height - 200, 100, 25, "BFS", font_size=20)
    dfs_b = Button(Win, (175, 175, 175), Width // 2 - 50 + 75, Height - 200, 100, 25, "DFS", font_size=20)

    run = True
    info = False
    timer = 0
    delay = 12

    def redraw_window():
        Win.fill((0, 0, 0))
        bfs_b.draw()
        dfs_b.draw()
        bfs_b.blit_text()
        dfs_b.blit_text()
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

    while run:
        clock.tick(FPS)
        redraw_window()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # print(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #
        dfs_b.can_click(mouse, click)
        if dfs_b.hover(mouse):
            dfs_b.color = (140, 140, 140)
        else:
            dfs_b.color = (175, 175, 175)
        #
        if dfs_b.clickable and click[0]:

            dfs_b.change_text_size(12)
            dfs_b.change_text("Coming Soon...")
            dfs_b.color = (255, 0, 0)
        else:
            dfs_b.change_text_size(20)
            dfs_b.change_text("DFS")

        bfs_b.can_click(mouse, click)
        if bfs_b.hover(mouse):
            bfs_b.color = (140, 140, 140)
        else:
            bfs_b.color = (175, 175, 175)

        if bfs_b.clickable and click[0]:
            if timer >= delay:
                bfs_b.color = (110, 110, 110)
                return main_gui()
            timer = 0



        if keys[pygame.K_SPACE]:
            # TODO Make a loading bar
            return main_gui()
        if keys[pygame.K_ESCAPE]:
            quit()
        if keys[pygame.K_i]:
            if timer >= delay:
                info = not info
            timer = 0
        # if keys[pygame.K_i]:
        #     if timer >= delay:
        #         info = False
        timer += 1
        # print(info)


maze = main_menu()
