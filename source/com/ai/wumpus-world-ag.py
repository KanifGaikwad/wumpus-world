from enum import Enum


class Percepts(Enum):
    BREEZE = 1
    SMELL = 2
    OK = 3
    SCREAMS = 4


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
        self.is_wumpus = False
        self.is_visited = False


def agent_receive_percepts(node):
    percepts = []
    if node.up is not None and node.up.is_wumpus:
        if Percepts.SMELL not in percepts:
            percepts.append(Percepts.SMELL)
    elif node.up is not None and node.up.is_pit:
        if Percepts.BREEZE not in percepts:
            percepts.append(Percepts.BREEZE)
    else:
        if Percepts.OK not in percepts:
            percepts.append(Percepts.OK)

    if node.down is not None and node.down.is_wumpus:
        if Percepts.SMELL not in percepts:
            percepts.append(Percepts.SMELL)
    elif node.down is not None and node.down.is_pit:
        if Percepts.BREEZE not in percepts:
            percepts.append(Percepts.BREEZE)
    else:
        if Percepts.OK not in percepts:
            percepts.append(Percepts.OK)

    if node.left is not None and node.left.is_wumpus:
        if Percepts.SMELL not in percepts:
            percepts.append(Percepts.SMELL)
    elif node.left is not None and node.left.is_pit:
        if Percepts.BREEZE not in percepts:
            percepts.append(Percepts.BREEZE)
    else:
        if Percepts.OK not in percepts:
            percepts.append(Percepts.OK)

    if node.right is not None and node.right.is_wumpus:
        if Percepts.SMELL not in percepts:
            percepts.append(Percepts.SMELL)
    elif node.right is not None and node.right.is_pit:
        if Percepts.BREEZE not in percepts:
            percepts.append(Percepts.BREEZE)
    else:
        if Percepts.OK not in percepts:
            percepts.append(Percepts.OK)

    return percepts


class Agent:
    def __init__(self, world, arrow):
        self.cell = world
        self.arrow = arrow
        self.arrow_cost = -10
        self.move_cost = -1
        self.gold_cost = 150
        self.agen_last_moves = []
        self.agen_shoots_arrow = []
        self.agent_travel_path = []
        self.is_found_gold = False
        self.is_game_over = False

    def agent_shot(self, start):
        percept = []

        if not start.up.is_visited:
            print("Shooting Arrows up")
            self.arrow_cost = self.arrow_cost + (-10)
            self.agen_shoots_arrow.append(Shoot.UP)

        if start.up is not None and not start.up.is_visited and start.up.is_wumpus:
            start.up.is_wumpus = False
            percept.append(Percepts.SCREAMS)
            print("Heard Scream, Wumpus Killed")
            return percept

        if not start.down.is_visited:
            print("Shooting Arrows down")
            self.agen_shoots_arrow.append(Shoot.DOWN)
            self.arrow_cost = self.arrow_cost + (-10)
        if start.down is not None and not start.down.is_visited and start.down.is_wumpus:
            start.down.is_wumpus = False
            percept.append(Percepts.SCREAMS)
            print("Heard Scream, Wumpus Killed")
            return percept

        if not start.right.is_visited:
            print("Shooting Arrows right")
            self.agen_shoots_arrow.append(Shoot.RIGHT)
            self.arrow_cost = self.arrow_cost + (-10)
        if start.right is not None and not start.right.is_visited and start.right.is_wumpus:
            start.right.is_wumpus = False
            percept.append(Percepts.SCREAMS)
            print("Heard Scream, Wumpus Killed")
            return percept

        if not start.left.is_visited:
            print("Shooting Arrows left")
            self.agen_shoots_arrow.append(Shoot.LEFT)
            self.arrow_cost = self.arrow_cost + (-10)
        if start.left is not None and not start.left.is_visited and start.left.is_wumpus:
            start.left.is_wumpus = False
            percept.append(Percepts.SCREAMS)
            print("Heard Scream, Wumpus Killed")
            return percept

        return percept

    def agent_traverse(self, start):

        if self.is_found_gold or self.is_game_over:
            return

        print("Visiting ", start.r, " ", start.c)

        start.is_visited = True

        if start.is_pit or start.is_wumpus:
            print("Gave Over!!!!")
            self.is_game_over = True
            return
        elif not start.is_gold:
            percepts = agent_receive_percepts(start)

            if Percepts.SMELL in percepts:
                print("Getting Smell, Shooting Arrows")
                self.agent_shot(start)
                start.is_visited = False
                if start.down is not None:
                    start.down.is_visited = False
                if start.right is not None:
                    start.right.is_visited = False
                if start.left is not None:
                    start.left.is_visited = False
                if start.up is not None:
                    start.up.is_visited = False

                if start.down is not None and not start.down.is_visited:
                    self.agen_last_moves.append(Go.DOWN)
                    self.agent_travel_path.append(start.down)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.down)

                elif start.left is not None and not start.left.is_visited:
                    self.agen_last_moves.append(Go.LEFT)
                    self.agent_travel_path.append(start.left)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.left)

                elif start.right is not None and not start.right.is_visited:
                    self.agen_last_moves.append(Go.RIGHT)
                    self.agent_travel_path.append(start.right)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.right)

                elif start.up is not None and not start.up.is_visited:
                    self.agen_last_moves.append(Go.UP)
                    self.agent_travel_path.append(start.up)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.up)

            if Percepts.BREEZE in percepts:
                print("Feeling Breeze Back Tracking")
                poped = self.agent_travel_path.pop(len(self.agent_travel_path) - 1)
                if poped is not None:
                    poped.is_visited = False
                    return self.agent_traverse(poped)

            if Percepts.OK in percepts:
                if start.down is not None and not start.down.is_visited:
                    self.agen_last_moves.append(Go.DOWN)
                    self.agent_travel_path.append(start.down)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.down)

                elif start.left is not None and not start.left.is_visited:
                    self.agen_last_moves.append(Go.LEFT)
                    self.agent_travel_path.append(start.left)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.left)

                elif start.right is not None and not start.right.is_visited:
                    self.agen_last_moves.append(Go.RIGHT)
                    self.agent_travel_path.append(start.right)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.right)

                elif start.up is not None and not start.up.is_visited:
                    self.agen_last_moves.append(Go.UP)
                    self.agent_travel_path.append(start.up)
                    self.move_cost = self.move_cost + (-1)
                    return self.agent_traverse(start.up)
        else:
            print("found gold!!!")
            self.gold_cost = self.gold_cost + 150
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
                cell.is_wumpus = True
            arr[row][col] = cell

    for i, x in enumerate(arr):
        for j, y in enumerate(x):
            if y is None:
                cell = Cell(i, j, '')
                arr[i][j] = cell

    for _ in arr:
        for i in _:
            if i.value == '':
                print('-', end=" ")
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
            if i + 1 < pitSize:
                side_cell = arr[i + 1][j]
                current_cell.down = side_cell
            if j - 1 >= 0:
                side_cell = arr[i][j - 1]
                current_cell.left = side_cell
            if j + 1 < pitSize:
                side_cell = arr[i][j + 1]
                current_cell.right = side_cell
    ag = Agent(arr, arrows)
    ag.agent_traverse(arr[0][0])

    print(" ")
    print(" Agent visited area ")
    for _ in arr:
        for i in _:
            if i.is_visited:
                print('v', end=" ")
            else:
                print('_', end=" ")
        print()

    print(" ")
    print("*** Moves Taken by Agent ***")
    for _ in ag.agen_last_moves:
        print(_)
    print("*** Total cost ", ag.move_cost+ag.arrow_cost+ag.gold_cost)
