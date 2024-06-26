import random
import operator

"""
This file is very similar to the evolutionOps.py file. The only changes
    were made to make this suitible for ghosts instead of pac man controllers.
    If redesigned from scratch, both could be accomplished easily in one class.
"""
def breedGhost(population, config):
    offspring = []

    if config["parentSelectGhost"] == "Fitness Proportional":
        parentFitnessProp(population, config, offspring)
    elif config["parentSelectGhost"] == "Over-Selection":
        overSelection(population, config, offspring)

    return offspring

def parentFitnessProp(population, config, offspring):
    weights = [0 for _ in range(len(population))]
    totalWithScores = 0

    minScore = 0
    for i in range(len(population)):
        curScore = population[i].gameScore
        if curScore < minScore:
            minScore = curScore
        weights[i] = curScore

    # The minScore ensures that all weights are at least 1e-99. This
    #   now allows for negative fitnesses. Each weight gets the minScore
    #   value (either negative or zero) subtracted from it so that each weight
    #   goes up proportionally.
    weights = [weight - minScore + 1e-99 for weight in weights]

    while len(offspring) < config["lambdaGhost"]:
        pick1 = random.choices(population, weights=weights, k=1)
        pick1 = pick1[0]

        # This is done to ensure that there is no asexual breeding.
        # It sets the weight of the chosen parent to zero, while also
        #   saving the initial weight in a temp variable.
        index = population.index(pick1)
        temp = weights[index]
        weights[index] = 0

        pick2 = random.choices(population, weights=weights, k=1)
        pick2 = pick2[0]

        # Resets the 1st parent's weight back to its initial value
        weights[index] = temp

        # This gives a 5 percent chance of mutating instead of mating.
        if random.randint(1, 100) <= 5:
            baby = pick1.mutate()
            offspring.append(baby)
            continue

        # Offspring creation happens here by adding the two parents.
        # This uses a custom addition operator of the IndividualGenotype class
        #   in order to recombine the parernts.
        # It creates 2 children and adds them both to offspring.
        baby1, baby2 = pick1 + pick2
        offspring.append(baby1)

        # This ensures that the offspring won't be one too big.
        if len(offspring) == config["lambdaGhost"]:
            break
        offspring.append(baby2)

def overSelection(population, config, offspring):
    newPop = sorted(population, key=operator.attrgetter("gameScore"))

    overSelectionNum = int(len(population) * config["overSelectionPercentage"])
    worsePop = newPop[:overSelectionNum] # This contains the x% of bad inds.
    betterPop = newPop[overSelectionNum:] # This contains the top (1-x)% of inds.

    while len(offspring) < config["lambdaGhost"]:
        # Gives an 80% chance of picking from the better population.
        if random.randint(1,100) <= 80:
            pick1 = random.choice(betterPop)
            betterFirst = True # Will later indicate which pop to add pick1 back to.
            betterPop.remove(pick1)
        else:
            pick1 = random.choice(worsePop)
            betterFirst = False # Will later indicate which pop to add pick1 back to.
            worsePop.remove(pick1)


        # Gives an 80% chance of picking from the better population.
        if random.randint(1,100) <= 80:
            pick2 = random.choice(betterPop)
        else:
            pick2 = random.choice(worsePop)

        # Adding back the first pick. This avoids asexual breeding.
        if betterFirst:
            betterPop.append(pick1)
        else:
            worsePop.append(pick1)

        # This gives a 5 percent chance of mutating instead of mating.
        if random.randint(1, 100) <= 5:
            baby = pick1.mutate()
            offspring.append(baby)
            continue

        # Offspring creation happens here by adding the two parents.
        # This uses a custom addition operator of the IndividualGenotype class
        #   in order to recombine the parernts.
        # It creates 2 children and adds them both to offspring.
        baby1, baby2 = pick1 + pick2
        offspring.append(baby1)

        # This ensures that the offspring won't be one too big.
        if len(offspring) == config["lambdaGhost"]:
            break
        offspring.append(baby2)

# All survival selection methods are below.
def survivalSelectionGhost(population, config):
    if config["survivalSelectGhost"] == "Truncation":
        return truncation(population, config)
    elif config["survivalSelectGhost"] == "k-Tournament":
        return survivalTourny(population, config)

def truncation(population, config):
    newPop = sorted(population, key=operator.attrgetter("gameScore"))
    newPop = newPop[::-1]
    return newPop[:config["muGhost"]]

def survivalTourny(population, config):
    popCopy = [] # Need the copy so that population in parent function is unaffected.
    for i in range(len(population)):
        popCopy.append(population[i])
    newPop = []
    while len(newPop) < config["muGhost"]:
        tourny = random.sample(popCopy, k=config["survivalTournyKGhost"])
        tourny.sort(key=operator.attrgetter("gameScore")) # This sorts the list by the score variable.
        #tourny = tourny[::-1] # This reverses the list, putting the best fitnesses at the front.

        newPop.append(tourny[-1])
        # Below removes the survivor from the population so it is not chosen twice.
        popCopy.remove(tourny[-1])

    return newPop
