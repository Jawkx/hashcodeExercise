pizzaCount = 5
twoPerson = 1
threePerson = 2
fourPerson = 1

def ingredient_num(arr):
    return len(arr) - 1 

pizs = [
    [0,'onion', 'pepper', 'olive'],
    [1,'mushroom', 'tomato' , 'basil'],
    [2,'chicken', 'mushroom' , 'pepper'],
    [3,'tomato', 'mushroom' , 'basil'],
    [4,'chicken', 'basil']
]

pizs.sort(key= ingredient_num , reverse = True)

def deliverPizza():

usedIng = []

for piz in pizs:
    pizNo = piz[0]
    pizIng = piz[1:]

    print ( pizNo , pizIng )


#print(piz)
