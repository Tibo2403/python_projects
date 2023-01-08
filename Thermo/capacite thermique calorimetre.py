"""reference : http://jlamerenx.fr/wp-content/uploads/2020/11/MC_Capacite%CC%81_thermique_dun_calorime%CC%80tre.html"""

import numpy as np
import matplotlib.pyplot as plt

N=100000

Ccal = []

for k in range(N) :
    T1=np.random.uniform(20.1,20.3)
    T2=np.random.uniform(47.2,47.4)
    Tf=np.random.triangular(30.2,31.2,32.2)
    M1i=np.random.uniform(152.5,153.5)
    M1f=np.random.uniform(98.5,99.5)
    M2i=np.random.uniform(175.5,176.5)
    M2f=np.random.uniform(118.5,119.5)
    Ccal.append(4.18*((M2i-M2f)*(T2-Tf)/(Tf-T1)+(M1f-M1i)))

Ccalm = sum(Ccal)/N
uCcal = np.std(Ccal,ddof=1)

print(f'Capacité thermique : {Ccalm} J/K')
print(f'Incertitude-type u(Ccal) : {uCcal} J/K')

#%%# Génération d'histogrammes

x = np.linspace(np.min(Ccal),np.max(Ccal),100)
Gaussienne = [1/(np.sqrt(2*np.pi*uCcal**2))*np.exp(-1/2*((z-Ccalm)/uCcal)**2) for z in x]

plt.hist(Ccal, bins='rice', density = True, label = "Valeurs simulées")
plt.plot(x, Gaussienne, 'k-', label = "Gaussienne associée")
plt.title(f'Simulation de {N} titrages \n Ccal = {Ccalm} J/K \n u(Ccal) = {uCcal} J/K')
plt.xlabel('Ccal en J.K$^{-1}$')
plt.legend()
plt.show()