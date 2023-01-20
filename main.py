import random
from math import sqrt

def  someDoMonteCarlo(n):
    circle = 0

    for i in range(1, n + 1):
        x = random.random()
        y = random.random()

        # Checking to see if the produced number falls into the circle
        if sqrt(x ** 2 + y ** 2) <= 1:
            circle += 1

    Pi = 4 * (circle / n)


    return Pi



n = [10, 100, 1000]

Pi_storage = {}

for j in n:
     Pi_storage[j] = someDoMonteCarlo(j)
for k in n:
     print("The result of pi estimation after " + str(k) + " attempts is equal to: " + str(Pi_storage[k]))