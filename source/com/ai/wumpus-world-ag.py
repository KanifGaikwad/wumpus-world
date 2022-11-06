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


class WumpusWorld:
    def __init__(self, world, size, arrow):
        self.cells = world
        self.size = size
        self.arrow = arrow
        self.arrow_cost = -10
        self.move_cost = -1
        self.gold_cost = 150
        self.agen_last_move = ""

    def agent_traverse(self, start):
        start.is_visited = True
        nodes = []
        if start.up is not None and not start.up.is_visited:
            nodes.append(start.up)
        if start.down is not None and not start.down.is_visited:
            nodes.append(start.down)
        if start.right is not None and not start.right.is_visited:
            nodes.append(start.right)
        if start.left is not None and not start.left.is_visited:
            nodes.append(start.left)

        node = self.calculate_best_node(nodes)
        print("Go To Cell (", node.r, " ,", node.c, " )")
        if node.is_pit or node.is_wumps:
            print("Gave Over!!!!")
            return
        if not node.is_gold:
            self.agent_traverse(node)
        else:
            print("found gold!!!")
            print("move cost ", self.move_cost)

    def calculate_best_node(self, nodes):
        for node in nodes:
            if not node.is_breeze and not node.is_smell:
                self.move_cost = self.move_cost + (-1)
                node.cost = node.cost + 1
            elif node.is_breeze and node.is_smell:
                self.move_cost = self.move_cost + (-1)
                node.cost = node.cost + 3
            elif node.is_breeze:
                self.move_cost = self.move_cost + (-1)
                node.cost = node.cost + 3
            elif node.is_smell:
                self.move_cost = self.move_cost + (-1)
                node.cost = node.cost + 3
        nodes.sort(key=lambda nd: nd.cost)
        return nodes[0]


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
    print(" Star from Cell ( 0, 0 )")
    ww.agent_traverse(arr[0][0])
