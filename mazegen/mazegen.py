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
        self.traveled = False

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
        self.path = None

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

    def dfs(self, x: int, y: int):
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
            i, j = wall[check]
            if (i < 0 or i >= self.height or j < 0 or j >= self.width):
                to_check.remove(check)
            elif self.cells[i][j].checked is True:
                to_check.remove(check)
            elif self.cells[i][j].logo is True:
                to_check.remove(check)
            else:
                self.cells[x][y].walls.remove(check)
                self.cells[i][j].walls.remove(oposite[check])
                self.dfs(i, j)
                to_check.remove(check)

    def prim(self):
        x, y = 0, 0
        cur = (0, 0)
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
        walls = []
        for w in self.cells[x][y].walls:
            if (wall[w][0] >= 0 and wall[w][0] < self.height and
                    wall[w][1] >= 0 and wall[w][1] < self.width):
                walls.append({cur: w, wall[w]: oposite[w]})
        print(walls)
        while len(walls) > 0:
            choice = random.choice(walls)
            c1, c2 = choice.keys()
            print(c1, c2)
            if (self.cells[c1[0]][c1[1]].checked is False or
                    self.cells[c2[0]][c2[1]].checked is False):
                #   remove cur wall and next wall
                #   add valid walls of next to list
                #   set next checked to True
                print(c1, c2)
            walls.remove(choice)

    def solve_maze(self, start: tuple[int, int], end: tuple[int, int]):
        q = []
        self.cells[start[0]][start[1]].traveled = True
        q.append(Node(start))
        walls = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        while len(q) > 0:
            n = q[0]
            q.pop(0)
            dir = {
                    Wall.NORTH: (n.coords[0] - 1, n.coords[1]),
                    Wall.EAST: (n.coords[0], n.coords[1] + 1),
                    Wall.SOUTH: (n.coords[0] + 1, n.coords[1]),
                    Wall.WEST: (n.coords[0], n.coords[1] - 1),
                    }
            if n.coords == end:
                out = ""
                while n.parent is not None:
                    out += n.dir
                    n = n.parent
                self.path = out[::-1]
            for wall in [x for x in walls if x not in
                         self.cells[n.coords[0]][n.coords[1]].walls]:
                if self.cells[dir[wall][0]][dir[wall][1]].traveled is False:
                    self.cells[dir[wall][0]][dir[wall][1]].traveled = True
                    w = Node(dir[wall])
                    w.dir = wall.name[0]
                    w.parent = n
                    q.append(w)

    def make_imperfect(self) -> None:
        for x in range(1, self.height - 1):
            for y in range(1, self.width - 1):
                if len(self.cells[x][y].walls) == 3:
                    self.cells[x][y].walls.pop(random.randint(0, 2))


class Node:
    def __init__(self, coords: tuple[int, int]):
        self.coords = coords
        self.parent = None
        self.dir = None


class MazeGenerator:
    maze: Maze

    def __init__(self, width: int, height: int, start: tuple[int, int],
                 ex: tuple[int, int], perfect: bool = True, sort: str = "DFS"):
        self.width = width
        self.height = height
        self.start = start
        self.exit = ex
        self.perfect = perfect
        self.algo = sort

    def generate_maze(self) -> None:
        self.maze = Maze(self.height, self.width)
        self.maze.create_logo()
        if self.algo == "DFS":
            self.maze.dfs(0, 0)
        else:
            self.maze.prim()
        if self.perfect is False:
            self.maze.make_imperfect()
        self.maze.solve_maze(self.start, self.exit)

    def set_seed(self, seed: int) -> None:
        random.seed(seed)

    def out(self, output: str | None = None):
        out_str = ""
        for x in range(self.height):
            for y in range(self.width):
                hexchar = hex(self.maze.cells[x][y].out())
                out_str += hexchar.replace("0x", '').capitalize()
            out_str += '\n'
        if output is None:
            print(out_str)
            print(f"{self.start[0]},{self.start[1]}")
            print(f"{self.exit[0]},{self.exit[1]}")
            print(self.maze.path)
        else:
            with open(output, "w") as file:
                file.write(f"{out_str}\n")
                file.write(f"{self.start[0]},{self.start[1]}\n")
                file.write(f"{self.exit[0]},{self.exit[1]}\n")
                file.write(f"{self.maze.path}\n")


if __name__ == "__main__":
    mazegen = MazeGenerator(11, 11, (0, 0), (9, 9), perfect=False, sort="PRIM")
    mazegen.set_seed(1000)
    mazegen.generate_maze()
    mazegen.out()
