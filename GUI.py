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


def fill_maze() -> None:
    config: dict[str] = config_read()
    # WSEN
    # 8421
    # 0000 = 0
    # 0001 = 1
    # 0010 = 2
    # 0011 = 3
    # 0100 = 4
    # 0101 = 5
    # 0110 = 6
    # 0111 = 7
    # 1000 = 8
    # 1001 = 9
    # 1010 = A
    # 1011 = B
    # 1100 = C
    # 1101 = D
    # 1110 = E
    # 1111 = F
    with open(config['output'], "r") as f:
        maze = []
        config['width']
        # print("  " + ("_" * config['width'] * 2))
        for line in f:
            for char in line:
                match char:
                    case "\n":
                        print(*maze)
                        maze = []
                    case "0":
                        maze.append("┼")
                    case "1":
                        maze.append("╷")
                    case "2":
                        maze.append("╴")
                    case "3":
                        maze.append("┐")
                    case "4":
                        maze.append("╵")
                    case "5":
                        maze.append("-")
                    case "6":
                        maze.append("┘")
                    case "7":
                        maze.append("┤")
                    case "8":
                        maze.append("╶")
                    case "9":
                        maze.append("┌")
                    case "A":
                        maze.append("|")
                    case "B":
                        maze.append("┬")
                    case "C":
                        maze.append("└")
                    case "D":
                        maze.append("├")
                    case "E":
                        maze.append("┴")
                    case "F":
                        maze.append(" ")



if __name__ == '__main__':
    draw_maze()
    fill_maze()
