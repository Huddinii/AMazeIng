from enum import Enum


class Wall(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Cell:
    def __init__(self, x: int, y: int):
        self.walls = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        self.position = (x, y)
        self.checked = False
        self.logo = False


class Maze:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.cells = [[Cell(x, y) for x in range(height)]for y in range(width)]

    def create_logo(self):
        if self.height > 9 and self.width > 9:
            middle = (int(self.height / 2), int(self.width / 2))
            print(middle)
            start = (middle[0] - 2, middle[1] - 3)
            print(start)
            y = start[1]
            for x in range(start[0], start[0] + 5):
                if (x != middle[0]):
                    self.cells[x][y].logo = True
                else:
                    for y in range(start[1], start[1] + 3):
                        self.cells[x][y].logo = True
            start = (middle[0] - 2, middle[1] + 1)
            print(start)
            for x in range(start[0], start[0] + 5):
                for y in range(start[1], start[1] + 3):
                    self.cells[x][y].logo = True
            self.cells[middle[0] - 1][middle[1] + 1].logo = False
            self.cells[middle[0] - 1][middle[1] + 2].logo = False
            self.cells[middle[0] + 1][middle[1] + 2].logo = False
            self.cells[middle[0] + 1][middle[1] + 3].logo = False


class MazeGenerator:
    maze: Maze

    def __init__(self, width: int, height: int, start: tuple[int, int],
                 ex: tuple[int, int], perfect: bool = True):
        self.width = width
        self.height = height
        self.start = start
        self.exit = ex
        self.perfect = perfect

    def generate_maze(self) -> Maze:
        self.maze = Maze(self.height, self.width)
        self.maze.create_logo()
        return self.maze


if __name__ == "__main__":
    mazegen = MazeGenerator(11, 11, (0, 0), (9, 9))
    mazegen.generate_maze()
