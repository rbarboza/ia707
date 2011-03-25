from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import DBAdapters
from random import shuffle
from math import sqrt
from random import randint, sample
from pyevolve import Mutators

from collections import defaultdict

import pylab

import psyco
psyco.full()

NUM_GROUPS = 3

def L1Q1Initializator(genome, **args):
    genome.clearString()
    genome_list = [1]*NUM_GROUPS + [0]* (len(genome)-NUM_GROUPS)
    shuffle(genome_list)
    for i in genome_list:
        genome.append(i)

    assert genome.genomeString.count(1) == NUM_GROUPS

def L1Q1CrossoverOX(genome, **args):
    """ The OX Crossover of L1Q1 """

    def get_ones_index(l):
        ll = []
        for index, value in enumerate(l):
            if value == 1:
                ll.append(index)
        return ll


    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)

    set_of_ones = set(get_ones_index(gMom.genomeString) + get_ones_index(gDad.genomeString))

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()

        sister.genomeString = [0] * listSize
        for index in sample(set_of_ones,NUM_GROUPS):
            sister.genomeString[index] = 1
    
    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()

        brother.genomeString = [0] * listSize
        for index in sample(set_of_ones,NUM_GROUPS):
            brother.genomeString[index] = 1

    try:
        assert sister.genomeString.count(1) == NUM_GROUPS
        assert brother.genomeString.count(1) == NUM_GROUPS
    except:
        print set_of_ones
        print sister.genomeString
        print brother.genomeString
        raise
    return (sister, brother)

def distance(point_a,point_b):
    return sqrt(reduce(lambda a,b: a+b, map(lambda a,b: (a-b) * (a-b), point_a, point_b), 0))

def fitness_func(genome):
    score = 0.0

    medoid = [pontos[i] for (i,j) in enumerate(genome) if  j == 1]

    l = []

    for point in pontos:
        try:
            l.append(min(map(distance, medoid, [point]*NUM_GROUPS)))
        except:
            print genome,medoid,[point]*NUM_GROUPS

    return 1000.0/reduce(lambda a,b: a+b, l, 0.0)


pontos = open("dados_ECC1.txt").read().split('\n')
pontos = [map(float,i.split(' ')) for i in pontos if i <> '']

sqlite_adapter = DBAdapters.DBSQLite(identify="l1q1_1", resetDB=False)

genome = G1DBinaryString.G1DBinaryString(60)
genome.initializator.set(L1Q1Initializator)
genome.mutator.set(Mutators.G1DBinaryStringMutatorSwap)
genome.crossover.set(L1Q1CrossoverOX)
genome.evaluator.set(fitness_func)

ga = GSimpleGA.GSimpleGA(genome)
ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
ga.selector.set(Selectors.GTournamentSelector)
ga.setPopulationSize(100)
ga.setGenerations(200)
ga.setCrossoverRate(0.9)
ga.setMutationRate(0.02)
ga.setDBAdapter(sqlite_adapter)

ga.evolve(freq_stats = 20)

print ga.bestIndividual()

medoides = []

medoides = [pontos[i] for (i,j) in enumerate(ga.bestIndividual().genomeString) if j == 1]

grupo = defaultdict(list)

for ponto in pontos:
    grupo[min(map(lambda x: (x[0], distance(ponto, x[1])), zip(range(len(medoides)),medoides)), key = lambda x: x[1])[0]].append(ponto)

get_x = lambda x: x[0]
get_y = lambda x: x[1]

print fitness_func(ga.bestIndividual().genomeString)
print medoides

pylab.plot(map(get_x,grupo[0]),map(get_y,grupo[0]), 'b<', medoides[0][0],medoides[0][1],'bs',\
           map(get_x,grupo[1]),map(get_y,grupo[1]), 'r>', medoides[1][0],medoides[1][1],'rs',\
           map(get_x,grupo[2]),map(get_y,grupo[2]), 'g^', medoides[2][0],medoides[2][1],'gs',\
          )
pylab.show()
