# The MIT License
# 
# Copyright (c) 2011 John Svazic
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A python script that demonstrates a simple "Hello, world!" application using
genetic algorithms.

@author: John Svazic
"""

from random import (random, randint)

__all__ = ['Chromosome', 'Population']

class Chromosome(object):
    """
    This class is used to define a chromosome for the gentic algorithm 
    simulation.  
       
    This class is essentially nothing more than a container for the details
    of the chromosome, namely the gene (the string that represents our 
    target string) and the fitness (how close the gene is to the target 
    string).
       
    Note that this class is immutable.  Calling mate() or mutate() will 
    result in a new chromosome instance being created.
    """

    __target_gene = "Hello, world!"
    
    def __init__(self, gene):
        self._gene = gene
        self._fitness = Chromosome._updateFitness(gene)
    
    @property
    def gene(self):
        """
        Method used to retrieve the gene for the chromosome.
        """
        return self._gene

    @property        
    def fitness(self):
        """
        Method used to retrieve the fitness value of the chromosome.
        """
        return self._fitness
        
    def mate(self, mate):
        """
        Method used to mate the chromosome with another chromosome, 
        resulting in a new chromosome being returned.
        """
        pivot = randint(0, len(self.gene) - 1)
        gene1 = self.gene[0:pivot] + mate.gene[pivot:]
        gene2 = mate.gene[0:pivot] + self.gene[pivot:]
        
        return Chromosome(gene1), Chromosome(gene2)
    
    def mutate(self):
        """
        Method used to generate a new chromosome based on a change in a 
        random character in the gene of this chromosome.  A new chromosome 
        will be created, but this original will not be affected.
        """
        gene = list(self.gene)
        delta = randint(0, 89) + 32
        idx = randint(0, len(gene) - 1)
        gene[idx] = chr((ord(gene[idx]) + delta) % 122)
        
        return Chromosome(''.join(gene))

    @staticmethod            
    def _updateFitness(gene):
        """
        Helper method used to return the fitness for the chromosome based
        on its gene.
        """
        fitness = 0
        for a, b in zip(gene, Chromosome.__target_gene):
            fitness += abs(ord(a) - ord(b))
            
        return fitness
        
    @staticmethod
    def genRandom():
        """
        A convenience method for generating a random chromosome with a random
        gene.
        """
        gene = []
        for x in range(len(Chromosome.__target_gene)):
            gene.append(chr(randint(0, 89) + 32))
                
        return Chromosome(''.join(gene))
        
class Population(object):
    """
    A class representing a population for a genetic algorithm simulation.
    
    A population is simply a sorted collection of chromosomes 
    (sorted by fitness) that has a convenience method for evolution.  This
    implementation of a population uses a tournament selection algorithm for
    selecting parents for crossover during each generation's evolution.
    
    Note that this object is mutable, and calls to the evolve()
    method will generate a new collection of chromosome objects.
    """
    
    __tournamentSize = 3
    
    def __init__(self, size=1024, crossover=0.8, elitism=0.1, mutation=0.03):
        self._elitism = elitism
        self._mutation = mutation
        self._crossover = crossover
        
        buf = []
        for i in range(size): buf.append(Chromosome.genRandom())
        self._population = list(sorted(buf, key=lambda x: x.fitness))
    
    @property
    def population(self):
        """
        Method to retrieve a copy of the population.  Note that this is
        a copy of the collection of chromosomes in the Populatin object, not
        a direct reference to the collection.
        """
        return self._population[:]

    @property        
    def elitism(self):
        """
        Method to retrieve the elitism rate of the population.
        """
        return self._elitism

    @property
    def mutation(self):
        """
        Method to retrieve the mutation rate of the population.
        """
        return self._mutation

    @property    
    def crossover(self):
        """
        Method to retrieve the crossover rate of the population.
        """
        return self._crossover
                    
    def __tournamentSelection(self):
        """
        A helper method used to select a random chromosome from the 
        population using a tournament selection algorithm.
        """
        best = self.population[randint(0, len(self._population) - 1)]
        for i in range(Population.__tournamentSize):
            cont = self._population[randint(0, len(self._population) - 1)]
            if (cont.fitness < best.fitness): best = cont
                    
        return best

    def __selectParents(self):
        """
        A helper method used to select two parents from the population using a
        tournament selection algorithm.
        """
                    
        return (self.__tournamentSelection(), self.__tournamentSelection())
        
    def evolve(self):
        """
        Method to evolve the population of chromosomes.
        """
        size = len(self._population)
        idx = int(round(size * self._elitism))
        buf = self._population[0:idx]
        
        while (idx < size):
            if random() <= self._crossover:
                (p1, p2) = self.__selectParents()
                children = p1.mate(p2)
                for c in children:
                    if random() <= self._mutation:
                        buf.append(c.mutate())
                    else:
                        buf.append(c)
                idx += 2
            else:
                if random() <= self._mutation:
                    buf.append(self._population[idx].mutate())
                else:
                    buf.append(self._population[idx])
                ++idx
        
        self._population = list(sorted(buf[0:size], key=lambda x: x.fitness))

if __name__ == "__main__":
	maxGenerations = 16384
	pop = Population(size=2048, crossover=0.8, elitism=0.1, mutation=0.3)

	for i in range(1, maxGenerations + 1):
		print "Generation %d: %s" % (i, pop.population[0].gene)
		if pop.population[0].fitness == 0: break
		else: pop.evolve()
	else:
		print "Maximum generations reached without success."