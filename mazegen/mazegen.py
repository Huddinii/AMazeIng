from enum import Enum
import random


class Wall(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.walls = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        self.position = (x, y)
        self.checked = False
        self.logo = False
        self.traveled = False

    def out(self) -> int:
        out = 0
        for wall in self.walls:
            out += 2 ** wall.value
        return out


class Maze:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.cells = [[Cell(x, y) for x in range(height)]for y in range(width)]
        self.path: str | None = None

    def create_logo(self) -> None:
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

    def dfs(self, x: int, y: int) -> None:
        self.cells[x][y].checked = True
        to_check = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        while len(to_check) > 0:
            check = random.choice(to_check)
            i, j = self.get_cell(x, y, check)
            if (i < 0 or i >= self.height or j < 0 or j >= self.width):
                to_check.remove(check)
            elif self.cells[i][j].checked is True:
                to_check.remove(check)
            elif self.cells[i][j].logo is True:
                to_check.remove(check)
            else:
                self.cells[x][y].walls.remove(check)
                self.cells[i][j].walls.remove(self.get_opposite(check))
                self.dfs(i, j)
                to_check.remove(check)

    def prim(self) -> None:
        x, y = 0, 0
        cur = (0, 0)
        self.cells[x][y].checked = True
        walls = []
        for w in self.cells[x][y].walls:
            dir = self.get_cell(x, y, w)
            if (dir[0] >= 0 and dir[0] < self.height and
                    dir[1] >= 0 and dir[1] < self.width):
                walls.append({cur: w, dir: self.get_opposite(w)})
        while len(walls) > 0:
            choice = random.choice(walls)
            c1, c2 = choice.keys()
            c1_check = (self.cells[c1[0]][c1[1]].checked ^
                        self.cells[c1[0]][c1[1]].logo)
            c2_check = (self.cells[c2[0]][c2[1]].checked ^
                        self.cells[c2[0]][c2[1]].logo)
            if ((c1_check is False and c2_check is True)
                    or (c1_check is True and c2_check is False)):
                if not c1_check:
                    next = c1
                elif not c2_check:
                    next = c2
                self.remove_walls(choice)
                self.cells[next[0]][next[1]].checked = True
                for w in self.cells[next[0]][next[1]].walls:
                    dir = self.get_cell(next[0], next[1], w)
                    if (dir[0] >= 0 and dir[0] < self.height and
                            dir[1] >= 0 and dir[1] < self.width):
                        walls.append({next: w, dir: self.get_opposite(w)})
            walls.remove(choice)

    def remove_walls(self, walls: dict[tuple[int, int], Wall]) -> None:
        for key in walls.keys():
            self.cells[key[0]][key[1]].walls.remove(walls[key])

    def get_cell(self, x: int, y: int, k: Wall) -> tuple[int, int]:
        wall = {
                Wall.NORTH: (x - 1, y),
                Wall.EAST: (x, y + 1),
                Wall.SOUTH: (x + 1, y),
                Wall.WEST: (x, y - 1)}
        return wall[k]

    def get_opposite(self, k: Wall) -> Wall:
        opposite = {
                Wall.NORTH: Wall.SOUTH,
                Wall.EAST: Wall.WEST,
                Wall.SOUTH: Wall.NORTH,
                Wall.WEST: Wall.EAST}
        return opposite[k]

    def solve_maze(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        q = []
        self.cells[start[0]][start[1]].traveled = True
        q.append(Node(start))
        walls = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        while len(q) > 0:
            n = q[0]
            q.pop(0)
            if n.coords == end:
                out = ""
                while n.parent is not None:
                    out = out + n.dir
                    n = n.parent
                self.path = out[::-1]
                return
            for wall in [x for x in walls if x not in
                         self.cells[n.coords[0]][n.coords[1]].walls]:
                dir = self.get_cell(n.coords[0], n.coords[1], wall)
                if self.cells[dir[0]][dir[1]].traveled is False:
                    self.cells[dir[0]][dir[1]].traveled = True
                    w = Node(dir)
                    w.dir = wall.name[0]
                    w.parent = n
                    q.append(w)

    def make_imperfect(self) -> None:
        for x in range(1, self.height - 1):
            for y in range(1, self.width - 1):
                if len(self.cells[x][y].walls) == 3:
                    self.cells[x][y].walls.pop(random.randint(0, 2))

    def input_check(self, x: int, y: int) -> bool:
        if self.cells[x][y].logo is True:
            return True


class Node:
    def __init__(self, coords: tuple[int, int]) -> None:
        self.coords = coords
        self.parent: Node | None = None
        self.dir: str = ""


class MazeGenerator:
    maze: Maze

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool = True,
                 sort: str = "DFS") -> None:
        self.width = width
        self.height = height
        self.start = entry
        self.exit = exit
        self.perfect = perfect
        self.algo = sort

    def generate_maze(self) -> None:
        self.maze = Maze(self.height, self.width)
        self.maze.create_logo()
        self.check_params()
        if self.algo == "DFS":
            self.maze.dfs(0, 0)
        else:
            self.maze.prim()
        if self.perfect is False:
            self.maze.make_imperfect()
        self.maze.solve_maze(self.start, self.exit)

    def set_seed(self, seed: int) -> None:
        random.seed(seed)

    def out(self, output: str | None = None) -> None:
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

    def check_params(self) -> None:
        x, y = self.start
        if (x < 0 or x >= self.height or y < 0 or y >= self.width):
            raise RuntimeError("Start is outside the Maze")
        x, y = self.exit
        if (x < 0 or x >= self.height or y < 0 or y >= self.width):
            raise RuntimeError("Exit is outside the Maze")
        if self.maze.input_check(self.start) is True:
            raise RuntimeError("Start is inside 42 Logo")
        if self.maze.input_check(self.exit) is True:
            raise RuntimeError("Exit is inside 42 Logo")


if __name__ == "__main__":
    mazegen = MazeGenerator(11, 11, (0, 0), (9, 9), sort="PRIM")
    mazegen.set_seed(1000)
    mazegen.generate_maze()
    mazegen.out("output.txt")
