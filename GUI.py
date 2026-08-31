from termcolor import colored
from mazegen import MazeGenerator
from typing import IO


class TColor:
    def __init__(self):
        self.colors = ['white', 'green', 'red', 'yellow', 'blue']
        self.i = 0
        self.calls = 0

    def __call__(self, maze: str) -> str:
        if self.calls == 0:
            return colored(maze, 'white')
        return colored(maze, self.colors[self.i])

    def next_call(self) -> None:
        self.calls += 1
        self.i += 1
        if self.i == len(self.colors):
            self.i = 0


def clear_screen() -> None:
    print("\033[2J\033[H", end="", flush=True)


def player_interaction() -> None:
    # need actual functions to do the stuff instread of just print
    # config: dict[str] = config_read()
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
                draw_maze()
                fill_maze(t_color)
            case "2":
                clear_screen()
                print("Show/Hide path from entry to exit")
            case "3":
                clear_screen()
                fill_maze(t_color)
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


def draw_maze() -> None:
    config: dict[str] = config_read()

    mazegen = MazeGenerator(config['height'], config['width'], config['start'],
                            config['exit'], config['perfect'], config['algo'])

    if config['seed'] is not None:
        mazegen.set_seed(config['seed'])

    try:
        mazegen.generate_maze()
    except RuntimeError as e:
        print(e)
    else:
        mazegen.out(config['output'])


def top(n: int = 1):
    return f"\033[53m{' ' * n}\033[55m"


def bottom(n: int = 1):
    return f"\033[4m{' ' * n}\033[24m"


def top_bottom(n: int = 1):
    return f"\033[53m\033[4m{' ' * n}\033[55m\033[24m"


def fill_maze(t_color: TColor) -> None:
    config: dict[str] = config_read()
    with open(config['output'], "r") as f:
        maze: list[str] = []
        for line in f:
            if line.startswith("\n"):
                break
            for char in line:
                match char:
                    case "\n":
                        print(t_color("".join(maze)))
                        maze = []
                    case "0":
                        maze.append(t_color("   "))
                    case "1":
                        maze.append(t_color(top(3)))
                    case "2":
                        maze.append(t_color("  |"))
                    case "3":
                        maze.append(t_color(top(2) + "|"))
                    case "4":
                        maze.append(t_color(bottom(3)))
                    case "5":
                        maze.append(t_color(top_bottom(3)))
                    case "6":
                        maze.append(t_color(bottom(2) + "|"))
                    case "7":
                        maze.append(t_color(top_bottom(2) + "|"))
                    case "8":
                        maze.append(t_color("|  "))
                    case "9":
                        maze.append(t_color("|" + top(2)))
                    case "A":
                        maze.append(t_color("| |"))
                    case "B":
                        maze.append(t_color("|" + top(1) + "|"))
                    case "C":
                        maze.append(t_color("|" + bottom(2)))
                    case "D":
                        maze.append(t_color("|" + top_bottom(2)))
                    case "E":
                        maze.append(t_color("|" + bottom(1) + "|"))
                    case "F":
                        maze.append(colored("\033[36m███"))

        t_color.next_call()
        start_end_coord(f, config['height'])


def start_end_coord(f: IO, maze_height: int) -> dict[str, tuple]:
    lines: list[str] = []
    start: tuple = None
    end: tuple = None
    for line in f:
        lines.append(line.strip())

    for i in range(len(lines) - 1):
        line = lines[i]
        nextline = lines[i + 1]

        if ',' in line and ',' in nextline:
            y_str, x_str = line.split(',', 1)
            start = (int(y_str.strip()), int(x_str.strip()))
            print_char(start[0], start[1], colored('█', 'red'))

        elif ',' in line and ',' not in nextline:
            y_str, x_str = line.split(',', 1)
            end = (int(y_str.strip()), int(x_str.strip()))
            print_char(end[0], end[1], colored('█', 'red'))

    print(f"\033[{maze_height+1};0H", end="", flush=True)
    ret = {'start': start, 'end': end}
    return ret


def print_char(y: int, x: int, char: str) -> None:
    # config: dict[str] = config_read()
    # if y < config['height'] and x < config['width']:
    print(f"\033[{y+1};{(x*3)+2}H{char}", end="", flush=True)


def draw_path() -> None:
    config: dict[str] = config_read()
    path = ''
    solve = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (3, 0),
        "W": (-3, 0),
    }
    with open(config['output'], "r") as f:
        coords = start_end_coord(f, config['height'])
        start = coords['start']
        print(start)
        f.seek(0)
        for line in f:
            line = line.strip()
            if line and set(line) <= {'N', 'S', 'E', 'W'}:
                path = line
        print(path)


# if __name__ == '__main__':
#     draw_path()
