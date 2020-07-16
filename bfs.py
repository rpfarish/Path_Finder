from timeit import timeit
# Returns list of adjacent nodes

def adjacent_nodes(n, grid_size=3):
    adj = []
    n0 = n[0]
    n1 = n[1]
    if 0 < n0:
        adj.append((n0 - 1, n1))
    if n0 < grid_size:
        adj.append((n0 + 1, n1))
    if 0 < n1:
        adj.append((n0, n1 - 1))
    if n1 < grid_size:
        adj.append((n0, n1 + 1))

    return {n: adj}


# BFS Search needs the starting node S and an adjacent node list
def bfs(s, adj):
    """Define a nodes location as a tuple e.g. (3,4) and (2,4),
        and a node is adjacent if it can be reached by moving either x or y by |1| away (1 or -1).
    """

    # The start node starts with a depth of 0 and its parent is None (Store the info in a Dict (Both the level and the parent))
    level = {s: 0}
    parent = {s: None}

    # Then set the level (i) to 1
    i = 1
    # On level 0 the current level nodes list only contains s (the start node)
    current_level_nodes = [s]

    # Then search the the current level nodes list
    # while current level nodes is not empty
    while current_level_nodes:
        next_level = []
        # Then to start the search, loop through all the current level nodes list
        for u in current_level_nodes:
            # and for every adjacent node
            ad = adjacent_nodes(u, 500)
            for v in ad[u]:
                #   check if the node has already been visited by looking for it in the level dict at the level (i)
                if v not in level:
                    #   if it has not already been visited then put the current adjacent node in the level dict at the level (i)
                    level[v] = i
                    #   also put the adjacent node as a child in the current node in the parent dict
                    parent[v] = u
                    #   put the adjacent in to a next level list
                    next_level.append(v)

        # At the end of iterating through current level nodes
        # set current level nodes equal to next
        current_level_nodes = next_level

        # then increment the level (i)
        i += 1
    return level, parent

    # The graph is defined by the adjacency list and maybe making a func to determine adjacent neighbors


# Adjacency list
adj = {(5, 5): [(4, 5), (6, 5), (5, 4), (5, 6)],
       (4, 5): [(5, 5)],
       (6, 5): [(5, 5)],
       (5, 4): [(5, 5)],
       (5, 6): [(5, 5)],
       (5, 6): [(5, 7)],
       (5, 7): [(5, 6)],

       }

# Iterate through the list for the key (5, 5)
# for i in adj[(5, 5)]:
#     print(i)

# print(adjacent_nodes((1, 1)))
import time
start = time.perf_counter()
level, parent = bfs((1, 1), adj)
end = time.perf_counter()
# print('level', level)
# print('parent', parent)
print('took', end-start, '# of seconds')