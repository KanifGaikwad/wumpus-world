import math


def demo(a, b, c):
    d = b ** 2 - 4 * a * c
    if d > 0:
        disc = math.sqrt(d)
        root1 = (-b + disc) / (2 * a)
        root2 = (-b - disc) / (2 * a)
        return root1, root2
    elif d == 0:
        return -b / (2 * a)
    else:
        return "This equation has no roots"


class Solver:
    pass


if __name__ == '__main__':
   # arr = [[0]*3]*3
    arr = [[0 for i in range(3)] for j in range(3)]
    print("Original Array")
    for _ in arr:
        for i in _:
            print(i, end=" ")
        print()

    arr[1][2] = 16

    print("Modified Array")
    for _ in arr:
        for i in _:
            print(i, end=" ")
        print()
