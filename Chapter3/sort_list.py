import math
import random


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
        
        return longest_sequence()
        
    def __lt__(self,e):
        return self.fitness<e.fitness
    
    def mutate(self):
        i=random.randrange(0,len(self.elements))
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
    
    def local_search(self,neighbors):
        current=self
        current.compute_fitness()
        it=0
        while True:
            if current.is_sorted():break
            it+=1
            if it%25==0:print(it,current.fitness)
            best_neighbor=min([current.clone().mutate() for i in range(neighbors)])
            if current>best_neighbor:
                current=best_neighbor
            else:
                break
        return current

    def local_search_2nd_chance(self,neighbors,max_iter):
        print("Local search 2nd chance")
        current=self
        current.compute_fitness()
        for it in range(max_iter):
            if it%25==0:print(it,current.fitness)
            best_neighbor=min([current.clone().mutate() for _ in range(neighbors)])
            if current>best_neighbor:
                current=best_neighbor
            if current.fitness==0:
                current.compute_fitness()
            if current.is_sorted():
                break
        return current
    
    def simulated_annealing(self,neighbors,max_iter,T=20,alpha=0.95):
        print("Simulated annealing")
        current=self
        best=current
        current.compute_fitness()
        for it in range(max_iter):
            if it%25==0:print(f"{it} {best.fitness}")
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
                break
            T*=alpha
        return best
    
l=Sorting_List(100)
l.generate_problem()
lp=Sorting_List(0,False)
lp.elements=l.elements[:]
print(f"Initial problem: {l}")
print(f"Solution is {l.local_search(20)}\n")
print(f"Solution is {l.local_search_2nd_chance(20,2000)}\n")
print(f"Solution is {lp.simulated_annealing(20,2000)}\n")
