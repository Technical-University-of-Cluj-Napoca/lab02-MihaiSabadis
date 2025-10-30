import sys
sys.setrecursionlimit(10000)    # increase recursion limit if needed

def read_maze(filename: str) -> list[list[str]]:
    """Reads a maze from a file and returns it as a list of lists (i.e. a matrix).

    Args:
        filename (str): The name of the file containing the maze.
    Returns:
        list: A 2D list (matrix) representing the maze.
    """
    with open(filename, 'r') as file:
        maze = [list(line.rstrip("\n")) for line in file if line.strip()]

    return maze



def find_start_and_target(maze: list[list[str]]) -> tuple[int, int]:
    """Finds the coordinates of start ('S') and target ('T') in the maze, i.e. the row and the column
    where they appear.

    Args:
        maze (list[list[str]): A 2D list (matrix) representing the maze.
    Returns:
        tuple[int, int]: A tuple containing the coordinates of the start and target positions.
        Each position is represented as a tuple (row, column).
    """
    start = None
    target = None
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'T':
                target = (r, c)
    if start is None or target is None:
        raise ValueError("Maze must contain both 'S' (start) and 'T' (target) positions.")
    return start, target



def get_neighbors(maze, position):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    y, x = position
    neighbors = []
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[ny]) and maze[ny][nx] != '#':
            neighbors.append((ny, nx))
    return neighbors




def bfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    """Performs a breadth-first search (BFS) to find the shortest path from start to target in the maze.

    Args:
        maze (list[list[str]]): A 2D list of lists (matrix) representing the maze.
        start (tuple[int, int]): The starting position in the maze as (row, column).
        target (tuple[int, int]): The target position in the maze as (row, column).
    Returns:
        list[tuple[int, int]]: A list of positions representing the shortest path from start to target,
        including both start and target. If no path exists, returns an empty list.
    """
    # from collections you can import deque for using a queue.
    from collections import deque

    queue = deque([(start)])
    visited = set()
    parent = {start: None}
    visited.add(start)
    while queue:
        current = queue.popleft()
        if current == target:
            # reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # reverse the path
        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    return [] # no path found



def dfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    """Performs a depth-first search (DFS) to find *a* path from start to target in the maze.

    Args:
        maze (list[list[str]]): A 2D list of lists (matrix) representing the maze.
        start (tuple[int, int]): The starting position in the maze as (row, column).
        target (tuple[int, int]): The target position in the maze as (row, column).
    Returns:
        list[tuple[int, int]]: A list of positions representing the path from start to target,
        including both start and target. If no path exists, returns an empty list.
    """
    stack = [start]
    visited = set([start])
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == target:
            # reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return []  # no path found


def print_maze_with_path(maze: list[list[str]], path: list[tuple[int, int]]) -> None:
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    # copy
    maze_with_path = [row[:] for row in maze]

    for y, x in path:
        if maze_with_path[y][x] == 'S':
            continue
        if maze_with_path[y][x] == 'T':
            continue
        maze_with_path[y][x] = f"{RED}*{RESET}"

    for r in range(len(maze_with_path)):
        row_out = []
        for c in range(len(maze_with_path[r])):
            ch = maze_with_path[r][c]
            if ch == 'S':
                row_out.append(f"{YELLOW}S{RESET}")
            elif ch == 'T':
                row_out.append(f"{GREEN}T{RESET}")
            else:
                row_out.append(ch)
        print("".join(row_out))
    print()



if __name__ == "__main__":
    # Example usage: py maze_search.py dfs/bfs maze.txt
    if len(sys.argv) != 3 or sys.argv[1] not in ('dfs', 'bfs'):
        print("Usage: python maze_search.py <dfs/bfs> <maze_file>")
        sys.exit(1)
    algorithm = sys.argv[1]
    maze_file = sys.argv[2]
    maze = read_maze(maze_file)
    start, target = find_start_and_target(maze)
    if algorithm == 'bfs':
        path = bfs(maze, start, target)
    else:
        path = dfs(maze, start, target)
    
    if not path:
        print("No path found from 'S' to 'T'.")
        sys.exit(1)

    print_maze_with_path(maze, path)
