import heapq
from config import LINHAS, COLUNAS, DIRECOES, CUSTO_MOVIMENTO, E_MAX, bateria


# =============================
# HEURÍSTICA
# =============================


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# =============================
# VIZINHOS
# =============================


def neighbors(grid, n):

    x, y = n
    result = []

    for dx, dy in DIRECOES:

        nx = x + dx
        ny = y + dy

        if 0 <= nx < LINHAS and 0 <= ny < COLUNAS:

            if grid[nx][ny] != 1:
                result.append((nx, ny))

    return result


# =============================
# CUSTO
# =============================


def custo(grid, x, y):

    if grid[x][y] == 2:
        return CUSTO_MOVIMENTO * 0.5
    elif grid[x][y] == 3:
        return CUSTO_MOVIMENTO * 1.5
    else:
        return CUSTO_MOVIMENTO


# =============================
# A*
# =============================


def astar(grid, start, goal):

    open_list = []
    heapq.heappush(open_list, (0, start))

    came = {}
    g = {start: 0}

    closed = set()

    while open_list:

        _, current = heapq.heappop(open_list)

        if current in closed:
            continue

        closed.add(current)

        if current == goal:

            path = []

            while current in came:
                path.append(current)
                current = came[current]

            path.append(start)
            path.reverse()

            return path

        for n in neighbors(grid, current):

            tentative = g[current] + custo(grid, n[0], n[1])

            if tentative > bateria:
                continue

            if n not in g or tentative < g[n]:

                g[n] = tentative
                f = tentative + heuristic(n, goal)

                heapq.heappush(open_list, (f, n))
                came[n] = current

    return None


# =============================
# IDA*
# =============================


def ida_star(grid, start, goal):

    bound = heuristic(start, goal)
    path = [start]

    def search(path, g, bound):

        node = path[-1]

        if g > E_MAX:
            return float("inf")

        f = g + heuristic(node, goal)

        if f > bound:
            return f

        if node == goal:
            return path.copy()

        minimum = float("inf")

        for n in neighbors(grid, node):

            if n in path:
                continue

            path.append(n)

            t = search(path, g + 1, bound)

            if isinstance(t, list):
                return t

            if t < minimum:
                minimum = t

            path.pop()

        return minimum

    while True:

        t = search(path, 0, bound)

        if isinstance(t, list):
            return t

        if t == float("inf"):
            return None

        bound = t


# =============================
# RBFS
# =============================


def rbfs(grid, node, goal, g, bound, path):

    f = g + heuristic(node, goal)

    if f > bound:
        return None, f

    if node == goal:
        return path, f

    successors = []

    for n in neighbors(grid, node):

        if n in path:
            continue

        if g + 1 > E_MAX:
            continue

        successors.append((n, g + 1 + heuristic(n, goal)))

    if not successors:
        return None, float("inf")

    while True:

        successors.sort(key=lambda x: x[1])

        best, best_f = successors[0]

        if best_f > bound:
            return None, best_f

        alt = successors[1][1] if len(successors) > 1 else float("inf")
        result, new_f = rbfs(grid, best, goal, g + 1, min(bound, alt), path + [best])

        successors[0] = (best, new_f)

        if result:
            return result, new_f


def run_rbfs(grid, start, goal):

    path, _ = rbfs(grid, start, goal, 0, float("inf"), [start])
    return path
