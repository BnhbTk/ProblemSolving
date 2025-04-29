# This is un update of the first version, now with the three fitness functions

import math
import random
import sys


class Sorting_List:
    def __init__(self,n,init=True):
        if init:
            self.elements=list(range(n))
        else:
            self.elements=[]
    
    def generate_problem(self):
        random.shuffle(self.elements)
    
    
    def is_sorted(self):
        for i in range(1,len(self.elements)):
            if self.elements[i-1]>self.elements[i]:return False
        return True

    def __str__(self):
        return f"{'Sorted' if self.is_sorted() else 'Unsorted'}"
    
    def compute_fitness(self):
        def penalty():
            sz=len(self.elements)
            m=0
            for i in range(sz):
                m+=len([1 for x in self.elements[:i] if x>self.elements[i]])+len([1 for x in self.elements[i+1:] if x<self.elements[i]])
            self.fitness=m
        
        def longest_sequence():
            l=0
            i=1
            cur=1
            sz=len(self.elements)
            while i<sz:
                if self.elements[i-1]<self.elements[i]:
                    cur+=1
                else:
                    if l<cur:l=cur
                    cur=1
                i+=1
            if l<cur:l=cur
            self.fitness=sz-l
        
        def good_orders():
            self.fitness=sum([0 if self.elements[i-1]<=self.elements[i] else 1 for i in range(1,len(self.elements))])
        
        {"pen":penalty,"longest":longest_sequence,"order":good_orders}[Sorting_List.method]()
    
    def __lt__(self,e):
        return self.fitness<e.fitness
    
    def mutate(self):
        pm=0.1#1/len(self.elements)
        for i in range(len(self.elements)):
            if random.random()<pm:
                while True:
                    j=random.randrange(0,len(self.elements))
                    if i!=j:break
                if i < j and self.elements[i]>self.elements[j]:
                    self.elements[i],self.elements[j]=self.elements[j],self.elements[i]
        self.compute_fitness()
        return self
    
    def clone(self):
        res=Sorting_List(0,False)
        res.elements=self.elements[:]
        return res
    
    def local_search(self,neighbors,method):
        current=self
        Sorting_List.method=method
        current.compute_fitness()
        it=0
        while True:
            if current.is_sorted():break
            it+=1
            print(it,current.fitness)
            best_neighbor=min([current.clone().mutate() for i in range(neighbors)])
            if current>best_neighbor:
                current=best_neighbor
            else:
                break
        print("\n")
        return current

    def local_search_2nd_chance(self,neighbors,max_iter,method):
        print("Local search 2nd chance")
        current=self
        Sorting_List.method=method
        current.compute_fitness()
        for it in range(max_iter):
            sys.stdout.write(f"\r{it} {current.fitness}   ")
            sys.stdout.flush()
            best_neighbor=min([current.clone().mutate() for _ in range(neighbors)])
            if current>best_neighbor:
                current=best_neighbor
            if current.fitness==0:
                current.compute_fitness()
            if current.is_sorted():
                sys.stdout.write(f"\r{it} {current.fitness}   ")
                sys.stdout.flush()
                break
        print("")
        return current
    
    def simulated_annealing(self,neighbors,max_iter,method,T=20,alpha=0.95):
        print("Simulated annealing")
        current=self
        best=current
        Sorting_List.method=method
        current.compute_fitness()
        for it in range(max_iter):
            sys.stdout.write(f"\r{it} {best.fitness}   ")
            sys.stdout.flush()
            best_neighbor=min([current.clone().mutate() for _ in range(neighbors)])
            if current>best_neighbor:
                current=best_neighbor
            else:
                r=math.exp((current.fitness-best_neighbor.fitness)/T)
                if random.random()<r:
                    current=best_neighbor
            if current<best:
                best=current
            if best.is_sorted():
                sys.stdout.write(f"\r{it} {best.fitness}   ")
                sys.stdout.flush()
                break
            T*=alpha
        print("")
        return best



    
l=Sorting_List(100)
l.generate_problem()
lp=Sorting_List(0,False)
lp.elements=l.elements[:]
print(f"Initial problem: {l}")
print(f"Solution is {l.local_search_2nd_chance(20,2000,'pen')}\n")
print(f"Solution is {lp.simulated_annealing(20,2000,'pen')}\n")
