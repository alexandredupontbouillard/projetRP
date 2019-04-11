# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 21:30:21 2019

@author: alex0
"""

import numpy as np
import os
import commands;
#lis le fichier basiquement
def lecture_fichier(filename,nb):
    data = np.loadtxt ( filename, delimiter='\n', dtype=np.str )
    result=[]
    for i in range (1,len(data)*nb/100):
        ligne = data[i].split(" ")
        ligne = [i-1]+[ligne[0]]+ligne[2:]
        result.append(ligne)
    return result

#prend le resultat du fichier et le transforme en deux listes
def separerH_V(liste):
    H=[]
    V=[]
    for i in liste:
        if(i[1]=="V"):
            V.append(i)
        else:
            H.append(i)
    return H,V

      
#prend deux listes et en fait un ordre simple
def ordreSimple(H,V):
    result=[]
    taille = len(H)+int(len(V)/2)
    result.append(taille)
    for i in H:
        result.append([i[0]])
    for i in range(len(V)/2):
        result.append([V[i][0],V[i+1][0]])
    return result


#transforme une liste solution en un fichier solution
#format de la liste solution :
#[nb_diapo,[1,2],[3],[4,5],[6,7],[8]] par exemple

def transfo(result):
    fichier = open("result.txt", "w")
    fichier.write(str(result[0]))
    fichier.write("\n")
    for i in result[1:]:
        for j in i:
            fichier.write(str(j))
            fichier.write(" ")
        fichier.write("\n")
    fichier.close()

def evaluation(fichier,result,proportion):
	transfo(result)
	t=commands.getoutput("./Checker "+fichier+" "+str(proportion)+" result.txt")
	i = 0	
	while(t[i] != "="):
		i=i+1
	return int(t[i+2:])
    
filename = "b_lovely_landscapes.txt"
nb = 10
H,V = separerH_V(lecture_fichier(filename,nb))
result = ordreSimple(H,V)
print(evaluation(filename,result,nb))

