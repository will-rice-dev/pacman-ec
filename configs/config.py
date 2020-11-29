import json

config = {}

#config["givenRandomSeed"] = 10
config["runType"] = "Both" # Could be "Random", "GA", or "Both"

config["mu"] = 100 # This is for Pac Man
config["lambda"] = 475 # This is for Pac Man
config["muGhost"] = 100
config["lambdaGhost"] = 475

config["pillDensity"] = 50
config["fruitSpawnProb"] = 1
config["fruitScore"] = 10
config["timeMult"] = 2

config["numOfRuns"] = 2
config["numOfFitnessEvals"] = 2000

# The following 3 lines are for Pac Man.
config["parentSelect"] = "Over-Selection" # Could be "Over-Selection" or "Fitness Proportional"
config["survivalSelect"] = "Truncation" # Could be "k-Tournament" or "Truncation"
#config["survivalTournyK"] = 10

# The following 3 lines are for Ghosts.
config["parentSelectGhost"] = "Over-Selection" # Could be "Over-Selection" or "Fitness Proportional"
config["survivalSelectGhost"] = "Truncation" # Could be "k-Tournament" or "Truncation"
#config["survivalTournyKGhost"] = 10

config["dMax"] = 3
config["parsimony"] = 5 # This is for Pac Man.
config["parsimonyGhost"] = 5

config["overSelectionPercentage"] = 0.75
config["nodeThreshold"] = 40
config["fruitConst"] = 100

config["logPath"] = "logs/new.log"
config["worldPath"] = "worlds/new.wrld"
config["solPath"] = "solutions/new.sol"
config["solPathGhost"] = "solutions/newGhost.sol"




outFile = open("new.json", "w")
json.dump(config, outFile)
outFile.close()
