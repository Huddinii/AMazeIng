from configparser import ConfigParser
from termcolor import colored


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


def config_read() -> None:
    config = ConfigParser()
    config.read("config.txt")


def draw_maze(maze_parts: list[str]) -> None:
    pass
