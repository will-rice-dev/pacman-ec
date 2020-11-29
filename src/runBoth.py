import random
import json
from .playBothControllers import Game
from .map import Map
from .pacManControllerNew import IndividualPacManControllerNew
from .ghostController import IndividualGhostController
from .evolutionOps import breed, survivalSelection
from .evolutionOpsGhost import breedGhost, survivalSelectionGhost

def runAllBoth(config):
    log = "Result Log\n\n"

    log += "World File: " + config["worldPath"] + "\n"
    log += "Solution File for Pac-Man: " + config["solPath"] + "\n"
    log += "Solution File for Ghost: " + config["solPathGhost"] + "\n"
    log += "Pill Density: " + str(config["pillDensity"]) + "\n"

    log += "Random Seed: " + str(config["usedSeed"]) + "\n\n"

    # Delelte usedSeed because it is not a user parameter, thus should not be put in the log file.
    del config["usedSeed"]

    log += "Config Used:\n"
    log += json.dumps(config) + "\n\n" # This puts the whole config into the log.

    bestScoresOfRuns = ""

    bestScoreOfAllRunsPac = -9e999 # This will be beat.
    bestIndOfAllRunsPac = "" # Declare it because it will get overwritten.
    bestScoreOfAllRunsGhost = -9e999 # This will be beat.
    bestIndOfAllRunsGhost = "" # Declare it because it will get overwritten.
    for i in range(config["numOfRuns"]):
        log += "Run " + str(i + 1) + '\n'
        print(f"Run {i+1}")

        bestIndOfRunPac, bestIndOfRunGhost, runLog = singleRunBoth(config)
        log += runLog
        bestScoresOfRuns += str(bestIndOfRunPac.gameScore) + '\n'
        print()

        # This keeps track of all runs and saves the very best Game instance.
        if bestIndOfRunPac.gameScore > bestScoreOfAllRunsPac:
            bestScoreOfAllRunsPac = bestIndOfRunPac.gameScore
            bestIndOfAllRunsPac = bestIndOfRunPac

        # This keeps track of all runs and saves the very best Game instance.
        if bestIndOfRunGhost.gameScore > bestScoreOfAllRunsGhost:
            bestScoreOfAllRunsGhost = bestIndOfRunGhost.gameScore
            bestIndOfAllRunsGhost = bestIndOfRunGhost


    bestSolOfAllRunsPac = bestIndOfAllRunsPac.sol
    bestSolOfAllRunsGhost = bestIndOfAllRunsGhost.sol

    curMap = getRandomMap(config)
    bestGame = Game(curMap, config, bestIndOfAllRunsPac.root, bestIndOfAllRunsGhost.root) # This is where game is run.

    return log, bestSolOfAllRunsPac, bestSolOfAllRunsGhost, bestGame.world

def singleRunBoth(config):
    runLog = ""
    runWorld = ""

    # The initial population of size mu is created below for Pac Man.
    pacPop = []
    for i in range(config["mu"]):
        pacPop.append(IndividualPacManControllerNew(config, brandNew=True))

    # The initial population of size mu is created below for Ghosts.
    ghostPop = []
    for i in range(config["muGhost"]):
        ghostPop.append(IndividualGhostController(config, brandNew=True))

    # Here the controllers compete for the first time.
    i = 0
    j = 0
    while i < config["mu"] or j < config["muGhost"]:
        if i >= config["mu"]:
            pacCont = random.choice(pacPop)
        else:
            pacCont = pacPop[i]

        if j >= config["muGhost"]:
            ghostCont = random.choice(ghostPop)
        else:
            ghostCont = ghostPop[j]

        curMap = getRandomMap(config)
        curGame = Game(curMap, config, pacCont.root, ghostCont.root) # This is where game is run.

        # Automatically averages if necessary.
        pacCont.setScore(curGame.gameScore)
        ghostCont.setScore(curGame.ghostScore)
        i += 1
        j += 1

    numOfFitnessEvals = max(config["mu"], config["muGhost"])

    avgScore, bestScoreOfRunPac, bestIndOfRunPac = evalPopulation(pacPop)
    toAdd = str(numOfFitnessEvals) + "\t" + str(avgScore) + '\t' + str(bestScoreOfRunPac)
    runLog += toAdd + '\n'
    print(toAdd)

    avgScore, bestScoreOfRunGhost, bestIndOfRunGhost = evalPopulation(ghostPop)

    while numOfFitnessEvals < config["numOfFitnessEvals"]:
        pacPop, ghostPop = evolve(config, pacPop, ghostPop)
        numOfFitnessEvals += max(config["lambda"], config["lambdaGhost"])

        avgScore, bestScoreInPopPac, bestIndividualInPopPac = evalPopulation(pacPop)
        toAdd = str(numOfFitnessEvals) + "\t" + str(avgScore) + '\t' + str(bestScoreInPopPac)
        runLog += toAdd + '\n'
        print(toAdd)

        if bestScoreInPopPac > bestScoreOfRunPac:
            bestScoreOfRunPac = bestScoreInPopPac
            bestIndOfRunPac = bestIndividualInPopPac

        avgScore, bestScoreInPopGhost, bestIndividualInPopGhost = evalPopulation(ghostPop)

        if bestScoreInPopGhost > bestScoreOfRunGhost:
            bestScoreOfRunGhost = bestScoreInPopGhost
            bestIndOfRunGhost = bestIndividualInPopGhost

    runLog += '\n'
    return bestIndOfRunPac, bestIndOfRunGhost, runLog

# Evolution happens here.
def evolve(config, pacPop, ghostPop):
    pacPop = breed(pacPop, config)
    ghostPop = breedGhost(ghostPop, config)

    # Here the controllers compete for the first time.
    i = 0
    j = 0
    while i < config["lambda"] or j < config["lambdaGhost"]:
        if i >= config["lambda"]:
            pacCont = random.choice(pacPop)
        else:
            pacCont = pacPop[i]

        if j >= config["lambdaGhost"]:
            ghostCont = random.choice(ghostPop)
        else:
            ghostCont = ghostPop[j]

        curMap = getRandomMap(config)
        curGame = Game(curMap, config, pacCont.root, ghostCont.root) # This is where game is run.

        # Automatically averages if necessary.
        pacCont.setScore(curGame.gameScore)
        ghostCont.setScore(curGame.ghostScore)
        i += 1
        j += 1

    return survivalSelection(pacPop, config), survivalSelection(ghostPop, config)

def evalPopulation(population):
    totScore = 0
    bestScore = -9e99
    bestIndividual = ""

    for individual in population:
        curScore = individual.gameScore
        totScore += curScore
        if curScore > bestScore:
            bestScore = curScore
            bestIndividual = individual

    avgScore = totScore / len(population)
    return avgScore, bestScore, bestIndividual

# Gets a random map to evaluate fitness on. Returns as Map class.
def getRandomMap(config):
    randNum = random.randint(0, 99)
    mapPath = "maps/map" + str(randNum) + ".txt"

    mapFile = open(mapPath, 'r')
    mapTxt = mapFile.read()
    mapFile.close()

    map = Map(mapTxt, config)
    return map
