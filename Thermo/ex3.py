# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:19:21 2022

@author: Stephane_Metens
"""

import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt

# definition de la fonction a integrer
def fonc(x):
    return 4*x + 3


# Définition d'une fonction qui calcul la valeur moyenne d'un tableau
def val_moy(tab):
    moy = 0.
    for val in tab:
        moy += val
    return moy / len(tab)

# definition d'une fonction qui fait le cacul pour un n donné
# on integre la fct f entre a et b en utilisant n point pour
#calculer la valeur moyenne de f. n donne la longueur de tab
def integ(n, f, a, b):
    x = rd.uniform(a, b, n)
# la fonction rd.uniform (a,b,n) tire n points réparti de façon
#uniforme entre a et b
    y = f(x)
    return (b-a) * val_moy(y)


x1 = 0.
x2 = 5.
N = 100
val_integrale=integ(N,fonc,x1,x2)
print(val_integrale)

N = np.array([10, 100, 1000, 10000, 20000,30000,50000,70000,100000])
I = np.zeros(len(N))
print("len(N)",len(N))
for i in range(len(N)):
    I[i] = integ(N[i], fonc, x1, x2)

plt.plot(N, I, 'bo')
plt.plot(N, 65*np.ones(len(N)), 'rd')
plt.xlabel('N')
plt.ylabel('I')
plt.xscale('log')
plt.xlim(1, 1e5)
plt.show()

print(I[len(N)-1])