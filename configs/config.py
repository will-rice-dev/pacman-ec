import json

config = {}

#config["givenRandomSeed"] = 10
config["runType"] = "Both" # Could be "Random", "GA", or "Both"

config["mu"] = 100 # This is for Pac Man
config["lambda"] = 475 # This is for Pac Man

config["pillDensity"] = 50
config["fruitSpawnProb"] = 1
config["fruitScore"] = 10
config["timeMult"] = 2

config["numOfRuns"] = 2
config["numOfFitnessEvals"] = 2000

config["parentSelect"] = "Over-Selection" # Could be "Over-Selection" or "Fitness Proportional"
config["survivalSelect"] = "Truncation" # Could be "k-Tournament" or "Truncation"
#config["survivalTournyK"] = 10

config["dMax"] = 3
config["parsimony"] = 2

config["overSelectionPercentage"] = 0.75
config["nodeThreshold"] = 40
config["fruitConst"] = 100

config["logPath"] = "logs/new.log"
config["worldPath"] = "worlds/new.wrld"
config["solPath"] = "solutions/new.sol"




outFile = open("new.json", "w")
json.dump(config, outFile)
outFile.close()
