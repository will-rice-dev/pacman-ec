import random
import json
from .play import Game
from .map import Map

def runAllRandom(config):
    log = "Result Log\n\n"

    log += "World File: " + config["worldPath"] + "\n"
    log += "Solution File: " + config["solPath"] + "\n"
    log += "Pill Density: " + str(config["pillDensity"]) + "\n"

    log += "Random Seed: " + str(config["usedSeed"]) + "\n\n"

    # Delelte usedSeed because it is not a user parameter, thus should not be put in the log file.
    del config["usedSeed"]

    log += "Config Used:\n"
    log += json.dumps(config) + "\n\n" # This puts the whole config into the log.

    bestScoreOfAllRuns = -1 # This will be beat since gameScore is >=0.
    bestGameOfAllRuns = "" # Declare it because it will get overwritten.
    for i in range(config["numOfRuns"]):
        log += "Run " + str(i + 1) + '\n'
        print(f"Run {i+1}")

        bestGameOfRun, runLog = singleRunRandom(config)
        log += runLog

        # This keeps track of all runs and saves the very best Game instance.
        if bestGameOfRun.gameScore > bestScoreOfAllRuns:
            bestScoreOfAllRuns = bestGameOfRun.gameScore
            bestGameOfAllRuns = bestGameOfRun

    bestSolOfAllRuns = bestGameOfAllRuns.getSol()
    bestWorldOfAllRuns = bestGameOfAllRuns.world

    return log, bestSolOfAllRuns, bestWorldOfAllRuns

def singleRunRandom(config):
    runLog = ""
    runWorld = ""

    bestScoreOfRun = -1 # This will be beat since gameScore is >=0.
    bestGameOfRun = "" # Declare it because it will get overwritten.
    for i in range(config["numOfFitnessEvals"]):
        controller = generateController()
        map = getRandomMap(config) # This gets a new map for each fitness eval.
        game = Game(map, config, controller) # This is where game is run.

        if game.gameScore > bestScoreOfRun:
            runLog += str(i+1) + "\t" + str(game.gameScore) + "\n"
            toPrint = str(i+1) + "\t" + str(game.gameScore)
            print(toPrint) # This prints as the program runs to show progress.
            bestScoreOfRun = game.gameScore
            bestGameOfRun = game

    runLog += '\n'
    return bestGameOfRun, runLog

# This generates random weights to be used as a controller.
def generateController():
    low = -10
    high = 10

    # Will be in order of G, P, W, F
    return [random.uniform(low, high) for _ in range(4)]

# Gets a random map to evaluate fitness on. Returns as Map class.
def getRandomMap(config):
    randNum = random.randint(0, 99)
    mapPath = "maps/map" + str(randNum) + ".txt"

    mapFile = open(mapPath, 'r')
    mapTxt = mapFile.read()
    mapFile.close()

    map = Map(mapTxt, config)
    return map
