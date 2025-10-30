import random
import sys

def generate_maze(height: int, width: int) -> list[list[str]]:
    # Ensure odd dimensions for walls and passages
    if height % 2 == 0:
        height += 1
    if width % 2 == 0:
        width += 1

    # Initialize grid with walls
    maze = [['#' for _ in range(width)] for _ in range(height)]

    # Starting position (must be odd)
    start_y, start_x = 1, 1
    maze[start_y][start_x] = '.'

    # Directions (N, S, E, W)
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    def dfs(y: int, x: int) -> None:
        random.shuffle(directions)
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 1 <= ny < height - 1 and 1 <= nx < width - 1 and maze[ny][nx] == '#':
                maze[ny - dy // 2][nx - dx // 2] = '.'
                maze[ny][nx] = '.'
                dfs(ny, nx)

    dfs(start_y, start_x)

    # Place S and T in random empty cells
    empty_cells = [(y, x) for y in range(1, height-1) for x in range(1, width-1) if maze[y][x] == '.']
    s_y, s_x = random.choice(empty_cells)
    t_y, t_x = random.choice(empty_cells)
    while (t_y, t_x) == (s_y, s_x):
        t_y, t_x = random.choice(empty_cells)

    maze[s_y][s_x] = 'S'
    maze[t_y][t_x] = 'T'

    return maze


def print_maze(maze: list[list[str]]) -> None:
    for row in maze:
        print(''.join(row))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python maze_generator.py <height> <width>")
        sys.exit(1)

    height = int(sys.argv[1])
    width = int(sys.argv[2])

    maze = generate_maze(height, width)
    print_maze(maze)
