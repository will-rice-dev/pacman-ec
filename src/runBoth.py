import random
import json
from .play import Game
from .map import Map
from .pacManController import IndividualPacManController
from .evolutionOps import breed, survivalSelection

def runAllBoth(config):
    log = "Result Log\n\n"

    log += "World File: " + config["worldPath"] + "\n"
    log += "Solution File: " + config["solPath"] + "\n"
    log += "Pill Density: " + str(config["pillDensity"]) + "\n"

    log += "Random Seed: " + str(config["usedSeed"]) + "\n\n"

    # Delelte usedSeed because it is not a user parameter, thus should not be put in the log file.
    del config["usedSeed"]

    log += "Config Used:\n"
    log += json.dumps(config) + "\n\n" # This puts the whole config into the log.

    bestScoresOfRuns = ""

    bestScoreOfAllRuns = -9e99 # This will be beat since.
    bestIndOfAllRuns = "" # Declare it because it will get overwritten.
    for i in range(config["numOfRuns"]):
        log += "Run " + str(i + 1) + '\n'
        print(f"Run {i+1}")

        bestIndOfRun, runLog = singleRunGA(config)
        log += runLog
        bestScoresOfRuns += str(bestIndOfRun.gameScore) + '\n'
        print()

        # This keeps track of all runs and saves the very best Game instance.
        if bestIndOfRun.gameScore > bestScoreOfAllRuns:
            bestScoreOfAllRuns = bestIndOfRun.gameScore
            bestIndOfAllRuns = bestIndOfRun

    bestSolOfAllRuns = bestIndOfAllRuns.getSol(bestIndOfAllRuns.root, 0)
    bestWorldOfAllRuns = bestIndOfAllRuns.game.world

    print()
    print(bestScoresOfRuns)

    return log, bestSolOfAllRuns, bestWorldOfAllRuns

def singleRunGA(config):
    runLog = ""
    runWorld = ""

    # The initial population of size mu is created below.
    population = []
    for i in range(config["mu"]):
        population.append(IndividualPacManController(config, brandNew=True))
    numOfFitnessEvals = config["mu"]

    avgScore, bestScoreOfRun, bestIndOfRun = evalPopulation(population)
    toAdd = str(numOfFitnessEvals) + "\t" + str(avgScore) + '\t' + str(bestScoreOfRun)
    runLog += toAdd + '\n'
    print(toAdd)

    if "noChangeForNEvals" in config:
        noChangeForNEvals = config["noChangeForNEvals"]
    else:
        noChangeForNEvals = config["numOfFitnessEvals"] # This will never terminate early.
    evalsWithoutChange = 0

    while numOfFitnessEvals < config["numOfFitnessEvals"]:
        population = evolve(config, population)
        numOfFitnessEvals += config["lambda"]

        avgScore, bestScoreInPop, bestIndividualInPop = evalPopulation(population)
        toAdd = str(numOfFitnessEvals) + "\t" + str(avgScore) + '\t' + str(bestScoreInPop)
        runLog += toAdd + '\n'
        print(toAdd)

        if bestScoreInPop > bestScoreOfRun:
            bestScoreOfRun = bestScoreInPop
            bestIndOfRun = bestIndividualInPop
            evalsWithoutChange = 0
        else:
            evalsWithoutChange += config["lambda"]
            if evalsWithoutChange >= noChangeForNEvals:
                break

    runLog += '\n'
    return bestIndOfRun, runLog

# Evolution happens here.
def evolve(config, population):
    population = breed(population, config)

    return survivalSelection(population, config)

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
