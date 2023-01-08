""" references : http://jlamerenx.fr/wp-content/uploads/2020/11/M%C3%A9thode_dEuler.html """
import matplotlib.pyplot as plt
from math import exp


"""Conditions initiales"""
a=1   # en mol/L


"""Paramètres de la méthode d'intégration"""
h=0.001         # en s
duree = 1       # en s


"""Valeurs des constantes de vitesse"""
k=10            # en s^(-1)


"""Listes des valeurs calculées des concentrations"""
LT=[0]        # liste des instants t
LA=[a]        # liste des concentrations successives de A


""" Boucle d'intégration"""
nbpts =duree/h
i=1
while i<=nbpts and LA[-1] >= 0 :
    A=LA[-1]
    LT.append(i*h)
    LA.append(A - k*A*h)
    i=i+1


"""Liste de valeurs issues de la solution analytique"""
A_litt = [a * exp(-k*t) for t in LT]


"""Tracé des courbes des concentrations calculées en fonction du temps"""
plt.figure(1)
plt.plot(LT,LA,'b--', label='A Euler')
plt.plot(LT,A_litt,'g--', label='A littéral')
plt.xlabel('t en s')
plt.ylabel('Concentrations en $mol.L^{-1}$')
plt.title(f"Intégration par la méthode d'Euler : k = {k} s^(-1) et pas de calcul h = {h} s")
plt.legend()
plt.grid()
plt.show()