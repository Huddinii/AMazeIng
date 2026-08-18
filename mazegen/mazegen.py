from enum import Enum
import random


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

    def out(self):
        out = 0
        for wall in self.walls:
            out += 2 ** wall.value
        return out


class Maze:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.cells = [[Cell(x, y) for x in range(height)]for y in range(width)]

    def create_logo(self):
        if self.height > 9 and self.width > 9:
            middle = (int(self.height / 2), int(self.width / 2))
            start = (middle[0] - 2, middle[1] - 3)
            y = start[1]
            for x in range(start[0], start[0] + 5):
                if (x != middle[0]):
                    self.cells[x][y].logo = True
                else:
                    for y in range(start[1], start[1] + 3):
                        self.cells[x][y].logo = True
            start = (middle[0] - 2, middle[1] + 1)
            for x in range(start[0], start[0] + 5):
                for y in range(start[1], start[1] + 3):
                    self.cells[x][y].logo = True
            self.cells[middle[0] - 1][middle[1] + 1].logo = False
            self.cells[middle[0] - 1][middle[1] + 2].logo = False
            self.cells[middle[0] + 1][middle[1] + 2].logo = False
            self.cells[middle[0] + 1][middle[1] + 3].logo = False

    def create_path(self, x: int, y: int):
        self.cells[x][y].checked = True
        wall = {
                Wall.NORTH: (x - 1, y),
                Wall.EAST: (x, y + 1),
                Wall.SOUTH: (x + 1, y),
                Wall.WEST: (x, y - 1)
                }
        oposite = {
                Wall.NORTH: Wall.SOUTH,
                Wall.EAST: Wall.WEST,
                Wall.SOUTH: Wall.NORTH,
                Wall.WEST: Wall.EAST
                }
        to_check = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        while len(to_check) > 0:
            check = random.choice(to_check)
            if (wall[check][0] < 0 or wall[check][0] >= self.height or
                    wall[check][1] < 0 or wall[check][1] >= self.width):
                to_check.remove(check)
            elif self.cells[wall[check][0]][wall[check][1]].checked is True:
                to_check.remove(check)
            elif self.cells[wall[check][0]][wall[check][1]].logo is True:
                to_check.remove(check)
            else:
                self.cells[x][y].walls.remove(check)
                self.cells[wall[check][0]][wall[check][1]] \
                    .walls.remove(oposite[check])
                self.create_path(wall[check][0], wall[check][1])
                to_check.remove(check)


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

    def set_seed(seed: int) -> None:
        random.seed(seed)


if __name__ == "__main__":
    out = "0123456789ABCDEF"
    mazegen = MazeGenerator(11, 11, (0, 0), (9, 9))
    maze = mazegen.generate_maze()
    maze.create_path(0, 0)
    for x in range(11):
        for y in range(11):
            print(out[maze.cells[x][y].out()], end='')
        print()
