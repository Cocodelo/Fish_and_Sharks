import random as rd
import matplotlib.pyplot as plt
from matplotlib import animation

def copyMat(m):
    return [[m[i][j] for j in range(len(m[0]))] for i in range(len(m))]

colorTable = [(0, 0, 102),(102, 255, 51),(0, 102, 255)]

class Ocean :   

    def __init__(self,width=50,height=50):
        self.width,self.height = width,height
        self.grid = [[None]*height for _ in range(width)]
        self.animals = []
        self.states = []
        self.animalCount = []
        # do not change the names of the attributes or the show function won't work

    def __str__(self):
        def conv(v):
            if v == None : return "0"
            else : return str(v.num)
        res = ""
        for i in range(self.width):
            res += "| "
            for j in range(self.height):
                res += conv(self.grid[i][j]) + " "
            res += "|\n"
        return res

    def initialize(self):
        for i in range(0,self.height):
            for j in range(0,self.width):
                if rd.randint(0,9)<=0:
                    self.grid[i][j]=Shark(1,2)
                    self.animals.append(Shark)
                elif rd.randint(0,9)>=6:
                    self.grid[i][j]=Fish(1,2)
                    self.animals.append(Fish)
        self.states.append(copyMat(self.grid))
        self.animalCount.append(self.count())

    def show(self):
        # used for the animation do not touch !
        fig = plt.figure(1)
        mapsList = []
        for k in range(len(self.states)):
            for i in range(self.width):
                for j in range(self.height):
                    if self.states[k][i][j] == None :
                        self.states[k][i][j] = colorTable[0]
                    else :
                        self.states[k][i][j] = colorTable[self.states[k][i][j].num]
            img = plt.matshow(self.states[k],fignum=1)
            mapsList.append([img])
        anim = animation.ArtistAnimation(fig,mapsList,interval=100,blit=True,repeat=False)
        plt.show()

    def surroundings(self,pos):
        d={0:[0,[]],1:[0,[]],2:[0,[]]}
        if self.grid[pos[0]][pos[1]-1]==None:
            d[0][0]+=1
            d[0][1].append((pos[0],pos[1]-1))
        else:
                for i in range(0,3):
                    if self.grid[pos[0]][pos[1]-1].num==i:
                        d[i][0]+=1
                        d[i][1].append((pos[0],pos[1]-1))
        
        if self.grid[pos[0]][pos[1]+1]==None:
            d[0][0]+=1
            d[0][1].append((pos[0],pos[1]+1)) 
        else:
            for i in range(0,3):
                if self.grid[pos[0]][pos[1]+1].num==i:
                    d[i][0]+=1
                    d[i][1].append((pos[0],pos[1]+1))
        
        if self.grid[pos[0]-1][pos[1]]==None:
            d[0][0]+=1
            d[0][1].append((pos[0]-1,pos[1])) 
        else:
            for i in range(0,3):
                if self.grid[pos[0]-1][pos[1]].num==i:
                    d[i][0]+=1
                    d[i][1].append((pos[0]-1,pos[1]))
        
        if self.grid[pos[0]+1][pos[1]]==None:
            d[0][0]+=1
            d[0][1].append((pos[0]+1,pos[1])) 
        else:
            for i in range(0,3):
                if self.grid[pos[0]+1][pos[1]].num==i:
                    d[i][0]+=1
                    d[i][1].append((pos[0]+1,pos[1]))
        return d
                

    def removeDeads(self):
        pass
        # complete here (remove pass)

    def tick(self):
        rd.shuffle(self.animals)
        # complete here
        self.states.append(copyMat(self.grid))
        self.animalCount.append(self.count())

    def count(self):
    # used for plotting the number of fishes and sharks
        nbF = 0
        nbS = 0
        for animal in self.animals :
            if animal.num == 1 :
                nbF += 1
            else :
                nbS += 1
        return nbF,nbS
    
class Animal :

    def __init__(self,x,y):
        pass
        # complete here (remove pass)

    def move(self,ocean,d,cellType):
        pass
        # complete here (remove pass)

    def reproduce(self,ocean,oldpos):
        pass
        # complete here (remove pass)

###

class Fish(Animal):

    num = 1

    reproductionTreshold = 4

###

class Shark(Animal):

    num = 2

    reproductionTreshold = 12


nbIter = 100

atlantic = Ocean()
atlantic.initialize()
for _ in range(nbIter):
    atlantic.tick()
atlantic.show()
