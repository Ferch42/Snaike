import numpy as np



def CreateChromossome(size):
    return np.random.uniform(-1,1,[size])

def CreateInitialPopulation():
    #Creates a initial population of 100
    pop=[]
    
    #The list of population is composed of itens of the form [ChromName, Chromossome]
    for i in range(100):
        chromname='Gen1_chrom'+str(i)
        pop.append([chromname,CreateChromossome(chromsize)])
        
    return pop