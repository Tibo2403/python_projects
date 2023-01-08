# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:24:31 2022

@author: Stephane_Metens
"""
import numpy as np
import numpy.linalg as nl

#solution de systemes lineaires algébriques
a = np.array([[1, 2], [3, 5]])
b = np.array([1, 2])

print("Matrice a",a)
print("b",b)
x = nl.linalg.solve(a, b)
print("solution du systeme",x)

A=np.array([[8,-6,2],[-4,11,-7],[4,-7,6]])
B=np.array([28,-40,33])

X=nl.linalg.solve(A,B)
print("X",X)

A2=np.array([[0,0,2,1,2],[0,1,0,2,-1],[1,2,0,-2,0],[0,0,0,-1,1],[0,1,-1,1,-1]])
B2=np.array([1,1,-4,-2,-1])

X=nl.linalg.solve(A2,B2)
print("X",X)

#produit de matrices
#xp=np.dot(M,x)
A=np.array([[2,-1,4],[3,0,1],[2,1,2]])
B=np.array([[4,-7,1],[2,2,-1],[0,4,-2]])
C=np.dot(A,B)
print("C",C)

A=np.array([[1,2,4,7],[-2,-4,0,1],[3,-1,-2,-3]])
B=np.array([[1,4],[3,-5],[2,-1],[0,4]])
C=np.dot(A,B)
print("C",C)

#transposition
AT=A.transpose()
print("AT",AT)
C=np.dot(A,AT)
print("AT A",C)

A=np.array([[2,3],[-1,4]])
#matrice de rotation d'angle t
#t=30
t=30.
R=np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
Rinv=np.linalg.inv(R)
#on exprime la matrice A dans la nouvelle base par
#A'=Inverse de R A R
AR= np.dot(A,R)
Aprime=np.dot(Rinv,AR)
TraceA=np.trace(A)
detA=np.linalg.det(A)
print("TraceA",TraceA)
print("det A",detA)
TraceAPrime=np.trace(Aprime)
print("TraceAPrime",TraceAPrime)
detAprime=np.linalg.det(Aprime)
print("det A prime",detAprime)
#les traces sont identiques, nous avons bien un des invariants des matrices