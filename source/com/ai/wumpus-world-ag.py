from enum import Enum


class Percepts(Enum):
    BREEZE = 1
    SMELL = 2
    OK = 3


class Go(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Shoot(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Cell:
    def __init__(self, r, c, w_value):
        self.r = r
        self.c = c
        self.value = w_value
        self.cost = 0
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.is_gold = False
        self.is_pit = False
        self.is_wumps = False
        self.is_breeze = False
        self.is_smell = False
        self.pit_possibility = 0
        self.wumps_possibility = 0
        self.is_visited = False


def agent_percepts(node):
    percepts = []
    if node.is_smell:
        percepts.append(Percepts.SMELL)
    if node.is_breeze:
        percepts.append(Percepts.BREEZE)
    if not node.is_smell and not node.is_breeze:
        percepts.append(Percepts.OK)
    return percepts


class WumpusWorld:
    def __init__(self, world, size, arrow):
        self.cells = world
        self.size = size
        self.arrow = arrow
        self.arrow_cost = -10
        self.gold_cost = 150
        self.agen_last_moves = []
        self.agen_shoots_arrow = []
        self.agent_travel_path = []
        self.is_found_gold = False

    def agent_traverse(self, start, back_track):

        if self.is_found_gold:
            return
        # To do - do not initialize the brreze and smell calculate on the go based on the percepts
        print("Visiting ", start.r, " ", start.c)

        start.is_visited = True
        if not back_track:
            self.agent_travel_path.append(start)

        if start.is_pit or start.is_wumps:
            print("Gave Over!!!!")
            for _ in self.cells:
                for i in _:
                    print(i.cost, end=" ")
                print()

            return
        elif not start.is_gold:
            percepts = agent_percepts(start)
            if Percepts.OK in percepts:
                if start.up is not None and (not start.up.is_visited or back_track):
                    self.agen_last_moves.append(Go.UP)
                    self.agent_traverse(start.up, False)
                if start.down is not None and (not start.down.is_visited or back_track):
                    self.agen_last_moves.append(Go.DOWN)
                    self.agent_traverse(start.down, False)
                if start.right is not None and (not start.right.is_visited or back_track):
                    self.agen_last_moves.append(Go.RIGHT)
                    self.agent_traverse(start.right, False)
                if start.left is not None and (not start.left.is_visited or back_track):
                    self.agen_last_moves.append(Go.LEFT)
                    self.agent_traverse(start.left, False)

            if Percepts.SMELL in percepts:
                self.agen_shoots_arrow.append(Shoot.UP)
                self.agen_shoots_arrow.append(Shoot.DOWN)
                self.agen_shoots_arrow.append(Shoot.RIGHT)
                self.agen_shoots_arrow.append(Shoot.LEFT)
                print("Shot Arrows ")
                if start.up is not None and (not start.up.is_visited or back_track):
                    if start.up.is_wumps:
                        print("Wumps Killed")
                    start.up.is_wumps = False
                    self.agen_last_moves.append(Go.UP)
                    self.agent_traverse(start.up, False)
                elif start.down is not None and (not start.down.is_visited or back_track):
                    if start.down.is_wumps:
                        print("Wumps Killed")
                    start.down.is_wumps = False
                    self.agen_last_moves.append(Go.DOWN)
                    self.agent_traverse(start.down, False)
                elif start.right is not None and (not start.right.is_visited or back_track):
                    if start.right.is_wumps:
                        print("Wumps Killed")
                    start.right.is_wumps = False
                    self.agen_last_moves.append(Go.RIGHT)
                    self.agent_traverse(start.right, False)
                elif start.left is not None and (not start.left.is_visited or back_track):
                    if start.left.down.is_wumps:
                        print("Wumps Killed")
                    start.right.is_wumps = False
                    self.agen_last_moves.append(Go.LEFT)
                    self.agent_traverse(start.left, False)

            if Percepts.BREEZE in percepts:
                print("Back Tracking")
                poped = self.agent_travel_path.pop(len(self.agent_travel_path) - 1)
                self.agent_traverse(poped, True)
        else:
            print("found gold!!!")
            self.is_found_gold = True
            return


if __name__ == '__main__':
    lines = open("env1.txt", "r")
    arr = []
    pitSize = 0
    arrows = 0
    for k, line in enumerate(lines):
        if k == 0:
            pitSize = int(line)
        elif k == 1:
            arr = [[None for i in range(pitSize)] for j in range(pitSize)]
            arrows = int(line)
        elif k > 1:
            inputs = line.replace("\n", "").split(" ")
            row = int(inputs[1]) - 1
            col = int(inputs[2]) - 1
            value = inputs[0]
            cell = Cell(row, col, value)
            if inputs[0] == "g":
                cell.is_gold = True
            elif inputs[0] == "p":
                cell.is_pit = True
            elif inputs[0] == "w":
                cell.is_wumps = True
            arr[row][col] = cell

    for i, x in enumerate(arr):
        for j, y in enumerate(x):
            if y is None:
                cell = Cell(i, j, '')
                arr[i][j] = cell

    for _ in arr:
        for i in _:
            if i.value == '':
                print('x', end=" ")
            else:
                print(i.value, end=" ")
        print()

    for i, x in enumerate(arr):
        for j, y in enumerate(x):
            if y is None:
                cell = Cell(i, j, '')
                arr[i][j] = cell
            current_cell = arr[i][j]
            if i - 1 >= 0:
                side_cell = arr[i - 1][j]
                current_cell.up = side_cell
                if side_cell.is_pit:
                    current_cell.is_breeze = True
                if side_cell.is_wumps:
                    current_cell.is_smell = True
            if i + 1 < pitSize:
                side_cell = arr[i + 1][j]
                current_cell.down = side_cell
                if side_cell.is_pit:
                    current_cell.is_breeze = True
                if side_cell.is_wumps:
                    current_cell.is_smell = True
            if j - 1 >= 0:
                side_cell = arr[i][j - 1]
                current_cell.left = side_cell
                if side_cell.is_pit:
                    current_cell.is_breeze = True
                if side_cell.is_wumps:
                    current_cell.is_smell = True
            if j + 1 < pitSize:
                side_cell = arr[i][j + 1]
                current_cell.right = side_cell
                if side_cell.is_pit:
                    current_cell.is_breeze = True
                if side_cell.is_wumps:
                    current_cell.is_smell = True
    ww = WumpusWorld(arr, pitSize, arrows)
    ww.agent_traverse(arr[0][0], False)
    print(ww.agen_last_moves)
