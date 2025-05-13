from __future__ import annotations
import random
import sys
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def generate_equilateral_triangle(self,a:float) -> Triangle:
        p1=Point(self.x,self.y+np.sqrt(3)*a/3)
        p2=Point(self.x+a/2,self.y-np.sqrt(3)*a/6)
        p3=Point(self.x-a/2,self.y-np.sqrt(3)*a/6)
        
        return Triangle(p1,p2,p3)
    
    def __repr__(self):
        return f"{self.x},{self.y}"
    
    def draw(self,ax):
        ax.scatter([self.x],[self.y],color='r',s=4)

class Triangle:
    def __init__(self,p1:Point,p2:Point,p3:Point):
        self.p1=p1
        self.p2=p2
        self.p3=p3
    
    def area(self):
        return np.abs(self.p1.x*(self.p2.y-self.p3.y)+self.p2.x*(self.p3.y-self.p1.y)+self.p3.x*(self.p1.y-self.p2.y))/2
    
    def draw(self,ax):
        coords=np.array([[self.p1.x,self.p1.y],[self.p2.x,self.p2.y],[self.p3.x,self.p3.y]])
        poly=Polygon(coords,alpha=0.4,edgecolor="blue",linewidth=1)
        ax.add_patch(poly)
        plt.ylim(0,100)
        plt.xlim(0,100)
    
    def contains(self,p:Point):
        t1=Triangle(self.p1,self.p2,p)
        t2=Triangle(self.p1,self.p3,p)
        t3=Triangle(self.p2,self.p3,p)
        a=self.area()
        return np.abs(a-(t1.area()+t2.area()+t3.area()))<1e-6

class Covering:
    pts=None
    points=None
    triangles=None
    side=15
    
    def prepare_data():
        Covering.points=[Point(x,y) for x,y in Covering.pts]
        Covering.triangles=[p.generate_equilateral_triangle(Covering.side) for p in Covering.points]
        
    def __init__(self,init=True):
        if init:
            self.solution=np.random.randint(low=0,high=2,size=len(Covering.pts))
        
    def draw(self):
        _, ax = plt.subplots(figsize=(6, 6))
        for i,cds in enumerate(pts):
            p=Point(cds[0],cds[1])
            if self.solution[i]:
                Covering.triangles[i].draw(ax)
            p.draw(ax)
        plt.show()
    
    def compute_fitness(self):
        nb=0
        candidates=[Covering.triangles[i] for i in range(len(Covering.triangles)) if self.solution[i]]
        for i in range(len(Covering.points)):
            for t in candidates:
                if t.contains(Covering.points[i]):
                    nb+=1
                    break
        self.fitness=self.solution.sum()-nb
        self.nb=nb
        self.sm=self.solution.sum()
        return self.fitness
    
    def __str__(self):
        return f"{self.fitness}: {self.nb}, {self.sm}"
    
    def clone(self):
        res=Covering(False)
        res.solution=np.array(self.solution)
        return res

    def mutate(self,pm=0.05):
        for i in range(self.solution.shape[0]):
            if np.random.random()<pm:
                self.solution[i]=1-self.solution[i]
        self.compute_fitness()
        return self
    
    def __lt__(self,obj):
        return self.fitness<obj.fitness
    
    def crossover(self,other):
        child1=Covering(False)
        child2=Covering(False)
        pt=1+np.random.randint(len(self.solution)-1)
        child1.solution=np.concatenate((self.solution[:pt],other.solution[pt:]))
        child2.solution=np.concatenate((other.solution[:pt],self.solution[pt:]))
        return child1,child2
    
    def simulated_annealing(self,T=50,a=0.95):
        self.compute_fitness()
        current=self
        best=current
        for i in range(1000):
            best_neighbor=min([current.clone().mutate() for _ in range(10)])
            print(i,">>",best)
            if current>best_neighbor:
                current=best_neighbor
            else:
                r=np.exp((current.fitness-best_neighbor.fitness)/T)
                if np.random.random()<r:
                    current=best_neighbor
            if best>current:
                best=current
            T*=a
        return current

class GeneticAlgorithm:
    def __init__(self,pop_size):
        self.population=[Covering() for _ in range(pop_size)]
        for q in self.population:
            q.compute_fitness()
    
    def select(self,method):
        res=[]
        n=len(self.population)
        if method=="elitist":
            return self.population
        elif method=="tournoi":
            k=6
            for i in range(n):
                nb=0
                k=6
                pool=[]
                while nb<k:
                    c=np.random.choice(self.population)
                    if c not in pool:
                        pool.append(c)
                        nb+=1
                res.append(min(pool))
        elif method=="wheel":
            weights=[np.abs(r.fitness) for r in self.population]
            res=random.choices(self.population,weights,k=len(self.population))
        else:
            raise ValueError(f"Unknown selection method {method}")
        return res
    
    def generation(self,pc,pm,selection):
        parents=self.select(selection)
        children:list[Covering]=[]
        for i in range(len(parents)//2):
            if random.random()<pc:
                child1,child2=parents[2*i].crossover(parents[2*i+1])
                children.append(child1)
                children.append(child2)
                child1.mutate(pm)
                child2.mutate(pm)
                

        for i in range(len(children)//2):
            children[i].compute_fitness()
            self.population[self.initsize-i-1]=children[i]
        
        return self.population[0]
    
    def execute(self,iterations,pc,pm,selection):
        self.initsize=len(self.population)
        
        for i in range(iterations):
            self.population.sort()
            best=self.generation(pc,pm,selection)
            print(i,best)
        return best

pts=[
    [0.21785146,32.80884325],
    [36.53983575,18.85454466],
    [30.22558699,40.47690186],
    [18.24973109,92.01706988],
    [58.08376113,92.00152543],
    [46.93621006,80.97613966],
    [47.32211679,91.18953057],
    [40.65971946,14.94515933],
    [97.7445341,62.9737585,],
    [67.15084079,32.35608877],
    [68.75175516,54.20477561],
    [91.80634184,94.35959023],
    [45.40857899,61.2605084,],
    [99.48086417,52.49122315],
    [48.93285306,62.77433716],
    [26.90344815,72.73694627],
    [60.28518974,34.06750296],
    [21.23856624,37.76163464],
    [85.79582818,41.13272287],
    [81.11078688,62.25071194],
    [83.08482713,84.81411278],
    [35.2874055,29.80941103],
    [49.66321866,35.67015919],
    [70.37347844,76.05067313],
    [91.9348889,81.85162595],
    [73.46612228,40.7045268,],
    [38.3556454,84.28602823],
    [5.21712579,18.30743315],
    [75.72162521,54.12073958],
    [26.72551212,68.47890848],
    [81.41504844,97.70267505],
    [19.59272594,53.29613031],
    [82.88070594,79.33406044],
    [42.97770388,39.39407873],
    [84.12304215,32.42914694],
    [88.1637349,95.53768435],
    [58.76495944,25.67892065],
    [62.05423696,83.28110411],
    [60.85664933,4.40774533],
    [19.72387992,12.50406704],
    [85.68495556,64.60429362],
    [45.40271382,25.43267343],
    [88.4323,75.45146857],
    [18.52167173,57.17151834],
    [96.87211957,79.17682143],
    [90.88110424,60.7095252,],
    [2.85430696,54.40447172],
    [99.91234515,74.4014438,],
    [73.94323878,97.65276912],
    [37.71273758,5.55845728]
]

Covering.pts=pts
Covering.side=30
Covering.prepare_data()

ga=GeneticAlgorithm(40)
sol=ga.execute(800,0.95,0.05,"wheel")
sol.draw()
plt.show()
