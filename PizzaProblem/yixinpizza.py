import os
import numpy as np
from math import floor

inputFile = input("Enter file name: ")
inF = open(inputFile, 'r')
lines = inF.readlines()
M, T2, T3, T4 = [int(n) for n in lines[0].split()]

outputFile = 'Output.txt'
outF = open(outputFile,'w')

pizzaArr = []
ingArr = []
uniquePizza = []

for p in range(1, len(lines)):
    availPizza = lines[p].split()
    pizzaArr.append(availPizza)

inF.close()

for index,piz in enumerate(pizzaArr):
    piz[0] = int(piz[0])    # convert no. of ingredients from str to int
    piz.insert(0,index)     # add index to pizzaArr

def index1(pizzaArr):
    return pizzaArr[1]

pizzaArr.sort(key=index1)     # sort pizzaArr by no. of ingredients in ascending order


def findUnique():
    for pizza in pizzaArr:
        newIng = 0
        for ingredient in pizza[2:]:
            if ingredient not in ingArr:
                newIng = newIng + 1
                
            if newIng == pizza[1]:
                for ingredient in pizza[2:]:
                    ingArr.append(ingredient)
                uniquePizza.append(pizza)

def deliver():
    outF = open(outputFile, "a")
    if len(uniquePizza) >= 1:
        outF.write("{} ".format(uniquePizza[0][0]))
        pizzaArr.pop(pizzaArr.index(uniquePizza[0]))
        uniquePizza.pop(0)
        print("Unique")

    else:
        outF.write("{} ".format(pizzaArr[0][0]))
        pizzaArr.pop(0)
        print("Not Unique")

def deliverTeam(team):
    outF = open(outputFile, "a")
    outF.write("{} ".format(team))
    outF.close()
    for i in range(team):
        deliver()
    outF = open(outputFile, "a")
    outF.write("\n")
    outF.close()

for i in range (M):
    findUnique()
    if T4 >= 1 and len(pizzaArr) - 4 > 0:
        deliverTeam(4)
        T4 = T4 - 1

    elif T3 >= 1 and len(pizzaArr) - 3 >= 0 and len(pizzaArr) - T2*2 != 0 :
        deliverTeam(3)
        T3 = T3 - 1
    
    elif T2 >= 1 and len(pizzaArr) - 2 >= 0:
        deliverTeam(2)
        T2 = T2 - 1

    uniquePizza.clear()
    ingArr.clear()
    
    if len(pizzaArr) < 2:
        break

print("Remaining pizzas: ", len(pizzaArr))
print("Remaining team of 4: ", T4)
print("Remaining team of 3: ", T3)
print("Remaining team of 2: ", T2)
