from os.path import exists
from random import randint

Lines = ''
records_list = []
dimension = 0
environment = ''
status = ''
goldX = 0
goldY = 0
if exists('env1.txt'):
    input_file = open('env1.txt', 'r')  # open the input file in read mode
    Lines = input_file.readlines()
else:
    print("File not found")


class Cell:
    pit = False
    wumpus = False
    gold = False
    agent = False

    def __init__(self):
        self.pit = False
        self.wumpus = False
        self.gold = False
        self.agent = False

    def __str__(self):
        return 'Pit:' + str(self.pit) + ' Wumpus:' + str(self.wumpus) + ' Gold:' + str(self.gold) + ' Agent:' + str(
            self.agent)


class Agent:
    arrows = 0
    xCoordinate = 0
    yCoordinate = 0
    score = 0

    def __init__(self):
        self.arrows = 0
        self.xCoordinate = 0
        self.yCoordinate = 0
        self.score = 0

    def __init__(self, arrows):
        self.arrows = arrows
        self.xCoordinate = 1
        self.yCoordinate = 1
        self.score = 0

    def __str__(self):
        return 'Agent Arrows: ' + str(self.arrows) + ' Position: (' + str(self.xCoordinate) + ',' + str(
            self.yCoordinate) + ')'


def initialize():
    global dimension, environment, goldX, goldY
    dimension = int(Lines[0])
    environment = [[Cell() for x in range(dimension)] for y in range(dimension)]
    agent = Agent(int(Lines[1]))
    for line in Lines:
        recordLine = line.split(" ")
        if recordLine[0].lower().startswith('p'):
            environment[int(recordLine[1])][int(recordLine[2])].pit = True
        elif recordLine[0].lower().startswith('w'):
            environment[int(recordLine[1])][int(recordLine[2])].wumpus = True
        elif recordLine[0].lower().startswith('g'):
            goldX = int(recordLine[1])
            goldY = int(recordLine[2])
            environment[int(recordLine[1])][int(recordLine[2])].gold = True
    return agent


def printEnvironmentState(agent):
    global dimension, environment
    tempEnvironment = environment
    tempEnvironment[int(agent.xCoordinate)][int(agent.yCoordinate)].agent = True
    print("-------------------ENVIRONMENT-------------------")
    for i in range(dimension):
        for j in range(dimension):
            if tempEnvironment[i][j].pit:
                print("P", end=' ')
            elif tempEnvironment[i][j].wumpus:
                print("W", end=' ')
            elif tempEnvironment[i][j].gold:
                print("G", end=' ')
            elif tempEnvironment[i][j].agent:
                print("A", end=' ')
            else:
                print("-", end=' ')
        print()


def getCoordinates(agent, direction):
    if direction == 1:
        return Point(agent.xCoordinate - 1, agent.yCoordinate)
    elif direction == 2:
        return Point(agent.xCoordinate + 1, agent.yCoordinate)
    elif direction == 3:
        return Point(agent.xCoordinate, agent.yCoordinate - 1)
    else:
        return Point(agent.xCoordinate, agent.yCoordinate + 1)


def getInput(agent):
    global status, goldY
    print("What action should agent take?\n1. Go\t2. Shoot")
    actionInput = randint(1, 2)
    print("In which direction?\n1. Up\t2. Down\t3. Left\t4. Right")
    directionInput = randint(1,4)
    if actionInput == 1:
        move = 'Go'
    else:
        move = 'Shoot'
    print("Agent chose to " + move + " in direction " + str(directionInput))
    return actionInput, directionInput


def moveAgent(agent, direction):
    global dimension, environment
    environment[agent.xCoordinate][agent.yCoordinate].agent = False
    if direction == 1:
        if agent.xCoordinate == 0:
            print("\nAt the edge of the environment, BUMP!\n")
        else:
            agent.xCoordinate -= 1
            agent.score -= 1
    elif direction == 2:
        if agent.xCoordinate == dimension - 1:
            print("\nAt the edge of the environment, BUMP!\n")
        else:
            agent.xCoordinate += 1
            agent.score -= 1
    elif direction == 3:
        if agent.yCoordinate == 0:
            print("\nAt the edge of the environment, BUMP!\n")
        else:
            agent.yCoordinate -= 1
            agent.score -= 1
    else:
        if agent.yCoordinate == dimension - 1:
            print("\nAt the edge of the environment, BUMP!\n")
        else:
            agent.yCoordinate += 1
            agent.score -= 1


