from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import DBAdapters
from random import shuffle
from math import sqrt
from random import uniform

from collections import defaultdict

import pylab

import psyco
psyco.full()

NUM_GROUPS = 3

def L1Q2ArithCrossover(genome, **args):
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
   
    x_element = uniform(-0.1,1.1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        sister.genomeList = map(lambda x,y: (1-x_element)*x+x_element*y, gMom.genomeList, gDad.genomeList)

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList = map(lambda x,y: (1-x_element)*x+x_element*y, gDad.genomeList, gMom.genomeList)

    return (sister, brother)

def distance(point_a,point_b):
    return sqrt(reduce(lambda a,b: a+b, map(lambda a,b: (a-b) * (a-b), point_a, point_b), 0))

def fitness_func(genome):
    score = 0.0

    centroid = [[i,j] for (i,j) in zip(genome.genomeList[::2],genome.genomeList[1::2])]

    l = []

    for point in pontos:
        try:
            l.append(min(map(distance, centroid, [point]*NUM_GROUPS)))
        except:
            print genome,medoid,[point]*NUM_GROUPS

    return 1.0/reduce(lambda a,b: a+b, l, 0.0)


pontos = open("dados_ECC1.txt").read().split('\n')
pontos = [map(float,i.split(' ')) for i in pontos if i <> '']

sqlite_adapter = DBAdapters.DBSQLite(identify="l1q2_6", resetDB=False)

genome = G1DList.G1DList(6)
genome.setParams(rangemin=1.0, rangemax=7.0)
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
genome.crossover.set(L1Q2ArithCrossover)
genome.evaluator.set(fitness_func)

ga = GSimpleGA.GSimpleGA(genome)
ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
#ga.selector.set(Selectors.GTournamentSelector)
ga.setPopulationSize(100)
ga.setGenerations(200)
ga.setCrossoverRate(0.9)
ga.setMutationRate(0.02)
ga.setDBAdapter(sqlite_adapter)

ga.evolve(freq_stats = 1)

winner = ga.bestIndividual()
print winner

centroids = [[i,j] for (i,j) in zip(winner.genomeList[::2],winner.genomeList[1::2])]

grupo = defaultdict(list)

for ponto in pontos:
    grupo[min(map(lambda x: (x[0], distance(ponto, x[1])), zip(range(len(centroids)),centroids)), key = lambda x: x[1])[0]].append(ponto)

get_x = lambda x: x[0]
get_y = lambda x: x[1]

print len(grupo[0]), len(grupo[1]), len(grupo[2])

pylab.plot(map(get_x,grupo[0]),map(get_y,grupo[0]), 'b.', centroids[0][0],centroids[0][1],'bo',\
           map(get_x,grupo[1]),map(get_y,grupo[1]), 'r.', centroids[1][0],centroids[1][1],'ro',\
           map(get_x,grupo[2]),map(get_y,grupo[2]), 'g.', centroids[2][0],centroids[2][1],'go',\
#          map(get_x,grupo[3]),map(get_y,grupo[3]), 'm.', centroids[3][0],centroids[3][1],'mo',\
#          map(get_x,grupo[4]),map(get_y,grupo[4]), 'y.', centroids[4][0],centroids[4][1],'yo',\
#          map(get_x,grupo[5]),map(get_y,grupo[5]), 'k.', centroids[5][0],centroids[5][1],'ko'\
          )
pylab.show()
