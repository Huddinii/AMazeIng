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
    input_str: str = input("type number 1-4: ")
    match input_str:
        case "1":
            print("Re-generate a new maze")
        case "2":
            print("Show/Hide path from entry to exit")
        case "3":
            print("Rotate maze color")
            t_color()
        case "4":
            print("Quit")
            exit(0)


def config_read() -> dict[str]:
    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key.lower().strip()] = value.strip()

    return config


def draw_maze() -> None:
    config: dict[str] = config_read()
    start: tuple = config['entry'].split(',', 1)
    exit: tuple = config['exit'].split(',', 1)

    try:
        width = int(config['width'])
        height = int(config['height'])
        start = tuple(int(x) for x in start)
        exit = tuple(int(x) for x in exit)
        perfect = bool(config['perfect'])
        algo = config.get('algorithm', None)
        seed = int(config.get('seed', None))
    except TypeError as e:
        print(e)

    mazegen = MazeGenerator(height, width, start, exit, perfect, algo)
    if seed is not None:
        mazegen.set_seed(seed)
    mazegen.generate_maze()
    mazegen.out("output.txt")


if __name__ == '__main__':
    draw_maze()
