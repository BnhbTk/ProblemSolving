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
        return np.abs(a-(t1.area()+t2.area()+t3.area()))<1e-4


_, ax = plt.subplots(figsize=(6, 6))
p=Point(50,50)
t=p.generate_equilateral_triangle(40)
p.draw(ax)
t.draw(ax)
plt.show()
