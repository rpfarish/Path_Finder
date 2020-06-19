import time
import gui

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


maze = gui.main_menu()


def main(gui_maze):

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
        for p in path:
            if p is True:
                pass
            else:
                for s in p:
                    k = int(s[0])
                    j = int(s[1])
                    maze[k][j] = "#"

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

    path_solution = all_paths(gui_maze, col, row)
    try:
        a = path_solution[1][-1][0]
        b = path_solution[1][-1][1]

        visualize_path(gui_maze, path_solution)
        gui_maze[a][b] = "X"
        for i in gui_maze:
            print(i)
    except TypeError:
        print("No solution")

    end = time.perf_counter()
    print(end - start)


if __name__ == "__main__":
    main(maze)
