# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 21:30:21 2019

@author: alex0
"""

import numpy as np
import os
import commands;
import random as r
import copy
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
        result.append([V[2*i][0],V[2*i+1][0]])
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

def evaluation(data,result,nb):
	score=0	
	for i in range(1,len(result)-1):
		d1 = [ data[j] for j in result[i]]
		d2 = [ data[j] for j in result[i+1]]
		score = score + evalCouple(d1,d2)
	return score
# prend en paramètre un couple de diapo exemple : [[8,H,rfe,ef]],[[5,V,er,tgr,ef],[6,V,erg,ferf,erf]]
def evalCouple(l1,l2):
	if(len(l1)==1):
		s1 = set(l1[0][2:])
	else:
		s1 = set(l1[0][2:] + l1[1][2:])
	if(len(l2)==1):
		s2 = set(l2[0][2:])
	else:
		s2 = set(l2[0][2:] + l2[1][2:])
	cardinal_intersect=len(s1.intersection(s2))

	
	return min([cardinal_intersect,len(s1) - cardinal_intersect,len(s2) - cardinal_intersect])


def evaluation2(fichier,result,proportion):
	transfo(result)
	t=commands.getoutput("./Checker "+fichier+" "+str(proportion)+" result.txt")
	i = 0	
	while(t[i] != "="):
		i=i+1
	return int(t[i+2:])
  
def glouton(H,V):
	taille = len(H)+len(V)/2
	H1 = copy.deepcopy(H)
	V1 = 	copy.deepcopy(V)
	HouV = r.randint(1,2)
	result=[taille]
	if(HouV == 1):
		n=r.randint(0,len(H))
		result.append([H[n][0]])
		del(H1[n])
		pred = [H[n]]
	else : 
		l = r.sample(set(range(len(V))),2)
		result.append([V[l[0]][0],V[l[1]][0]])
		del(V1[l[0]])
		if(l[0]<l[1]):
			del(V1[l[1]-1])
		else:
			del(V1[l[1]])
		pred = [V[l[0]],V[l[1]]]
	
	while(len(H1)>0 ):

		maxx = evalCouple([H1[0]],pred)
		index1 = 0
		index2 = 0
		typ = "H"
		for i in range(len(H1)):
			m=evalCouple([H1[i]],pred)
			if(maxx<m):
				maxx=m
				index1=i
		for i in range(len(V1)):
			for j in range(len(V1)):
				if(i!=j):
					m=evalCouple([V1[i],V1[j]],pred)
					if(maxx<m):
						maxx=m
						index1 = i
						index2 = j
						typ="V"
		if(typ=="H"):
			result.append([H1[index1][0]])
			pred = [H1[index1]]
			del(H1[index1])
		else : 
			pred = [V1[index1],V1[index2]]
			result.append([V1[index1][0],V1[index2][0]])
			del(V1[index1])
			if(index2<index1):
				del(V1[index2])
			else:
				del(V1[index2-1])
	while(len(V1)>1):
		maxx = evalCouple([V1[0],V1[1]],pred)
		index1 = 0
		index2 = 1
		for i in range(len(V1)):
			for j in range(len(V1)):
				if(i!=j):
					m=evalCouple([V1[i],V1[j]],pred)
					if(maxx<m):
						maxx=m
						index1 = i
						index2 = j
		pred = [V1[index1],V1[index2]]
		result.append([V1[index1][0],V1[index2][0]])
		del(V1[index1])
		if(index2<index1):
			del(V1[index2])
		else:
			del(V1[index2-1])
	if(len(V1)==1):
		result.append([V[0][0]])
	return result
	
		
	  


filename = "c_memorable_moments.txt"
nb = 70
data = lecture_fichier(filename,nb)
H,V = separerH_V(data)
result = glouton(H,V)
print(evaluation2(filename,result,nb))

