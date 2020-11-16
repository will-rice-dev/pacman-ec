import random
from copy import deepcopy
from .playPacManController import Game
from .map import Map

"""
IndividualPacManController both creates controllers and also runs the game.
It also contains methods for recombination and mutation.

Recombination is done in __add__
Mutation is done in mutate()
"""
class IndividualPacManController:
    def __init__(self, config, brandNew, existingTree=None):
        self.sensors = ['G', 'P', 'W', 'F', '#.#']
        self.ops = ['+', '-', '*', '/', 'RAND']
        self.all = self.sensors + self.ops
        self.dMax = config["dMax"]
        self.config = config

        if brandNew:
            self.generateTree(config)
        else:
            self.root = TreeNode()
            # Subtracts one from existingTree because the last spot is always blank.
            self.generateExistingTree(self.root, existingTree[:len(existingTree)-1], 0)

        try:
            self.run(config)
        except:
            print()
            print(self.getSol(self.root, 0))
            raise
        self.nodeCount = self.countNodes(self.root)
        self.sol = self.getSol(self.root, 0)
        self.parsimony(config) # This will adjust the score.

    # This is the ramped half-and-half initialization.
    def generateTree(self, config):
        self.root = TreeNode()
        if random.randint(0,1) == 0:
            self.fill(self.root, 0)
        else:
            self.grow(self.root, 0)

    # This reads a list version of a tree and converts it to nodes.
    def generateExistingTree(self, node, tree, depth):
        # This the value and ignores the depth.
        node.val = tree[0].replace('|', '')

        # This casts the floats as such.
        if '.' in node.val:
            node.val = float(node.val)

        # If the node is a sensor, then it is done.
        if node.val in self.ops:
            node.left = TreeNode()
            node.right = TreeNode()
            i = 2
            # The following loop determines how big the left subtree is and puts it in i.
            while i < len(tree):
                nextVal = tree[i]
                nextDepth = 0
                for letter in nextVal:
                    if letter == '|':
                        nextDepth += 1
                    else:
                        break
                if nextDepth <= depth+1:
                    break
                else:
                    i += 1

            # The following generate the left and right nodes using slices that represent subtrees.
            self.generateExistingTree(node.left, tree[1:i], depth+1)
            # Goes to the end of the list because only subtrees can be passed through.
            self.generateExistingTree(node.right, tree[i:], depth+1)

    # Full ensures that the tree goes to max depth in all spots.
    def fill(self, node, depth):
        if depth == self.dMax:
            node.val = random.choice(self.sensors)
            if node.val == '#.#':
                node.val = random.uniform(-10, 10)
        else:
            node.left = TreeNode()
            node.right = TreeNode()
            self.fill(node.left, depth+1)
            self.fill(node.right, depth+1)
            node.val = random.choice(self.ops)

    # Grow makes a random, possibly not full tree.
    def grow(self, node, depth):
        if depth == self.dMax:
            node.val = random.choice(self.sensors)
            if node.val == '#.#':
                node.val = random.uniform(-10, 10)
        else:
            node.val = random.choice(self.all)
            if node.val in self.ops:
                node.left = TreeNode()
                node.right = TreeNode()
                self.grow(node.left, depth+1)
                self.grow(node.right, depth+1)
            elif node.val == '#.#':
                node.val = random.uniform(-10, 10)

    # Returns the text solution version of the controller. Also used to make subtrees.
    def getSol(self, node, depth):
        out = '|'*depth + str(node.val) + '\n'
        if node.left != None:
            out += self.getSol(node.left, depth+1)
        if node.right != None:
            out += self.getSol(node.right, depth+1)

        return out

    def countNodes(self, node):
        count = 1
        if node.left != None:
            count += self.countNodes(node.left)
        if node.right != None:
            count += self.countNodes(node.right)

        return count

    """
    This overwrites the "IndividualPacManController + IndividualPacManController" to form
        two offspring of type IndividualPacManController from two parents.
    self is parent 1, and other is parent 2.

    This is where recombination takes place.
    """
    def __add__(self, other):
        count1 = self.nodeCount
        count2 = other.nodeCount

        # Chooses a random node to be root of subtree that is swapped.
        sub1 = random.randint(1, count1) - 1
        sub2 = random.randint(1, count2) - 1

        treeList1 = self.sol.split('\n') # Creates an array of nodes.
        subtree1 = self.getSubtree(treeList1, sub1)

        treeList2 = other.sol.split('\n') # Creates an array of nodes.
        subtree2 = other.getSubtree(treeList2, sub2)

        baby1Tree = self.insertSubtree(treeList1, subtree2, sub1)
        baby2Tree = self.insertSubtree(treeList2, subtree1, sub2)

        baby1 = IndividualPacManController(self.config, False, baby1Tree)
        baby2 = IndividualPacManController(self.config, False, baby2Tree)
        return baby1, baby2

    # This returns a list version of a subtree.
    def getSubtree(self, treeList, num):
        subtreeRoot = treeList[num]

        depth = 0
        for letter in subtreeRoot:
            if letter == '|':
                depth += 1
            else:
                break

        subtree = []
        subtree.append(subtreeRoot[depth:])

        i = num + 1
        while i < len(treeList):
            nextVal = treeList[i]

            nextDepth = 0
            for letter in nextVal:
                if letter == '|':
                    nextDepth += 1
                else:
                    break
            if nextDepth <= depth:
                break
            else:
                subtree.append(nextVal[depth:])
                del treeList[i] # Remove because it will late be replaced.

        return subtree

    # This inserts a subtree where another subtree was taken.
    def insertSubtree(self, oldTreeList, newSubtree, location):
        # The tree is the same up until where the previous subtree was removed.
        baby = oldTreeList[:location]

        replacedNode = oldTreeList[location]
        depth = 0
        for letter in replacedNode:
            if letter == '|':
                depth += 1
            else:
                break

        # This puts the subtree at the correct depth.
        for i in range(len(newSubtree)):
            newSubtree[i] = '|'*depth + newSubtree[i]

        baby += newSubtree
        baby += oldTreeList[location+1:]
        return baby

    # Mutation randomly changes a node to another value of the same type.
    def mutate(self):
        mutatedNodeNum = random.randint(1, self.nodeCount) - 1
        treeList = self.sol.split('\n')
        toUpdate = treeList[mutatedNodeNum]

        depth = 0
        for letter in toUpdate:
            if letter == '|':
                depth += 1
            else:
                break

        toUpdate = toUpdate.replace('|', '')
        if toUpdate in self.ops:
            newVal = random.choice(self.ops)
        else:
            newVal = random.choice(self.sensors)
            if newVal == '#.#':
                newVal = random.uniform(-10, 10)

        newVal = '|'*depth + str(newVal)
        treeList[mutatedNodeNum] = newVal

        mutation = IndividualPacManController(self.config, False, treeList)
        return mutation

    # This is where the made controller is run in a random game.
    def run(self, config):
        self.map = getRandomMap(config) # This gets a new map for each fitness eval.
        self.game = Game(self.map, config, self.root) # This is where game is run.
        self.gameScore = self.game.gameScore

    def parsimony(self, config):
        overage = 40 - self.nodeCount # 40 is tunable. It is where my computer slowed down.
        if overage < 0:
            self.gameScore += overage * config["parsimony"]


# This class is used to make the tree.
class TreeNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.val = None

# Gets a random map to evaluate fitness on. Returns as Map class.
def getRandomMap(config):
    randNum = random.randint(0, 99)
    mapPath = "maps/map" + str(randNum) + ".txt"

    mapFile = open(mapPath, 'r')
    mapTxt = mapFile.read()
    mapFile.close()

    map = Map(mapTxt, config)
    return map
