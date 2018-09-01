from __future__ import division
import random
from deap import creator, base, tools, algorithms
import os
import config

IND_SIZE = 2+12+12+1+12+4+6


def listToConfig(x):
    config.rhythm_split_11 = config.rhythm_split_11Type(config.rhythm_split_11Range[0]
                                                        + config.rhythm_split_11Range[1] * x[0])
    config.patternNoteNumMul = config.patternNoteNumMulType(config.patternNoteNumMulRange[0]
                                                            + config.patternNoteNumMulRange[1] * x[1])
    for i in range(len(config.scaleWeights)):
        config.scaleWeights[i] = config.scaleWeightsType(config.scaleWeightsRange[0]
                                                         + config.scaleWeightsRange[1] * x[2 + i])
    for i in range(len(config.jumpWeights)):
        config.jumpWeights[i] = config.jumpWeightsType(config.jumpWeightsRange[0]
                                                       + config.jumpWeightsRange[1] * x[14 + i])
    config.minTone = config.minToneType(config.minToneRange[0] + config.minToneRange[1] * x[39])
    config.maxTone = config.maxToneType(config.maxToneRange[0] + config.maxToneRange[1] * x[40])
    config.patternRhythmNum = config.patternRhythmNumType(config.patternRhythmNumRange[0]
                                                          + config.patternRhythmNumRange[1] * x[41])
    config.patternMelodyNum = config.patternMelodyNumType(config.patternMelodyNumRange[0]
                                                          + config.patternMelodyNumRange[1] * x[42])
    for i in range(len(config.sameRhythmWeight)):
        config.sameRhythmWeight[i] = config.sameRhythmWeightType(config.sameRhythmWeightRange[0]
                                                                 + config.sameRhythmWeightRange[1] * x[43 + i])
    for i in range(len(config.sameMelodyWeight)):
        config.sameMelodyWeight[i] = config.sameMelodyWeightType(config.sameMelodyWeightRange[0]
                                                                 + config.sameMelodyWeightRange[1] * x[46 + i])

    config.init()


def evaluate(individual):
    return sum(individual)/IND_SIZE,


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attribute", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

if not os.path.exists("geneticresults/"):
    os.makedirs("geneticresults/")

def main():
    pop = toolbox.population(n=50)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 100

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Make sure everyone is in boundaries
        for i in range(len(offspring)):
            for j in range(len(offspring[i])):
                offspring[i][j] = min(1.0, max(0.0, offspring[i][j]))

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

    return pop


def autorun():
    print "Genetics started"
    pop = main()
    maximum = -1
    maxIndividual = []
    for i in pop:
        if maximum < evaluate(i):
            maximum = evaluate(i)
            maxIndividual = i
    print maximum
    f = open("geneticresults/%d.txt" % len([name for name in os.listdir('geneticresults/')
                                            if os.path.isfile('geneticresults/' + name)]), "w+")
    for i in maxIndividual:
        f.write("%f\n" % i)

    listToConfig(maxIndividual)
    print "Genetics done"


def load(i):
    indidvidual = []
    if i < 0:
        f = open("geneticresults/%d.txt" % (len([name for name in os.listdir('geneticresults/')
                                                if os.path.isfile('geneticresults/' + name)]) + i), "r")
    else:
        f = open("geneticresults/%d.txt" % i, "r")
    indidvidual = f.read().splitlines()
    listToConfig(indidvidual)

