import numpy as np
from random import randint, uniform

chromsize=243

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

def son(p1,p2):
    
    son=[]
    for i in range(p1):
        j=randint(1,2)
        #The son's attributes are randomly selected
        if(j==1):
            son.append(p1[i])
        else:
            son.append(p2[i])
    return np.array(son)

def mutate(subj):
    
    mutated_subject=[]
    for f in subj:
        odds=randint(0,19)
        if(odds==0):
            gene=uniform(-1,1)
            mutated_sunject.append(gene)
        else:
            mutated_subject.append(f)
    return np.array(mutated_subject)

def mutate_pop(pop):
    
    mutated_pop=[]
    for s in pop:
        odds=randint(0,9)
        if(odds==0):
            mutated_pop.append(mutate(s))
        else:
            mutated_pop.append(s)
    return np.array(mutated_pop)

def breed(population):
    
    sorted_pop=sorted(population,key=lambda x: x[2],reverse=True)
    most_adapted=sorted_pop[:10]
    next_pop=[]
    
    while(len(next_pop)<100):
        #selecting the parents
        p1=randint(0,9)
        p2=randint(0,9)
        next_pop.append(son(most_adapted[p1],most_adapted[p2]))
    
    return np.array(next_pop)

def name_pop(pop,gen):
    
    named_pop=[]
    i=0
    base_name="Gen"+str(gen)+"_chrom"
    for s in pop:
        named_pop.append([(base_name+str(i)), s])
    return named_pop

class SubjectPool:
    
    def __intit__(self):
        
        #List of the subjects of the form [ChromName, Chromossome]
        self.population=CreateInitalPopulation()
        self.iterator=0
        self.generation=1
        
    def set_fitness(fitness):
        
        #Sets the fitness of a given subject indexed by iterator
        self.population[self.iterator].append(fitness)
        self.iterator+=1
        
    def get_subj():
        
        if(self.iterator==100):
            self.generation+=1
            new_pop=breed(self.population)
            new_pop=mutate_pop(new_pop)
            new_pop=name_pop(new_pop,self.generation)
            self.population=new_pop
            self.iterator=0
        return self.population[self.iterator]