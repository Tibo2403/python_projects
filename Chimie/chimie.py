#Demande la concentration et affiche le ph
def pH():
    c=eval(input("Entrer la concentration : "))
    print("Le PH est",-log10(c))

#Pour lancer :
pH()

from math import *

# Fonction qui donne v_x et v_y en fonction de la norme de v et de l'angle en degré par rapport à  l'horizontale
def coord_v(norme, angle):
    return norme*cos(radians(angle)),norme*sin(radians(angle))

# Convertir une quantite en mole
def convertir_mole(N):
    Na= 6.02214076*10**23
    return N/Na

def compo_finale(a,b,c,d,nx,ny):
    x=min(nx/a,ny/b)
    return nx-a*x,ny-b*y,c*x,d*x

def etat_eau(t):
    if t<0 :
        return "Solide"
    elif 0<=t<=100:
        return "Liquide"
    else :
        return "Gazeux"

def trouver_temps_radioactivité(proportion,T,precision=0.01):
    t=0
    Lambda=log(2)/T
    while exp(-Lambda*t)>proportion:
        t+=precision
    return t

# Donner la configuration electonique d'un atome en fonction du nombre d'electrons
def configuration_electronique(n):
    reponse=""
    ligne=0
    colonne=0
    couches="spdfg"
    while n>0:
        k=min(n, 4*colonne+2)
        n-=k
        reponse+=str(ligne+1)+couches[colonne]+str(k)+" "
        if colonne==0 :
            colonne,ligne=ligne+1,0
            while colonne>ligne:
                colonne-=1
                ligne+=1
        else :
            colonne-=1
            ligne+=1
    return reponse[:-1]