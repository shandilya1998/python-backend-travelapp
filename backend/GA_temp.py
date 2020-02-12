# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 23:51:51 2019

@author: shreyas.shandilya
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 22:34:42 2019
Assumptions-
1. The salesman travels at a constant speed to all cities
2. A grid is created to make all calculations. The  grid is of the size of max_lat_diff*max_long_diff
3. The salesman travels at a speed drawn from a uniform probablity distribution, with a minimum of 0 and maximum
such that he can cover the distance along the diagonal of the grid self.num_cities times over in 3 days. 
The grid is 200*200. Thus maximum speed is self.num_cities*grid_diag_length*math.sqrt(2)/self.num_days units\day
4. All computations are made on the average speed of the salesman
5. To be able to visit all cities,and have sufficient time to travel, it is assumed that the maximum time that the maximum time that the 
salesman can spend in a city is self.num_days/self.num_cities days and the minimum time being zero
@author: shreyas.shandilya
"""
import random
import math
import pandas as pd
import copy

class City():
    def __init__(self,
                 maximum_stay_time,
                 travelSpeed,
                 name=None,
                 x = None,
                 y = None):
        """
         The x and y coordinates of all the cities will be between 0 and 200
         Generates a city with random coordinates if x and y are not provided
         If x and y are provided then generates a city with coordinates x and y
        """
        if x and y:
            self.x = x
            self.y = y
        elif x and not y:
            raise ValueError('Please provide two coordinates. One provided')
        elif not x and y:
            raise ValueError('Please provide two coordinates. One provided')
        else:           
            self.x = random.randint(0,200)
            self.y = random.randint(0,200)
        if not name:
            self.name = 'Unnamed Location'
        else:
            self.name = name
        # Defines the amount of time a tourist will want to stay at an attraction
        # When at the pivot, this refers to the time that the sales man takes to rest
        self.stay_time = random.uniform(0,maximum_stay_time)
        self.travelSpeed = travelSpeed
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distance_cities(self,
                        City2):
        # Takes the object of another class as input and computes the distance between the current city and the input city
        x_ = City2.getX()
        y_ = City2.getY()
        delta_x = self.x-x_
        delta_y = self.y-y_
        distance = math.sqrt(delta_x**2+delta_y**2)
        return distance
    
    def __repr__(self):
        # Creates the string representation of the class City object
        return self.name
    
class Itinerary():
    def __init__(self):
        self.city_lst = []
        
    def addCity(self,
                City):
        # Adds a city to the itinerary
        self.city_lst.append(City)
    
    def getCity(self,
                index):
        # returns a city at the specified index in the  itinerary
        return self.city_lst[index]
    
    def getNumCities(self):
        # Returns the number of cities in itinerary
        return len(self.city_lst)
    
class Tour():
    def __init__(self,
                 itinerary,
                 travelSpeed,
                 pivot,
                 final,
                 num_days,
                 tour = None):
        self.tour = []
        self.fitness = 0.0
        self.distance = 0.0
        self.tourTime = 0.0
        self.itinerary = itinerary
        self.travelSpeed = travelSpeed
        self.pivot = pivot
        self.final = final
        self.num_days = num_days
        self.plan = []
        # Constructs a list of blank cities(None) if tour  is not provided
        # If tour is given, sets self.tour as tour
        if not tour:
            for i in range(0,self.itinerary.getNumCities()):
                self.tour.append(None)
        else:
            self.tour = tour
        self.plan = [self.pivot]+self.tour+[self.final]
        self.createPlan()
                
    def generateIndividual(self):
        """
         Generate an individual
         Loop through all our destination cities and add them to our tour
         Randomly shuffle all cities in the tour after adding them to the tour
         Add self.pivot and self.final at the  beginning and end of the  tour
        """
        for cityIndex in  range(0,self.itinerary.getNumCities()):
            self.setCity(cityIndex, self.itinerary.getCity(cityIndex),True)
        random.shuffle(self.tour)
        self.createPlan()
            
    def createPlan(self):
        rand_pos = random.randint(2,self.tourSize()+self.num_days-2)
        sample = [rand_pos]
        self.plan = [self.pivot]+self.tour+[self.final]
        for i in range(0, self.num_days-1):
            self.plan.insert(rand_pos,self.pivot)
            while(True):
                rand_pos = random.randint(2,self.tourSize()-2)
                if rand_pos in sample:
                    continue
                elif rand_pos+1 in sample or rand_pos-1 in sample:
                    continue
                else:
                    sample.append(rand_pos)
                    break
        if None not in self.plan:
            self.plan = self.createDays()
                
    def createDays(self):
        plan = copy.deepcopy(self.plan)
#        print(plan)
        plan_ = [plan[0]]
        time = plan[0].distance_cities(plan[1])/self.travelSpeed
        temp = 0
        cityIndex = 1
        while cityIndex<len(plan)-1:
            fromCity = plan[cityIndex]
            plan_.append(fromCity)
#            print(fromCity)
            if math.floor(time+fromCity.distance_cities(self.pivot)+self.pivot.stay_time)>temp:
                if plan[cityIndex+1] != self.pivot:
                    plan.insert(cityIndex+1,self.pivot)
                    destinationCity = copy.deepcopy(self.pivot) 
                    time = time + fromCity.distance_cities(destinationCity)/self.travelSpeed + fromCity.stay_time
#                    print('pivot')
                    cityIndex+=1
                else:
                    destinationCity = plan[cityIndex]
                    time = time + fromCity.distance_cities(destinationCity)/self.travelSpeed + fromCity.stay_time
                temp = math.floor(time)
            else:
                if plan[cityIndex+1] == self.pivot and plan[cityIndex] != self.pivot :
                    plan[cityIndex+1] = copy.deepcopy(plan[cityIndex+2])
                    plan[cityIndex+2] = self.pivot
                    destinationCity = copy.deepcopy(plan[cityIndex+1])
                    time = time + fromCity.distance_cities(destinationCity)/self.travelSpeed + fromCity.stay_time
                else:
                    destinationCity = plan[cityIndex+1]
                    time = time + fromCity.distance_cities(destinationCity)/self.travelSpeed + fromCity.stay_time
            cityIndex+=1
        plan_.append(plan[-1])
        return plan_
                        
    def setCity(self,
                cityIndex, 
                City,
                gen = False):
        """
         Sets a city at a given position in the tour
         Resets self.fitness and self.distance to 0.0 when self.tour is modified
        """
        self.tour[cityIndex] = City
        self.fitness = 0.0
        self.distance = 0.0
        if not gen:
            self.createPlan()
        
    def getCity(self,
                tourPosition):
        # Returns a city at position tourPosition
        return self.tour[tourPosition]
    
    def getCityPlan(self,
                    planPosition):
        return self.plan[planPosition]
    
    def getFitness(self):
        # Returns the fitness of a tour
        if self.fitness == 0.0:
            self.fitness = self.getTourTime()
        return self.fitness
    
    def getTourTime(self):
        travel_time = self.getDistance()/self.travelSpeed
        stay_time = 0.0
        for city in self.plan:
            stay_time = stay_time+city.stay_time 
        self.tourTime = stay_time+travel_time - self.pivot.stay_time
        return self.tourTime
    
    def getDistance(self):
        if self.distance == 0.0:
            tourDistance = 0.0
            # Loop through cities in the tour
#            print(self.plan)
            for cityIndex in range(0,self.tourSize()+self.num_days+1):
                # Source City
                fromCity = self.getCityPlan(cityIndex)
                # Destination city
                try:
                    destinationCity = self.getCityPlan(cityIndex+1)
                except IndexError:
                    destinationCity = self.getCityPlan(0)
                tourDistance+=fromCity.distance_cities(destinationCity)
            self.distance = tourDistance
        return self.distance
    
    def tourSize(self):
        return len(self.tour)
    
    def containsCity(self,
                     City):
        # Checks if the tour contains the input city
        try:
            self.tour.index(City)
            return True
        except ValueError:
            return False
        
#    def createDailyPlan(self):
#        self.plan=[self.pivot]
#        time = (self.pivot.distance_cities(self.getCity(0))/self.travelSpeed)
#        temp=0
#        for cityIndex in range(0,self.tourSize()):
#            fromCity = self.getCity(cityIndex)
#            self.plan.append(fromCity)
#            try:
##                print(time+(fromCity.distance_cities(self.pivot)/self.travelSpeed)-temp)
#                print(temp)
#                if time+(fromCity.distance_cities(self.pivot)/self.travelSpeed)-temp>=1:
##                    print('pivot')
#                    destinationCity = self.pivot
#                    time = fromCity.stay_time+(fromCity.distance_cities(destinationCity)/self.travelSpeed) 
#                    self.plan.append(self.pivot)
#                    destinationCity = self.getCity(cityIndex+1)
#                    time+= self.pivot.stay_time+(self.pivot.distance_cities(destinationCity)/self.travelSpeed) 
#                    temp+=1
##                    print(time)
##                    print(temp)
#                else:
##                    print('not pivot')
#                    destinationCity = self.getCity(cityIndex+1)
#                    time+= fromCity.stay_time+(fromCity.distance_cities(destinationCity)/self.travelSpeed)
#            except IndexError:
##                print('except')
#                destinationCity = self.final
#                time+= fromCity.stay_time+(fromCity.distance_cities(destinationCity)/self.travelSpeed)
#        return time
        
    def __repr__(self):
        # Creates a string representation of the tour class object
        geneString = '|'
        for i in range(0,self.tourSize()):
            geneString+=str(self.getCity(i))+'|'
        return geneString
    
class Population():
    def __init__(self,
                 populationSize, 
                 initialize,
                 itinerary,
                 travelSpeed,
                 pivot,
                 final,
                 num_days):
        self.tours = []# Holds population of tours
        self.populationSize = populationSize
        self.initialize = initialize
        self.itinerary=itinerary
        self.travelSpeed = travelSpeed
        self.pivot = pivot
        self.final = final
        self.num_days = num_days
        for i in range(0,self.populationSize):
            self.tours.append(None)
        # Constructs a population of tours
        if initialize:
            # Loop to create individuals
            for i in range(0,self.populationSize):
                newTour = Tour(self.itinerary,self.travelSpeed,self.pivot,self.final,self.num_days)
                newTour.generateIndividual()
                self.saveTour(i,newTour)
        
    def saveTour(self,
                 index,
                 Tour):
        # Appends a tour 
        self.tours[index]=Tour
        
    def getTour(self, 
                index):
        # Returns the tour at the  given index
        return self.tours[index]
    
    def getFittest(self):
        # Finds the fittest tour
        fittest=self.tours[0]
        for i in range(0, self.populationSize):
            if fittest.getFitness() >= self.getTour(i).getFitness():
                fittest = self.getTour(i)
        return fittest
    
    def populationSize_(self):
        return len(self.tours)
    
class GeneticAlgorithm():
    def __init__(self,
                 itinerary,
                 travelSpeed,
                 pivot,
                 final,
                 num_days,
                 mutationRate = 0.015,
                 tournamentSize = 5,
                 elitism=True):
        self.mutationRate = mutationRate
        self.tournamentSize = tournamentSize
        self.elitism = elitism
        self.itinerary = itinerary
        self.travelSpeed = travelSpeed
        self.pivot = pivot
        self.final = final
        self.num_days = num_days
        
    def evolvePopulation(self, 
                         pop):
        # Evovles the current population through crossover and mutation 
        newPopulation =  Population(pop.populationSize_(),
                                   False,
                                   self.itinerary,
                                   self.travelSpeed,
                                   self.pivot,
                                   self.final,
                                   self.num_days)
        # Keep the best population if elitism is True
        elitismOffset = 0
        if self.elitism:
            newPopulation.saveTour(0,pop.getFittest())
            elitismOffset = 1
        
        """
         Crossover  population
         Loop over the new population's size and create individuals from
         Current population
        """
        for i in range(elitismOffset,newPopulation.populationSize_()):
            # Select Parents
            parent1 = self.tournamentSelection(pop)
            parent2 = self.tournamentSelection(pop)
            #  Crossover Parents
            child = self.crossover(parent1,
                                   parent2)
            newPopulation.saveTour(i,child)
        
        # Mutate the new population to add new genetic material
        for i in range(elitismOffset,newPopulation.populationSize_()):
            self.mutate(newPopulation.getTour(i))
        
        return newPopulation
    
    def crossover(self,
                  parent1,
                  parent2):
        # Applies crossover to set of parents and creates offspring
        child=Tour(self.itinerary,self.travelSpeed,self.pivot,self.final,self.num_days)
        startPos = int(random.random()*parent1.tourSize())
        endPos = int(random.random()*parent1.tourSize())
        
        # Loops through the child tour and places all cities of parent1 from startPos to endPos in child city
        for i in range(0,child.tourSize()):
            if startPos < endPos and i > startPos and i < endPos:
                child.setCity(i, 
                              parent1.getCity(i))
            elif startPos > endPos:
                if not (i < startPos and i> endPos):
                    child.setCity(i, 
                                  parent1.getCity(i))
         
        # Loops through the child city and fills all vacant spots with cities from parent2
        for i in range(0,parent2.tourSize()):
            if not child.containsCity(parent2.getCity(i)):
                for j in range(0,child.tourSize()):
                    if not child.getCity(j):
                        child.setCity(j,parent2.getCity(i))
                        break
        
        return child
    
    def mutate(self,
               tour):
        # Mutates a tour by swapping the position of two cities
        for tourPos1 in range(0,tour.tourSize()):
            if random.random() < self.mutationRate:
                tourPos2 = int(tour.tourSize()*random.random())
                city1 = tour.getCity(tourPos1)
                city2 = tour.getCity(tourPos2)
                tour.setCity(tourPos2,
                             city1)
                tour.setCity(tourPos1,
                             city2)
                
    def tournamentSelection(self,
                            pop):
        # Selects self.tournamentSize cities from the population for crossover
        tournament = Population(self.tournamentSize,
                                False,
                                self.itinerary,
                                self.travelSpeed,
                                self.pivot,
                                self.final,
                                self.num_days)
        for i in range(0, self.tournamentSize):
            randomInt = int(random.random()*pop.populationSize_())
            tournament.saveTour(i,pop.getTour(randomInt))
        fittest = tournament.getFittest()
        return fittest
        
class TSP_GA():
    def __init__(self,
                 num_days,
                 populationSize,
                 num_cycles,
                 file):
        self.location_file = file
        self.df = pd.read_csv(self.location_file)
        self.num_cities = len(self.df)
        self.num_days = num_days
        self.populationSize = populationSize
        self.num_cycles = num_cycles
        self.maximum_stay_time =  float(self.num_days/self.num_cities)
        self.travelSpeed = self.calcTravelSpeed()
        # Ensure that the pivot ie the hotel to return to always is always at the top of the csv file
        self.pivot = City(self.maximum_stay_time,self.travelSpeed,self.df.iloc[0]['Location'],self.df.iloc[0]['Latitude'],self.df.iloc[0]['Longitude'])
        self.final=City(self.maximum_stay_time,self.travelSpeed,self.df.iloc[self.num_cities-1]['Location'],self.df.iloc[self.num_cities-1]['Latitude'],self.df.iloc[self.num_cities-1]['Longitude'])
        self.df = self.df[1:self.num_cities-1]
        
    def calcTravelSpeed(self):
        minLat = self.df['Latitude'].min()
        minLong = self.df['Longitude'].min()
        maxLat = self.df['Latitude'].max()
        maxLong = self.df['Longitude'].max()
        delta_x = maxLat-minLat
        delta_y = maxLong-minLong
        diag = math.sqrt(delta_x**2 +  delta_y**2)
        speed = diag*12/(self.num_days*2)
        return speed
        
    def main(self):
        itinerary = Itinerary() # This creates the  itinerary for the customer
        # Add input for city coordinates later
        for i in range(0,len(self.df)):
            x = float(self.df.iloc[i]['Latitude'])
            y = float(self.df.iloc[i]['Longitude'])
            name =  self.df.iloc[i]['Location']
            city = City(self.maximum_stay_time,self.travelSpeed,name,x,y)
            itinerary.addCity(city)
        self.pop = Population(self.populationSize,
                         True,
                         itinerary,
                         self.travelSpeed,
                         self.pivot,
                         self.final,
                         self.num_days)
        print('Initial distance:')
        print(self.pop.getFittest().getDistance())
        
        self.pop = GeneticAlgorithm(itinerary,self.travelSpeed,self.pivot,self.final,self.num_days).evolvePopulation(self.pop)
        cycles=0
        while(True):
            self.pop = GeneticAlgorithm(itinerary,self.travelSpeed,self.pivot,self.final,self.num_days).evolvePopulation(self.pop)
            cycles+=1
            if cycles >= self.num_cycles:
                break

        print('Fin')
        print('Final distance:')
        print(self.pop.getFittest().getDistance())
        print('Minimum tour time:')
        print(self.pop.getFittest().getTourTime())
        print('Solution:')
        print(self.pop.getFittest().plan)
        
if __name__=='__main__':
    file=r'C:\Users\shreyas.shandilya\Desktop\location.csv'
    ob=TSP_GA(3,50,100,file)
    temp=ob.main()
    
            
        
        
                    
            
        
        
    
                
            
            
        
        
        
            
    
        

        
            
    
    
    
        
        
        