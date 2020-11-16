from sys import argv
from datetime import datetime
from src.map import Map
from src.randomGA import runAllRandom
from src.ga import runAllGA
import random
import json


DEFAULT_CONFIG = "configs/default.json"

def main():
    if len(argv) == 2:
        print('Using the provided config!')
        configPath = argv[1]
    elif len(argv) == 1:
        configPath = DEFAULT_CONFIG
        print('Using default config!')
    else:
        print('Invalid number of arguments')
        return

    print(f'The config file being used is: {configPath}')

    config = buildConfig(configPath)

    if config["runType"] == "Random":
        log, sol, world = runAllRandom(config) # Majority of runtime is here.
    elif config["runType"] == "GA":
        log, sol, world = runAllGA(config) # Majority of runtime is here.

    writeFile(config["logPath"], log)
    writeFile(config["solPath"], sol)
    writeFile(config["worldPath"], world)


def writeFile(fileName, fileString):
    file = open(fileName, 'w')
    file.write(fileString)
    file.close()

# The following reads the json config file and puts it into a python dict.
# It also sets the random seed.
def buildConfig(configPath):
    configFile = open(configPath, 'r')
    config = json.loads(configFile.read())
    configFile.close()
    if "givenRandomSeed" in config:
        random.seed(config["givenRandomSeed"])
        config["usedSeed"] = config["givenRandomSeed"]
    else:
        dt = datetime.now()
        microseconds = dt.microsecond
        random.seed(microseconds)
        config["usedSeed"] = microseconds
    return config


if __name__ == "__main__":
    main()
