from configparser import ConfigParser


def player_interaction() -> None:
    # need actual functions to do the stuff instread of just print, only placeholder
    input_str: str = input("type number 1-4: ")
    match input_str:
        case "1":
            print("Re-generate a new maze")
        case "2":
            print("Show/Hide path from entry to exit")
        case "3":
            print("Rotate maze color")
        case "4":
            print("Quit")
            exit(0)


def config_read() -> None:
    config = ConfigParser()
    config.read("config.txt")
