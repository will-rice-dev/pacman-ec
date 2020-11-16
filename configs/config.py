import json

config = {}

#config["givenRandomSeed"] = 10
config["runType"] = "GA"

config["pillDensity"] = 50
config["fruitSpawnProb"] = 1
config["fruitScore"] = 10
config["timeMult"] = 2

config["numOfRuns"] = 2
config["numOfFitnessEvals"] = 1000
config["givenRandomSeed"] = 10

config["parentSelect"] = "Fitness Proportional" # Could also be "Over-Selection"
config["survivalSelect"] = "Truncation" # Could also be "k-Tournament"
#config["survivalTournyK"] = 10

config["dMax"] = 3
config["parsimony"] = 5

config["fruitConst"] = 100

config["logPath"] = "logs/new.log"
config["worldPath"] = "worlds/new.wrld"
config["solPath"] = "solutions/new.sol"




outFile = open("default2.json", "w")
json.dump(config, outFile)
outFile.close()
