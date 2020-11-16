import random

# This is where the PacMan game is actually simulated.
class Game:
    def __init__(self, map, config, controller):
        self.baseMap = map
        self.config = config
        self.controller = controller

        self.pacMan = (0, 0) # Starts in top left.
        self.ghosts = [(map.rows - 1, map.cols - 1) for _ in range(3)] # Starts in bottom right.

        self.blanks = map.blanks.copy()
        self.walls = map.walls.copy()

        self.pills = set()
        self.time = map.rows * map.cols * config["timeMult"]

        # This saves the start time to calculate gameScore later.
        self.timeStart = self.time

        # This becomes true if a fruit is generated. It becomes false again once eaten.
        self.isFruit = False

        self.pillsEaten = 0
        self.fruitEaten = 0

        self.populate()
        self.world = self.startWorld()

        # Saves the number of pills started with to calculate gameScore later.
        self.pillStartLen = len(self.pills)

        # The gameScore will be set below.
        self.runGame()


    def runGame(self):
        self.gameScore = 0
        while self.time > 0 and len(self.pills) > 0:
            # Previous spots are saved to determine if PacMan passes through a ghost later.
            prevPacSpot = self.pacMan
            prevGhostSpots = [ghost for ghost in self.ghosts]

            self.generateFruit()

            pacNeighbors = self.getNeighbors(prevPacSpot)
            # PacMan has the ability to stay in the same spot, so that spot is added to its neighbors.
            pacNeighbors.add(prevPacSpot)
            ghostNeighbors = [self.getNeighbors(ghost) for ghost in self.ghosts]

            nextPac = self.getNextPac(pacNeighbors)
            self.pacMan = nextPac
            # This uniform randomly chooses a place for the ghost to go.
            self.ghosts = [random.choice(list(row)) for row in ghostNeighbors]

            # The next few lines update the world string.
            self.world += "m " + str(nextPac[1]) + " " + str(self.baseMap.rows - 1 - nextPac[0]) + "\n"
            for i in range(len(self.ghosts)):
                ghost = self.ghosts[i]
                self.world += str(i + 1) + " " + str(ghost[1]) + " " + str(self.baseMap.rows - 1 - ghost[0]) + "\n"

            # The next few files determine if a ghost got PacMan.
            for i in range(len(self.ghosts)):
                ghost = self.ghosts[i]
                if ghost == self.pacMan:
                    return
                if ghost == prevPacSpot:
                    if prevGhostSpots[i] == self.pacMan:
                        return

            # Removes a pill if PacMan landed on one.
            if self.pacMan in self.pills:
                self.pillsEaten += 1
                self.pills.remove(self.pacMan)

            # Removes fruit if PacMan landed on it.
            if self.isFruit:
                if self.pacMan == self.fruit:
                    self.fruitEaten += 1
                    self.isFruit = False

            # Calculates game score.
            self.gameScore = int(100 * (self.pillsEaten / self.pillStartLen))
            self.gameScore += self.config["fruitScore"] * self.fruitEaten

            self.time -= 1
            self.world += "t " + str(self.time) + " " + str(self.gameScore) + "\n"

        # Adds time bonus only if all pills were consumed.
        if len(self.pills) == 0:
            self.gameScore += int(100 * (self.time / self.timeStart))

    # Chooses the next PacMan position based on the controller fitnesses of the
    #   current PacMan's neighbors.
    def getNextPac(self, pacNeighbors):
        bestFitness = -9e99 # This will almost certainly be beaten.
        nextPac = (-1,-1)
        for neighbor in pacNeighbors:
            G, P, W, F = self.pacMapEval(neighbor)
            neighborFitness = self.pacFitnessEval(self.controller, G, P, W, F)
            if neighborFitness > bestFitness:
                bestFitness = neighborFitness
                nextPac = neighbor
        return nextPac


    # Evaluates the fitness based on the given Game's controller and the current Map.
    def pacFitnessEval(self, node, G, P, W, F):
        if node.val == '+':
            return self.pacFitnessEval(node.left, G, P, W, F) + self.pacFitnessEval(node.right, G, P, W, F)
        elif node.val == '-':
            return self.pacFitnessEval(node.left, G, P, W, F) - self.pacFitnessEval(node.right, G, P, W, F)
        elif node.val == '*':
            return self.pacFitnessEval(node.left, G, P, W, F) * self.pacFitnessEval(node.right, G, P, W, F)
        elif node.val == '/':
            left = self.pacFitnessEval(node.left, G, P, W, F)
            # Have to try here to avoid a possible division by 0
            try:
                return left / self.pacFitnessEval(node.right, G, P, W, F)
            except:
                return left * 9e10 # Returning a large number here because the number would be large if being divided by near 0
        elif node.val == 'RAND':
            return random.uniform(self.pacFitnessEval(node.left, G, P, W, F), self.pacFitnessEval(node.right, G, P, W, F))
        elif node.val == 'G':
            return G
        elif node.val == 'P':
            return P
        elif node.val == 'W':
            return W
        elif node.val == 'F':
            return F
        else:
            return node.val

    # Evaluates the newPac board to find G, P, W, and F.
    def pacMapEval(self, newPac):
        G = 9e99
        for ghost in self.ghosts:
            manDistG = self.manhattanDist(ghost, newPac)
            if manDistG < G:
                G = manDistG

        P = 9e99
        for pill in self.pills:
            manDistP = self.manhattanDist(pill, newPac)
            if manDistP < P:
                P = manDistP

        # This will have W = number of adjacent walls + number of adjacent edges.
        #   It was kept this way because edges act the same as walls.
        W = 4 - len(self.getNeighbors(newPac))

        if self.isFruit:
            F = self.manhattanDist(self.fruit, newPac)
        else:
            # A user parameter for the constant fruit value is used if
            #   there is no fruit present on the board.
            F = self.config["fruitConst"]
        return G, P, W, F

    def manhattanDist(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return abs(x2-x1) + abs(y2 - y1)

    # Returns a set of neighboring blank spaces.
    def getNeighbors(self, spot):
        x, y = spot
        out = set()
        if x > 0:
            out.add((x-1, y))
        if y > 0:
            out.add((x, y-1))
        if x < self.baseMap.rows - 1:
            out.add((x+1, y))
        if y < self.baseMap.cols - 1:
            out.add((x, y+1))

        return out - self.walls

    # This starts the world file with beginning of the map.
    #   To translate my implementation where (0, 0) is top left,
    #   the following formula for worldX and worldY was made.
    #       worldX = myY
    #       worldY = Number of Rows - 1 - myX
    #   These are used throughout the code.
    def startWorld(self):
        world = ""
        world += str(self.baseMap.cols) + "\n"
        world += str(self.baseMap.rows) + "\n"

        world += "m 0 " + str(self.baseMap.rows - 1) + "\n"
        world += "1 " + str(self.baseMap.cols - 1) + " 0\n"
        world += "2 " + str(self.baseMap.cols - 1) + " 0\n"
        world += "3 " + str(self.baseMap.cols - 1) + " 0\n"

        for wall in self.walls:
            world += "w " + str(wall[1]) + " " + str(self.baseMap.rows - 1 - wall[0]) + "\n"

        for pill in self.pills:
            world += "p " + str(pill[1]) + " " + str(self.baseMap.rows - 1 - pill[0]) + "\n"

        world += "t " + str(self.time) + " 0\n"
        return world

    # Generates fruit if possible.
    def generateFruit(self):
        prob = random.uniform(0, 100)
        if self.isFruit:
            return
        elif prob < self.config["fruitSpawnProb"]:
            possibleFruitSpots = self.blanks - self.walls - self.pills
            possibleFruitSpots.remove(self.pacMan)
            if len(possibleFruitSpots) == 0:
                return

            self.fruit = random.choice(list(possibleFruitSpots))
            self.world += "f " + str(self.fruit[1]) + " " + str(self.baseMap.rows - 1 - self.fruit[0]) + "\n"
            self.isFruit = True

    # Populates the map with pills to start the game.
    def populate(self):
        self.blanks.remove(self.pacMan) # Do not want a pill on pac man.

        for blank in self.blanks:
            prob = random.uniform(0, 100)
            if prob < self.config["pillDensity"]:
                self.pills.add(blank)

        # Fallback to ensure that there is at least one pill on map.
        if len(self.pills) == 0:
            randomOnePill = random.choice(list(self.blanks))
            self.pills.add(randomOnePill)

        self.blanks.add(self.pacMan) # Add pac man's spot back to blanks.

    # This generates a string that represents the controller formula used for this game.
    def getSol(self):
        sol = str(self.controller[0]) + "*G + "
        sol += str(self.controller[1]) + "*P + "
        sol += str(self.controller[2]) + "*W + "
        sol += str(self.controller[3]) + "*F"
        return sol
