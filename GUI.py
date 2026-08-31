from termcolor import colored
from mazegen import MazeGenerator
from typing import IO


class TColor:
    def __init__(self):
        self.colors = ['white', 'green', 'red', 'yellow', 'blue']
        self.i = 0
        self.calls = 0

    def __call__(self, maze: str, on_str: str = 'on_grey') -> str:
        if self.calls == 0:
            return colored(maze, 'white', on_str)
        return colored(maze, self.colors[self.i], on_color=on_str)

    def next_call(self) -> None:
        self.calls += 1
        self.i += 1
        if self.i == len(self.colors):
            self.i = 0


def clear_screen() -> None:
    print("\033[2J\033[H", end="", flush=True)


def player_interaction() -> None:
    # need actual functions to do the stuff instread of just print
    config: dict[str] = config_read()
    try:
        mazegen = MazeGenerator(config['height'], config['width'],
                                config['start'], config['exit'],
                                config['perfect'], config['algo'])
        if config['seed'] is not None:
            mazegen.set_seed(config['seed'])
        mazegen.generate_maze()
    except RuntimeError as e:
        print("Error:", e)
        exit(0)
    else:
        mazegen.out(config['output'])

    maze: list[list[str]] = [[' ' for _ in range(config['width'])]
                             for _ in range(config['height'])]
    t_color = TColor()
    while 1:
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze color")
        print("4. Quit")
        input_str: str = input("type number 1-4: ")
        match input_str:
            case "1":
                clear_screen()
                fill_maze(config, maze)
                draw_maze(maze, t_color)
            case "2":
                clear_screen()
                draw_path(config, maze)
                draw_maze(maze, t_color)
            case "3":
                clear_screen()
                t_color.next_call()
                fill_maze(config, maze)
                draw_maze(maze, t_color)
            case "4":
                break


def config_read() -> dict[str]:
    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key.lower().strip()] = value.strip()

    start: tuple = config['entry'].split(',', 1)
    exit: tuple = config['exit'].split(',', 1)

    try:
        config.update({'width': int(config['width'])})
        config.update({'height': int(config['height'])})
        config.update({'start': tuple(int(x) for x in start)})
        config.update({'exit': tuple(int(x) for x in exit)})
        config.update({'perfect': bool(config['perfect'])})
        config.update({'algo': config.get('algorithm', None)})
        config.update({'seed': int(config.get('seed', None))})
        config.update({'output': config['output_file']})
    except TypeError as e:
        print(e)

    return config


def draw_maze(maze: list[list], t_color: TColor) -> None:
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            print(t_color(maze[x][y][0], maze[x][y][1]), end='')
        print()


def top(n: int = 1):
    return f"\033[53m{' ' * n}\033[55m"


def bottom(n: int = 1):
    return f"\033[4m{' ' * n}\033[24m"


def top_bottom(n: int = 1):
    return f"\033[53m\033[4m{' ' * n}\033[55m\033[24m"


def fill_maze(config: dict, maze: list[list]) -> None:
    x, y = 0, 0
    with open(config['output'], "r") as f:
        for line in f:
            if line.startswith("\n"):
                break
            for char in line:
                match char:
                    case "\n":
                        x += 1
                        y = 0
                    case "0":
                        maze[x][y] = ("   ", 'on_black', 'on_black')
                        y += 1
                    case "1":
                        maze[x][y] = (top(3), 'on_black')
                        y += 1
                    case "2":
                        maze[x][y] = ("  |", 'on_black')
                        y += 1
                    case "3":
                        maze[x][y] = (top(2) + "|", 'on_black')
                        y += 1
                    case "4":
                        maze[x][y] = (bottom(3), 'on_black')
                        y += 1
                    case "5":
                        maze[x][y] = (top_bottom(3), 'on_black')
                        y += 1
                    case "6":
                        maze[x][y] = (bottom(2) + "|", 'on_black')
                        y += 1
                    case "7":
                        maze[x][y] = (top_bottom(2) + "|", 'on_black')
                        y += 1
                    case "8":
                        maze[x][y] = ("|  ", 'on_black')
                        y += 1
                    case "9":
                        maze[x][y] = ("|" + top(2), 'on_black')
                        y += 1
                    case "A":
                        maze[x][y] = ("| |", 'on_black')
                        y += 1
                    case "B":
                        maze[x][y] = ("|" + top(1) + "|", 'on_black')
                        y += 1
                    case "C":
                        maze[x][y] = ("|" + bottom(2), 'on_black')
                        y += 1
                    case "D":
                        maze[x][y] = ("|" + top_bottom(2), 'on_black')
                        y += 1
                    case "E":
                        maze[x][y] = ("|" + bottom(1) + "|", 'on_black')
                        y += 1
                    case "F":
                        maze[x][y] = ("\033[36m███", 'on_black')
                        y += 1

        start_end_coord(maze, f, config['height'])


def start_end_coord(maze: list[list], f: IO, maze_height: int) -> None:
    lines: list[str] = []
    for line in f:
        lines.append(line.strip())

    for i in range(len(lines) - 1):
        line = lines[i]
        nextline = lines[i + 1]

        if ',' in line and ',' in nextline:
            y_str, x_str = line.split(',', 1)
            x, y = int(y_str.strip()), int(x_str.strip())
            maze[x][y] = (maze[x][y][0], 'on_green')

        elif ',' in line and ',' not in nextline:
            y_str, x_str = line.split(',', 1)
            x, y = int(y_str.strip()), int(x_str.strip())
            print(maze[x][y])
            maze[x][y] = (maze[x][y][0], 'on_green')
            print(maze[x][y])


def draw_path(config: dict, maze: list[list]) -> None:
    path: str = []

    with open(config['output'], "r") as f:
        x, y = config['start']
        f.seek(0)
        for line in f:
            line = line.strip()
            if line and set(line) <= {'N', 'S', 'E', 'W'}:
                path = line
        for char in path:
            match char:
                case "N":
                    x -= 1
                    maze[x][y] = (maze[x][y][0], 'on_magenta')
                case "S":
                    x += 1
                    maze[x][y] = (maze[x][y][0], 'on_magenta')
                case "E":
                    y += 1
                    maze[x][y] = (maze[x][y][0], 'on_magenta')
                case "W":
                    y -= 1
                    maze[x][y] = (maze[x][y][0], 'on_magenta')


# if __name__ == '__main__':
#     draw_path()
