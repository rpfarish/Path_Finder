import pygame
import random
import os


pygame.font.init()
icon = pygame.image.load(os.path.join("assets", "pathfinder.png"))
pygame.display.set_icon(icon)

# Window
Width, Height = 700, 650
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Path Finder v1.0")





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


def main():
    run = True

    text_maze = open("maze.txt", "r+")

    BLUE = (0, 0, 255)
    white = (255, 255, 255)
    grey = (175, 175, 175)
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    red = (255, 0, 0)
    white = (255, 255, 255)
    white2 = (235, 235, 235)
    color1 = white2
    button1 = Button(Win, grey, 250, 5, 200, 25, "Find Path", text_color=(0, 0, 0))
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
    delay = 12
    cursor_x = 1
    main_label = main_font.render(f"{cursor_x}", 1, (119, 209, 225))
    current_start = []
    current_end = []

    def redraw_window():
        # Draw everything here if it happens during the game
        # for balloon in balloons:
        #     balloon.draw(Win)
        Win.fill((0, 0, 0))
        # Win.fill((21, 104, 207))
        button1.draw()
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

        border.draw()

        if lost:
            quit()

        Win.blit(main_label, (0, 0))
        button1.blit_text()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        main_label = main_font.render(f"{cursor_x}", 1, (119, 209, 225))
        keys = pygame.key.get_pressed()
        cell = the_grid[cursor_x]
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        # print(mouse)

        if cell.color == (0, 0, 0):
            cell.is_wall = True
        # print(cell.color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not button1.hover(mouse) and click[0]:
            button1_can_click = False
        if not button1.hover(mouse) and not click[0]:
            button1_can_click = True

        # 250, 5, 200, 25
        if button1.hover(mouse) and button1_can_click:

            button1.change_color((140, 140, 140))
            if button1.hover(mouse) and click[0] and button1_can_click:
                button1.change_text("Find Path")
                button1.change_color((140, 0, 0))
                maze = []
                if len(current_start) == 1 and len(current_end) == 1:
                    for i in the_grid:
                        maze.append(the_grid[i].is_wall)
                    # new_maze = make_maze(maze, current_start[0], current_end[0])
                    text_maze.write(str(maze))
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

        # print("\n" * 3)

        timer += 1


def main_menu():
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 60)
    info_font = pygame.font.SysFont("sans", 15)
    main_label = main_font.render("Pathfinder v1", 1, (119, 209, 225))
    info_color = (255, 255, 225)
    # info_color = (119, 209, 225)
    info_label = info_font.render("Press i for info or Space to continue.", 1, info_color)
    info_text_label = info_font.render("Generally the BFS Algorithm runs better the fewer walls there", 1, info_color)
    info_text_label2 = info_font.render("are and the space time complexity exponentially increases", 1, info_color)
    info_text_label3 = info_font.render("the farther apart the start and end nodes are.", 1, info_color)

    run = True
    info = False
    def redraw_window():
        Win.fill((0, 0, 0))
        Win.blit(main_label, (Width // 2 - main_label.get_width() // 2, Height // 2 - main_label.get_height() // 2))
        Win.blit(info_label, (Width // 2 - info_label.get_width() // 2, Height // 2 - info_label.get_height() // 2+50))
        if info:
            Win.blit(info_text_label, (Width // 2 - info_text_label.get_width() // 2, Height // 2 - info_text_label.get_height() // 2 + 100))
            Win.blit(info_text_label2, (Width // 2 - info_text_label2.get_width() // 2, Height // 2 - info_text_label2.get_height() // 2 + 150))
            Win.blit(info_text_label3, (Width // 2 - info_text_label3.get_width() // 2, Height // 2 - info_text_label3.get_height() // 2 + 200))
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
             return main()
        if keys[pygame.K_ESCAPE]:
            quit()
        if keys[pygame.K_i]:
            info = True

if __name__ == '__main__':
    main()