def checkForWumpusShot(xCoordinate, yCoordinate):
    if isCellValidForChecking(xCoordinate, yCoordinate):
        if environment[xCoordinate][yCoordinate].wumpus:
            print("Wumpus screams and is killed")
            environment[xCoordinate][yCoordinate].wumpus = False
        else:
            print("Arrow wasted")


def shootingOutcome(agentX, agentY, direction):
    if direction == 1:
        checkForWumpusShot(agentX - 1, agentY)
    elif direction == 2:
        checkForWumpusShot(agentX + 1, agentY)
    elif direction == 3:
        checkForWumpusShot(agentX, agentY - 1)
    else:
        checkForWumpusShot(agentX, agentY + 1)


def agentShoot(agent, direction):
    if agent.arrows > 0:
        agent.arrows -= 1
        agent.score -= 10
        shootingOutcome(agent.xCoordinate, agent.yCoordinate, direction)
    else:
        print("No more arrows available, cannot shoot")


def isCellValidForChecking(xCoordinate, yCoordinate):
    if xCoordinate < 0 or yCoordinate < 0:
        return False
    elif xCoordinate > dimension - 1 or yCoordinate > dimension - 1:
        return False
    return True


def getPerception(xCoordinate, yCoordinate):
    minStatus = ''
    if environment[xCoordinate][yCoordinate].wumpus:
        minStatus += 'Stench\t'
    if environment[xCoordinate][yCoordinate].pit:
        minStatus += 'Breeze\t'
    return minStatus


def checkAroundAgent(xCoordinate, yCoordinate):
    global dimension
    perceptionAround = ''
    if isCellValidForChecking(xCoordinate, yCoordinate):
        if isCellValidForChecking(xCoordinate - 1, yCoordinate):
            perceptionAround += getPerception(xCoordinate - 1, yCoordinate)
        if isCellValidForChecking(xCoordinate + 1, yCoordinate):
            perceptionAround += getPerception(xCoordinate + 1, yCoordinate)
        if isCellValidForChecking(xCoordinate, yCoordinate - 1):
            perceptionAround += getPerception(xCoordinate, yCoordinate - 1)
        if isCellValidForChecking(xCoordinate, yCoordinate + 1):
            perceptionAround += getPerception(xCoordinate, yCoordinate + 1)
    return perceptionAround


def getScore(agent):
    scoreStr = '\n-----AGENT\'s SCORE-----'
    scoreStr += "\nScore: " + str(agent.score)
    return scoreStr


def perceiveEnvironment(agent):
    global status
    status = ''
    print('----------------AGENT PERCEPTION----------------')
    status += "\nAbove: " + str(checkAroundAgent(agent.xCoordinate - 1, agent.yCoordinate))
    status += "\nBelow: " + str(checkAroundAgent(agent.xCoordinate + 1, agent.yCoordinate))
    status += "\nLeft: " + str(checkAroundAgent(agent.xCoordinate, agent.yCoordinate - 1))
    status += "\nRight: " + str(checkAroundAgent(agent.xCoordinate, agent.yCoordinate + 1))
    print(status)


def checkStatus(agent):
    if environment[agent.xCoordinate][agent.yCoordinate].wumpus:
        print("Game over | Agent killed by wumpus")
        return True
    elif environment[agent.xCoordinate][agent.yCoordinate].pit:
        print("Game over | Agent fell in a pit")
        return True
    elif environment[agent.xCoordinate][agent.yCoordinate].gold:
        agent.score += 150
        print("Agent found the gold!")
        return True
    else:
        return False


def main():
    global dimension, environment
    gameOver = False
    agent = initialize()
    printEnvironmentState(agent)
    while not gameOver:
        perceiveEnvironment(agent)
        getScore(agent)
        print('###################NEW INPUT###################')
        action, direction = getInput(agent)
        if action == 1:
            moveAgent(agent, direction)
        else:
            agentShoot(agent, direction)
        gameOver = checkStatus(agent)
        printEnvironmentState(agent)
        print(getScore(agent))
    # perceiveEnvironment(agent)
    # getScore(agent)
    # print('###################NEW INPUT###################')
    # action, direction = getInput(agent)
    # if action == 1:
    #     moveAgent(agent, direction)
    # else:
    #     agentShoot(agent, direction)
    # gameOver = checkStatus(agent)
    # printEnvironmentState(agent)
    # print(getScore(agent))


if __name__ == '__main__':
    main()
