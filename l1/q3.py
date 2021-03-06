from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Initializators
from pyevolve import Crossovers
from pyevolve import Mutators
from pyevolve import DBAdapters

from itertools import combinations
from math import sqrt
from collections import defaultdict

import pylab

import psyco
psyco.full()

def distance(point_a,point_b):
    return sqrt(reduce(lambda a,b: a+b, map(lambda a,b: (a-b) * (a-b), point_a, point_b), 0))

def fitness_func(genome):
    score = 0.0

    intra = 0.0
    inter = 0.0

    for (grupo_a,ponto_a),(grupo_b,ponto_b) in combinations(zip(genome.genomeList,pontos), 2):
        if grupo_a == grupo_b: intra += distance(ponto_a,ponto_b)
        else                 : inter += distance(ponto_a,ponto_b)

    return inter/intra


pontos = open("dados_ECC1.txt").read().split('\n')
pontos = [map(float,i.split(' ')) for i in pontos if i <> '']

sqlite_adapter = DBAdapters.DBSQLite(identify="l1q3_1", resetDB=True)

genome = G1DList.G1DList(60)
genome.initializator.set(Initializators.G1DListInitializatorInteger)
genome.setParams(rangemin=0, rangemax=2)
genome.mutator.set(Mutators.G1DListMutatorIntegerRange)
genome.crossover.set(Crossovers.G1DListCrossoverUniform)
genome.evaluator.set(fitness_func)

ga = GSimpleGA.GSimpleGA(genome)
ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
#ga.selector.set(Selectors.GTournamentSelector)
ga.setPopulationSize(100)
ga.setGenerations(200)
ga.setCrossoverRate(0.9)
ga.setMutationRate(0.02)
ga.setDBAdapter(sqlite_adapter)

ga.evolve(freq_stats = 20)

print ga.bestIndividual()

exit

grupos = defaultdict(list)

for grupo,ponto in zip(ga.bestIndividual().genomeList,pontos):
    grupos[grupo].append(ponto)

get_x = lambda x: x[0]
get_y = lambda x: x[1]

print len(grupos[0]), len(grupos[1]), len(grupos[2])

pylab.plot(map(get_x,grupos[0]),map(get_y,grupos[0]), 'b<', \
           map(get_x,grupos[1]),map(get_y,grupos[1]), 'r>', \
           map(get_x,grupos[2]),map(get_y,grupos[2]), 'gv', \
          )
pylab.show()
