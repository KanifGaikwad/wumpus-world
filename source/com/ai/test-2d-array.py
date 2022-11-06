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


class WumpusWorld:
    def __init__(self, world, size, arrow):
        self.cells = world
        self.size = size
        self.arrow = arrow
        self.arrowCost = -10
        self.moveCost = -1
        self.goldCost = 150


"""
    def traverse(self, r, c):
        j = r
        i = c
        found_gold = 0
        result_down = [4] * 0
        result_left = [4] * 0
        result_up = [4] * 0
        result_right = [4] * 0
        while found_gold == 0:
            if i - 1 >= 0:
                print("checking up")
                up = self.check_content(i - 1, j)
                result_up = self.make_choice(up, i - 1, j)
            if i + 1 < self.size:
                print("checking down")
                down = self.check_content(i + 1, j)
                result_down = self.make_choice(down, i + 1, j)
            if j - 1 >= 0:
                print("checking left")
                left = self.check_content(i, j - 1)
                result_left = self.make_choice(left, i + 1, j)
            if j + 1 < self.size:
                print("checking right")
                right = self.check_content(i, j + 1)
                result_right = self.make_choice(right, i + 1, j)

            if result_up[1] == 1 or result_down[1] == 1 or result_left[1] == 1 or result_right == 1:
                found_gold = 1
            else:
                good_choice = []

    def make_choice(self, site, i, j):
        good_choice = [4] * 0
        if site == "g":
            good_choice = [150, 1, i - 1, j]
        elif site == "w":
            if self.arrow > 0:
                self.world[i - 1, j] = ''
                self.arrowCost = self.arrowCost + (-10)
                self.arrow = self.arrow - 1
                good_choice = [-11, 0, i - 1, j]
        elif site == "":
            good_choice = [-1, 0, i - 1, j]
        return good_choice

    def check_content(self, l, m):
        up = self.world[l][m]
        if up == "g":
            print("found gold")
        elif up == "w":
            print("found wumpus")
        elif up == "p":
            print("found pit")
        else:
            print("empty cell")
        return up
"""


def print_array(arr2):
    for _ in arr2:
        for i in _:
            print(i, end=" ")
        print(" ")


if __name__ == '__main__':
    lines = open("env1.txt", "r")

    pitSize = 0
    arrows = 0
    for k, line in enumerate(lines):
        if k == 0:
            pitSize = int(line)
            # arr = {(i, j): None for i in range(pitSize) for j in range(pitSize)}
            arr = [[0] * pitSize] * pitSize
        elif k == 1:
            arrows = int(line)
        elif k > 1:
            print(line)
            inputs = line.replace("\n", "").split(" ")
            row = int(inputs[1])
            col = int(inputs[2])
            value = inputs[0]
            cell = Cell(row, col, value)
            if inputs[0] == "g":
                arr[row][col] = "g"
                cell.is_gold = True
                print_array(arr)
            elif inputs[0] == "p":
                arr[row][col] = "p"
                cell.is_pit = True
                print_array(arr)
            elif inputs[0] == "w":
                arr[row][col] = "w"
                cell.is_wumps = True
                print_array(arr)

for idx, x in enumerate(arr):
    for idy, y in enumerate(x):
        if y == 0:
            arr[idx][idy] = "x"
