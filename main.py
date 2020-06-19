
maze1 = [['|', '-', '-', '-', '-', '-', '|'],
         ['|', ' ', ' ', ' ', '+', ' ', '|'],
         ['|', ' ', ' ', ' ', '+', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', '+', '+', '+', ' ', '|'],
         ['|', ' ', ' ', ' ', ' ', 'X', '|'],
         ['|', '-', '-', '-', '-', '-', '|']]

# Start Node
col = 1
row = 1
maze1[col][row] = "S"

# Print Maze
for i in maze1:
    print(i)
print("-" * 35)


def is_wall(cell_val, maze, node_col, node_row):
    if cell_val == "U":
        adj_cell = maze[node_col - 1][node_row]
        if adj_cell == "-" or adj_cell == "|" or adj_cell == "+":
            return True
        else:
            return False

    if cell_val == "R":
        adj_cell = maze[node_col][node_row + 1]
        if adj_cell == "-" or adj_cell == "|" or adj_cell == "+":
            return True
        else:
            return False

    if cell_val == "D":
        adj_cell = maze[node_col + 1][node_row]
        if adj_cell == "-" or adj_cell == "|" or adj_cell == "+":
            return True
        else:
            return False

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
    # Start in Col and Row
    path += ""
    visited_nodes = []
    path = [char for char in path]
    # this is a list of what the path was to the end node

    for j in range(len(path)):

        nd = path[j]

        if nd == "U":
            val = maze[node_col - 1][node_row]
            node_col -= 1
            visited_nodes.append([node_col, node_row])
            if val == "X":
                if visited_nodes is not None:
                    return True, visited_nodes
                else:
                    return True

        if nd == "R":
            val = maze[node_col][node_row + 1]
            node_row += 1
            visited_nodes.append([node_col, node_row])
            if val == "X":
                if visited_nodes is not None:
                    return True, visited_nodes
                else:
                    return True
        if nd == "D":
            val = maze[node_col + 1][node_row]
            node_col += 1
            visited_nodes.append([node_col, node_row])
            if val == "X":
                if visited_nodes is not None:
                    return True, visited_nodes
                else:
                    return True
        if nd == "L":
            val = maze[node_col][node_row - 1]
            node_row -= 1
            visited_nodes.append([node_col, node_row])
            if val == "X":
                if visited_nodes is not None:
                    return True, visited_nodes
                else:
                    return True


def all_paths(maze, node_col, node_row):
    """the maze param is only needed to pass to the valid move func"""
    queue = [""]
    found = False
    while not found:
        # deque
        e = queue[0]
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


path_solution = all_paths(maze1, col, row)

a = path_solution[1][-1][0]
b = path_solution[1][-1][1]

visualize_path(maze1, path_solution)
maze1[a][b] = "X"
for i in maze1:
    print(i)