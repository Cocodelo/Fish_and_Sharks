
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
        self.anim = None
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
                r=rd.randint(0,9)
                if r==0:
                    self.grid[i][j]=Shark(i,j)
                    self.animals.append(self.grid[i][j])
                elif r>6:
                    self.grid[i][j]=Fish(i,j)
                    self.animals.append(self.grid[i][j])
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
         self.anim = animation.ArtistAnimation(fig,mapsList,interval=100,blit=True,repeat=False)
         plt.show()
         
    def surroundings(self,pos):
        d={0:[0,[]],1:[0,[]],2:[0,[]]}
        l=[[pos[0],pos[1]-1],[pos[0],pos[1]+1],[pos[0]-1,pos[1]],[pos[0]+1,pos[1]]]
        # if indice au bord, alors on remplace les valeurs de la liste par les trucs qui vont bien!
        if pos[0]==0 :
            l[2]=[self.width-1,pos[1]]
        if pos[0]==self.width-1:
            l[3]=[0,pos[1]]
        if pos[1]==0 :
            l[0]=[pos[0],self.width-1]
        if pos[1]==self.width-1:
            l[1]=[pos[0],0]
            
        for i in l:
            if self.grid[i[0]][i[1]]==None:
                d[0][0]+=1
                d[0][1].append(i)
            else:
                for j in range(0,3):
                    if self.grid[i[0]][i[1]].num==j:
                        d[j][0]+=1
                        d[j][1].append(i)
        return d
    
    def removeDeads(self):
        c=0
        for i in self.animals:
            if type(i)==Shark and i.energy==0:
                i.alive=False
            if not i.alive:
                self.animals.pop(c)
                self.grid[i.pos[0]][i.pos[1]]=None
            c+=1
                
                # for i in range(0,len(self.animals)):
            #    if not self.animals[i].alive:
            #      self.animals.pop(i) 
            

    def tick(self):
        rd.shuffle(self.animals)
        for i in range(0,len(self.animals)):
            if self.animals[i].alive:
                self.animals[i].rep+=1
                d=self.surroundings(self.animals[i].pos)
                if type(self.animals[i])==Shark:
                    if d[1][0]>0:
                        self.animals[i].move(self,d,1)
                        self.animals[i].energy+=3
                        if self.animals[i].energy>6:
                            self.animals[i].energy=6
                        self.animals[i].energy-=1
                        if self.animals[i].energy==0:
                            self.animals[i].alive=False
                    else:
                        self.animals[i].move(self,d,0)
                        self.animals[i].energy-=1
                        if self.animals[i].energy==0:
                            self.animals[i].alive=False
                elif self.surroundings(self.animals[i].pos)[0][0]!=0:
                    self.animals[i].move(self,d,0)
        self.removeDeads()
                
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
        self.pos=(x,y)
        self.rep=0
        self.alive=True

    def reproduce(self,ocean,oldpos):
        self.rep=0
        ocean.grid[oldpos[0]][oldpos[1]]=type(self)(oldpos[0],oldpos[1])
        ocean.animals.append(ocean.grid[oldpos[0]][oldpos[1]])

    def move(self,ocean,d,cellType):
        if d[cellType][0]==0:
            pass
        else:
            a=rd.randint(0,d[cellType][0]-1)
            oldpos=self.pos
            if type(self)==Shark and type(ocean.grid[d[cellType][1][a][0]][d[cellType][1][a][1]])==Fish:
                ocean.grid[d[cellType][1][a][0]][d[cellType][1][a][1]].alive=False
                
            ocean.grid[d[cellType][1][a][0]][d[cellType][1][a][1]]=self
            self.pos=(d[cellType][1][a])
            
            ocean.grid[oldpos[0]][oldpos[1]]=None
            if self.rep>=self.reproductionTreshold:
                self.reproduce(ocean,oldpos)




###

class Fish(Animal):


    num = 1

    reproductionTreshold = 4

###

class Shark(Animal):
    
    maximum_energy=6
    energy_start=3
    num = 2

    reproductionTreshold = 12
    def __init__(self,x,y):

        self.energy=self.energy_start
        super().__init__(x,y)


nbIter = 200
atlantic = Ocean()
atlantic.initialize()
for _ in range(nbIter):
    atlantic.tick()
atlantic.show()
fishes = [atlantic.animalCount[i][0] for i in range(20,nbIter+1)]
sharks = [atlantic.animalCount[i][1] for i in range(20,nbIter+1)]

# call the function LV only after running the simulation

def LV():
    x = [i for i in range(20,nbIter+1)]
    plt.plot(x,fishes,color='green')
    plt.plot(x,sharks,color='blue')
    plt.show()
#LV()

print("frames:", len(atlantic.states), "animals:", len(atlantic.animals), "last count:", atlantic.animalCount[-1] if atlantic.animalCount else None)


 # textual grid
#affiche un graph vierge, wtf
