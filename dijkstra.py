def adjacent_nodes(n, wall, grid_size):
    """
    :param n: node coordinate
    :param wall: list of walls
    :param grid_size: a tuple eg (3, 2)
    """

    if n in wall:
        return []
    adj = []
    n0, n1 = n[0], n[1]
    if 0 < n0 and (n0 - 1, n1) not in wall:
        adj.append((n0 - 1, n1))  # LEFT
    if n0 < grid_size[0] and (n0 + 1, n1) not in wall:
        adj.append((n0 + 1, n1))  # RIGHT
    if 0 < n1 and (n0, n1 - 1) not in wall:
        adj.append((n0, n1 - 1))  # UP
    if n1 < grid_size[1] and (n0, n1 + 1) not in wall:
        adj.append((n0, n1 + 1))  # DOWN

    return adj


def min_of_grid_in_check_node(grid, wall, check_node):
    seq = {x: grid[x] for x in check_node}
    x = float("inf")
    a, b = None, None
    for key, val in seq.items():
        if val < x:
            x = val
            a = key
            b = val
    return a, b


def dijkstra(start, wall, grid_size):
    grid = {}
    check_node = []
    prev = {start: None}
    weight = {}
    for x in range(grid_size[0] + 1):
        for y in range(grid_size[1] + 1):
            grid[(x, y)] = float("inf")

            if (x, y) not in wall:
                check_node.append((x, y))
            weight[(x, y)] = 1
    grid[start] = 0
    print(grid)
    print()
    print(check_node)

    while check_node:
        curr, curr_dist = min_of_grid_in_check_node(grid, wall, check_node)  # curr needs to be a key val from grid

        check_node.remove(curr)
        # print(adjacent_nodes(curr, wall, grid_size))
        for adj in adjacent_nodes(curr, wall, grid_size):
            pot_dist = curr_dist + 1
            if pot_dist < grid[adj]:
                grid[adj] = pot_dist
                prev[adj] = curr
    return grid, prev


start, end = (0, 0), (2, 2)
grid, parent_dict = dijkstra(start, [(1, 0)], (2, 2))
print(grid)
print(parent_dict)

