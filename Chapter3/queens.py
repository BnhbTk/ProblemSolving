from __future__ import annotations
import copy
import math
import random


class Queens:
    def __init__(self,nb_queen,init=True):
        if init:
            self.positions = list(range(nb_queen))
            random.shuffle(self.positions)
        self.fitness=0
    
    def __str__(self) -> str:
        mat="\n".join(["".join(["[♛]" if p==i else "[ ]"  for i in range(len(self.positions))]) for p in self.positions])
        return f"{mat}\n{self.positions}\n{self.fitness}"
    
    def __lt__(self,other:Queens) -> bool:
        return self.fitness > other.fitness
    
    def mutate(self,pm):
        n = len(self.positions)
        for i in range(n):
            if random.random()<pm:
                a=random.randint(0,n-1)
                while True:
                    b=random.randint(0,n-1)
                    if a!=b:break
                self.positions[a],self.positions[b]=self.positions[b],self.positions[a]
        return self

    def copy(self):
        return copy.deepcopy(self)

    def hill_climbing_2nd_chance(self,pm):
        current=self
        current.compute_fitness()
        for j in range(800):
            if j%80==0:print(j,current.fitness)
            next_hope=current.copy().mutate(pm)
            next_hope.compute_fitness()
            for i in range(1,10):
                candidate=current.copy().mutate(pm)
                candidate.compute_fitness()
                if next_hope.fitness<candidate.fitness:
                    next_hope=candidate
            if next_hope.fitness>current.fitness:
                current=next_hope
            if current.fitness==len(self.positions):
                break
        return current.fitness

    def simulated_annealing(self,pm,T,a):
        current=self
        current.compute_fitness()
        best=current
        for j in range(800):
            if j%80==0:print(j,best.fitness)
            next_hope=current.copy().mutate(pm)
            next_hope.compute_fitness()
            for i in range(1,10):
                candidate=current.copy().mutate(pm)
                candidate.compute_fitness()
                if next_hope.fitness<candidate.fitness:
                    next_hope=candidate
            if next_hope.fitness>current.fitness:
                current=next_hope
            else:
                p=math.exp((next_hope.fitness-current.fitness)/T)
                if random.random()<p:
                    current=next_hope
            if current.fitness>best.fitness:
                best=current
            if best.fitness==len(self.positions):
                break
            T=T*a
        return best.fitness

inst=Queens(8)
print(inst)
