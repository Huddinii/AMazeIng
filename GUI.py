from termcolor import colored
from mazegen import MazeGenerator


class TColor:
    def __init__(self):
        self.colors = ['green', 'red', 'yellow', 'blue', 'white']
        self.i = 0

    def __call__(self) -> None:
        text = colored('┤', self.colors[self.i])
        print(text)
        self.i += 1


t_color = TColor()


def player_interaction() -> None:
    # need actual functions to do the stuff instread of just print
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze color")
    print("4. Quit")
    input_str: str = input("type number 1-4: ")
    match input_str:
        case "1":
            draw_maze()
            fill_maze()
        case "2":
            print("Show/Hide path from entry to exit")
        case "3":
            t_color()
        case "4":
            exit(0)


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


def get_reset() -> str:
    return "\033[0m"


def top(n=1):
    return f"\033[53m{' ' * n}{get_reset()}"


def bottom(n=1):
    return f"\033[4m{' ' * n}{get_reset()}"


def top_bottom(n=1):
    return f"\033[53m\033[4m{' ' * n}{get_reset()}"


def fill_maze() -> None:
    config: dict[str] = config_read()
    with open(config['output'], "r") as f:
        maze = []
        print()
        # over_under = "\033[53m\033[4m \033[0m"
        # under = "\033[4m \033[0m"
        # over = "\033[53m "
        for line in f:
            if line.startswith("\n"):
                break
            for char in line:
                match char:
                    case "\n":
                        print(*maze, sep='')
                        maze = []
                    case "0":
                        maze.append("   ")
                    case "1":
                        maze.append(top(3))
                    case "2":
                        maze.append("  |")
                    case "3":
                        maze.append(top(2) + "|")
                    case "4":
                        maze.append(bottom(3))
                    case "5":
                        maze.append(top_bottom(3))
                    case "6":
                        maze.append(bottom(2) + "|")
                    case "7":
                        maze.append(top_bottom(2) + "|")
                    case "8":
                        maze.append("|  ")
                    case "9":
                        maze.append("|" + top(2))
                    case "A":
                        maze.append("| |")
                    case "B":
                        maze.append("|" + top(1) + "|")
                    case "C":
                        maze.append("|" + bottom(2))
                    case "D":
                        maze.append("|" + top_bottom(2))
                    case "E":
                        maze.append("|" + bottom(1) + "|")
                    case "F":
                        maze.append("███")


if __name__ == '__main__':
    draw_maze()
    fill_maze()
