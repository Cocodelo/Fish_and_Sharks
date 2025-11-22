
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
        for i in range(0, self.width):
            for j in range(0, self.height):
            #Run through the grid
                r = rd.randint(0, 9)
                if r == 0:
                    self.grid[i][j]=Shark(i, j)
                    self.animals.append(self.grid[i][j])
                    #Create a shark with 10% probability
                elif r > 6:
                    self.grid[i][j]=Fish(i,j)
                    self.animals.append(self.grid[i][j])
                    #Create a Fish with 40% probability
                #Else, leave it as None
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
        l=[[pos[0],pos[1]-1],[pos[0],pos[1]+1],[pos[0]-1,pos[1]],[pos[0]+1,pos[1]]] #Create a list of the four positions around the considered position.
        
        #Tests in case the position is on a edge, and modify the list adequately.
        if pos[0]==0 :
            l[2]=[self.width-1,pos[1]]
        if pos[0]==self.width-1:
            l[3]=[0,pos[1]]
        if pos[1]==0 :
            l[0]=[pos[0],self.width-1]
        if pos[1]==self.width-1:
            l[1]=[pos[0],0]

        #Class correctly the different positins in the dictionary    
        for i in l:
            if self.grid[i[0]][i[1]]==None:
                d[0][0]+=1
                d[0][1].append(i)
            else:
                for j in range(1,3):
                    if self.grid[i[0]][i[1]].num==j:
                        d[j][0]+=1
                        d[j][1].append(i)
        return d
    
    def removeDeads(self):
        #Create a temporary list with only the live animals, then overwrite self.animals with it
        l=[]
        for i in self.grid:
            for j in i:
                if type(j) == Shark and j.energy==0: #Test in case a shark depleted all its energy.
                    j.alive = False
                if j != None and not j.alive:   #Erase dead animals from the grid.
                        self.grid[j.pos[0]][j.pos[1]]=None
                elif j != None and j.alive:
                            l.append(j)
        self.animals=l

            
    def tick(self):
        rd.shuffle(self.animals)
        for i in range(0, len(self.animals)):
            if self.animals[i].alive:                       #Increment the rep value of an animal.
                self.animals[i].rep += 1
                d=self.surroundings(self.animals[i].pos)
                if type(self.animals[i]) == Shark:
                    if d[1][0]>0:
                        self.animals[i].move(self, d, 1)
                        self.animals[i].energy += 3         #Increment the energy value of a shark IF he ate a fish.
                        if self.animals[i].energy > 6:
                            self.animals[i].energy = 6      #Regulate the energy value of sharks
                        self.animals[i].energy -= 1
                        if self.animals[i].energy == 0:
                            self.animals[i].alive = False   #Sets to dead sharks with no energy.
                    elif d[0][0] != 0:                      #Handle the Fishes
                        self.animals[i].move(self, d, 0)    
                        self.animals[i].energy -= 1
                        if self.animals[i].energy == 0:
                            self.animals[i].alive = False
                elif d[0][0] != 0:
                    self.animals[i].move(self, d, 0)
        #print("with deads ", self.count())
        self.removeDeads()
        #print("deads removed ", self.count())
        self.states.append(copyMat(self.grid))
        self.animalCount.append(self.count())
        #print("end tick ", self.count())

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

    def __init__(self, x, y):
        self.pos = (x,y)
        self.rep = 0
        self.alive = True

    def reproduce(self, ocean, oldpos):
            #A method that is used to make a animal reproduce. 
            #First ste rep value to 0 then create a new instance on the grid, and add this instance to the animal list.
            self.rep = 0
            ocean.grid[oldpos[0]][oldpos[1]] = type(self)(oldpos[0],oldpos[1])
            ocean.animals.append(ocean.grid[oldpos[0]][oldpos[1]])

    def move(self, ocean, d, cellType):
        #Move method, used by all animals
        if d[cellType][0] == 0:
            pass
        # Test necessary to check if there is a available cell of the specified type.
        else:
            a = rd.randint(0, d[cellType][0] - 1)
            #Choose a random number that will determine on wich cell does the animal moves.
            oldpos = self.pos
            if type(self) == Shark and type(ocean.grid[d[cellType][1][a][0]][d[cellType][1][a][1]]) == Fish:
                ocean.grid[d[cellType][1][a][0]][d[cellType][1][a][1]].alive = False
            #Kill the Fish in case a Shark is eating it.

            ocean.grid[d[cellType][1][a][0]][d[cellType][1][a][1]] = self
            self.pos=(d[cellType][1][a])
            ocean.grid[oldpos[0]][oldpos[1]] = None
            #Update the grid and self values
            
            if self.rep >= self.reproductionTreshold:
                
                self.reproduce(ocean, oldpos)
                #print("after reproduce ", ocean.count())





class Fish(Animal):


    num = 1

    reproductionTreshold = 4



class Shark(Animal):
    
    maximum_energy = 6
    energy_start = 3
    num = 2

    reproductionTreshold = 12
    def __init__(self, x, y):

        self.energy=self.energy_start
        super().__init__(x, y)
        #Inherit all __init__ variables from the superclass Animal


nbIter = 500
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


print("frames:", len(atlantic.states), "animals:", len(atlantic.animals), "last count:", atlantic.animalCount[-1] if atlantic.animalCount else None)


 # textual grid

