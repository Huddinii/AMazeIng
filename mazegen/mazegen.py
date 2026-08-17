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
        for i in range(height):
            for j in range(width):
                self.cells[i][j] = Cell(i, j)

    def createLogo():
        return


class MazeGenerator:
    def __init__(self, width: int, height: int, start: tuple[int, int],
                 ex: tuple[int, int], perfect: bool):
        self.width = width
        self.height = height
        self.start = start
        self.exit = ex
        self.perfect = perfect
        self.Maze

    def GenerateMaze(self):
        self.Maze = Maze(self.height, self.width)
        self.Maze.createLogo()
