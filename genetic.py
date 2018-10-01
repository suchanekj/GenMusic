from __future__ import division
import random
from deap import creator, base, tools, algorithms
import os
import time
import config
import melody
import write
import miditotxt
import discriminator


def evaluate(individual):
    global tim
    config.listToConfig(individual)
    config.init()
    x = 0
    for i in range(config.evaluationToAverage):
        tim += time.process_time()
        melody.generate()
        write.write([melody.melody], [melody.rhythm])
        write.save()
        track = miditotxt.rewrite('output.mid')
        tim -= time.process_time()
        x += discriminator.evaluate(track)
    return x/config.evaluationToAverage,


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attribute", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, n=config.IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

if not os.path.exists("geneticresults/"):
    os.makedirs("geneticresults/")

def evolve():
    pop = toolbox.population(n=config.geneticPopulationSize)
    CXPB, MUTPB, NGEN = config.geneticCXPB, config.geneticMUTPB, config.geneticNGEN

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

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
    global tim
    tim -= time.process_time()
    pop = evolve()
    maximum = -1
    maxIndividual = []
    for i in pop:
        if maximum < evaluate(i)[0]:
            maximum = evaluate(i)[0]
            maxIndividual = i
    print(maximum)
    f = open("geneticresults/%d.txt" % len([name for name in os.listdir('geneticresults/')
                                            if os.path.isfile('geneticresults/' + name)]), "w+")
    for i in maxIndividual:
        f.write("%f\n" % i)

    config.listToConfig(maxIndividual)
    tim += time.process_time()


def load(i):
    indidvidual = []
    if i < 0:
        f = open("geneticresults/%d.txt" % (len([name for name in os.listdir('geneticresults/')
                                                if os.path.isfile('geneticresults/' + name)]) + i), "r")
    else:
        f = open("geneticresults/%d.txt" % i, "r")
    indidvidual = list(map(float, f.read().splitlines()))
    config.listToConfig(indidvidual)

