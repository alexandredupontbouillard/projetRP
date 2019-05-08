# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 21:30:21 2019

@author: alex0
"""

import numpy as np
import os
#import commands
import random as r
import copy
import gurobipy
import copy as c
import time as t
#lis le fichier basiquement
def lecture_fichier(filename,nb):
    data = np.loadtxt ( filename, delimiter='\n', dtype=np.str )
    result=[]
    for i in range (1,int(len(data)*nb/100)):
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
    V1 =     copy.deepcopy(V)
    HouV=1
    if(len(V)>2):
        HouV = r.randint(1,2)
    if(len(H)==0):
        HouV = 2
    result=[taille]
    if(HouV == 1):
        if(len(H)>1):
            n=r.randint(0,len(H)-1)
        else:
            n=0
        print(len(H))
        print(n)
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

#on fait des couples aléatoires d'image verticales puis on ajoute au fur et à mesure les images
def glouton2(H,V):
    taille = len(H)+len(V)/2 
    H1 = copy.deepcopy(H)
    V1 =     copy.deepcopy(V)
    HouV=1
    if(len(V)>2):
        HouV = r.randint(1,2)
    if(len(H)==0):
        HouV = 2
    result=[taille]
    if(HouV == 1):
        if(len(H)>1):
            n=r.randint(0,len(H)-1)
        else:
            n=0
        result.append([H[n][0]])
        del(H1[n])
        pred = [H[n]]
        result[0] = result[0] -1
    else : 
        l = r.sample(set(range(len(V))),2)
        result.append([V[l[0]][0],V[l[1]][0]])
        del(V1[l[0]])
        if(l[0]<l[1]):
            del(V1[l[1]-1])
        else:
            del(V1[l[1]])
        pred = [V[l[0]],V[l[1]]]
    V2 = []
    
    for i in range(int(len(V)/2)-1):
        l = r.sample(set(range(len(V1))),2)
        V2.append([V1[l[0]],V1[l[1]]])
        del(V1[l[0]])
        if(l[0]<l[1]):
            del(V1[l[1]-1])
        else:
            del(V1[l[1]])

    while(len(H1)>0 or len(V2)>0):
        H = False
        compteur=0
        for i in range(len(H1)):
            if(evalCouple([H1[i-compteur]],pred)>0):
                pred = [H1[i-compteur]]
                H=True
                result.append([H1[i-compteur][0]])
                del(H1[i-compteur])
                compteur=compteur+1
        if(not H):
            for i in range(len(V2)):
                if(evalCouple(V2[i],pred)>0):
                    pred = V2[i]
                    result.append([V2[i][0][0],V2[i][1][0]])
                    H=True
                    del(V2[i])
                    break
        if(not H):
            if(len(V2)>0 and len(H1)>0):
                HouV=HouV = r.randint(1,2)
            elif(len(V2)>0):
                HouV = 2
            else:
                Houv = 1
            if(HouV == 1):
                if(len(H1)>1):
                   n=r.randint(0,len(H1)-1)
                else:
                   n=0
                result.append([H1[n][0]])
                pred = [H1[n]]                
                del(H1[n])
            else:
                if(len(V2)>1):
                   n=r.randint(0,len(V2)-1)
                else:
                   if(len(V2)==0):
                       break
                   n=0
                result.append([V2[n][0][0],V2[n][1][0]])
                pred = V2[n]                
                del(V2[n])

    return result
def descente_stochastique(data, result,nb):
    n = len(result)
    maxi = evaluation(data, result,nb)
    modif = True
    while(modif):
        modif = False
        for i in range(1, n-1):
            result_local = copy.deepcopy(result)
            if (len(result_local[i]) == 2 and len(result_local[i+1]) == 2):
                if (r.random() < 0.5):
                    v1 = r.randint(0, 1)
                    v2 = r.randint(0, 1)
                    result_local[i][v1], result_local[i+1][v2] = result_local[i+1][v2], result_local[i][v1]
                else:
                    result_local[i],result_local[i+1] = result_local[i+1], result_local[i]
            else:
                result_local[i], result_local[i+1] = result_local[i+1],result_local[i]
            maxi_local = evaluation(data, result_local,nb)
            if (maxi_local > maxi):
                modif = True
                maxi = maxi_local
                result = result_local
    return result

def evalCouple2(r1, r2,data):
    if(len(r1)==2 and len(r2)==2):
        return evalCouple([data[r1[0]],data[r1[1]]],[data[r2[0]],data[r2[1]]])
    if (len(r1) == 2):
        return evalCouple([data[r1[0]], data[r1[1]]], [data[r2[0]]])
    if(len(r2)==2):
        return evalCouple([data[r1[0]], data[r2[0]]], [data[r2[1]]])
    return evalCouple([data[r1[0]]],[data[r2[0]]])

def descente_stochastique2(data, result,NB):
    n = len(result)
    maxi = evaluation(data, result,NB)
    modif = True
    maxTransi = 0
    maxPosition = -1
    while(modif):
        modif = False
        for i in range(n-1,2,-1):
            result_local = copy.deepcopy(result)
            maxTransi = evalCouple2(result[i],result[i-1],data)
            maxPosition = -1
            for k in range(NB):
                j = r.randint(1,i-1)
                maxTlocal = evalCouple2(result_local[i],result_local[j],data)
                if(maxTlocal>maxTransi):
                    maxTransi = maxTlocal
                    maxPosition = j
            if(maxPosition != -1):
                result_local[i-1],result_local[maxPosition] = result_local[maxPosition],result_local[i-1]
                maxi_local = evaluation(data, result_local,NB)
                if (maxi_local > maxi):
                    modif = True
                    maxi = maxi_local
                    result = result_local
    return result

def pl_binary(H,data):
    m = gurobipy.Model("MyModel")
    V = len(H)
    x = []
    z = []
    
    for i in range(V+1):
        x2 = []
        for j in range(V+1):
            x2.append(m.addVar(vtype = gurobipy.GRB.BINARY, name = "x%d%d"%(i,j)))
        x.append(x2)
    for i in range(V+1):
        z2 = []
        for j in range(V+1):
            z2.append(m.addVar(vtype = gurobipy.GRB.CONTINUOUS, name = "z%d%x"%(i,j)))
        z.append(z2)
    m.update()
    
    obj = gurobipy.LinExpr();
    obj = 0
    #Fonction objectif
    for i in range(V):
        for j in range(V):
            obj += evalCouple2(H[i],H[j],data) * x[i][j]
    m.setObjective(obj,gurobipy.GRB.MAXIMIZE)
    
    #1 arete sortante par sommet
    for j in range(V+1):
        m.addConstr(gurobipy.quicksum(x[i][j] for i in range(V+1))==1)
    #1 arete entrante par sommet
    for i in range(V+1):
        m.addConstr(gurobipy.quicksum(x[i][j] for j in range(V+1))==1)
    #pas d'arete sur un meme sommet
    for i in range(V+1):
        m.addConstr(x[i][i]==0)
    #pas d'arete de a vers b et de b vers a simultanes
    for i in range(V+1):
        for j in range(V+1):
            m.addConstr(x[i][j]+x[j][i]<=1)
            
    #Contraintes de flots
    #1
    m.addConstr(gurobipy.quicksum(z[0][j] for j in range(1,V+1)) == V)
    #2
    for i in range(1,V+1):
        m.addConstr( (gurobipy.quicksum(z[i][j] for j in range(1,V+1) if j != i)+1) == (gurobipy.quicksum(z[j][i] for j in range(V+1) if j!=i)) )
    #3
    for i in range(V+1):
        list_j = [j for j in range(1,V+1) if j != i]
        for j in list_j:
            m.addConstr((z[i][j]+z[j][i]) <= (V)*(x[i][j]+x[j][i]))
    #4
    for i in range(V+1):
        list_j = [j for j in range(1,V+1) if j != i]
        for j in list_j:
            m.addConstr(z[i][j]>=0)
    #Resolution
    m.optimize()
    result= []
    for i in range(V):
        for j in range(V):
            if(x[i][j].x == 1):
                result.append([[i],[j]])
                
    
    result1 = transfoPl(result)[0]
    result1.insert(0,len(result1))
    return result1

def transfoPl(lCouple):
    if(len(lCouple) ==1):
        return lCouple
    else:
        elem = lCouple[0]
        for i in range(1,len(lCouple)):
            if(lCouple[i][0]  == elem[len(elem)-1]):
                del(elem[len(elem)-1])
                lCouple[i] =  elem + lCouple[i] 
                del(lCouple[0])
                return transfoPl(lCouple)
            if(lCouple[i][len(lCouple[i])-1]  == elem[0]):
                del(elem[0])
                lCouple[i] =   lCouple[i] + elem
                del(lCouple[0])
                return transfoPl(lCouple)    
        return lCouple  

def deepTransfoPl(lCouple):
    if(len(lCouple) ==1):
        return lCouple
    else : 
        b = False
        for  i in lCouple:
            for j in lCouple:
                if(i[0] == j[len(j)-1] and i!=j):
                    b=True
                    a = lCouple.index(j)
                    j.pop()
                    lCouple[a] = lCouple[a] + i
                    lCouple.remove(i)
                    break
        if(b):
            return deepTransfoPl(lCouple)
        else:
            return lCouple

def heuristique_arrondi(H,data):
    m = gurobipy.Model("MyModel")
    V = len(H)
    x = []
    z = []
    
    for i in range(V+1):
        x2 = []
        for j in range(V+1):
            x2.append(m.addVar(vtype = gurobipy.GRB.CONTINUOUS, name = "x%d%d"%(i,j)))
        x.append(x2)
    for i in range(V+1):
        z2 = []
        for j in range(V+1):
            z2.append(m.addVar(vtype = gurobipy.GRB.CONTINUOUS, name = "z%d%x"%(i,j)))
        z.append(z2)
    m.update()
    
    obj = gurobipy.LinExpr();
    obj = 0
    #Fonction objectif
    for i in range(V):
        for j in range(V):
            obj += evalCouple2(H[i],H[j],data) * x[i][j]
    m.setObjective(obj,gurobipy.GRB.MAXIMIZE)
    
    #1 arete sortante par sommet
    for j in range(V+1):
        m.addConstr(gurobipy.quicksum(x[i][j] for i in range(V+1))==1)
    #1 arete entrante par sommet
    for i in range(V+1):
        m.addConstr(gurobipy.quicksum(x[i][j] for j in range(V+1))==1)
    #pas d'arete sur un meme sommet
    for i in range(V+1):
        m.addConstr(x[i][i]==0)
    #pas d'arete de a vers b et de b vers a simultanes
    for i in range(V+1):
        for j in range(V+1):
            m.addConstr(x[i][j]+x[j][i]<=1)
            
    #Contraintes de flots
    #1
    m.addConstr(gurobipy.quicksum(z[0][j] for j in range(1,V+1)) == V)
    #2
    for i in range(1,V+1):
        m.addConstr( (gurobipy.quicksum(z[i][j] for j in range(1,V+1) if j != i)+1) == (gurobipy.quicksum(z[j][i] for j in range(V+1) if j!=i)) )
    #3
    for i in range(V+1):
        list_j = [j for j in range(1,V+1) if j != i]
        for j in list_j:
            m.addConstr((z[i][j]+z[j][i]) <= (V)*(x[i][j]+x[j][i]))
    #4
    for i in range(V+1):
        list_j = [j for j in range(1,V+1) if j != i]
        for j in list_j:
            m.addConstr(z[i][j]>=0)
    #Resolution
    m.optimize()
    result = []
    
    v = [ [x[i][j].x,i,j] for j in range(len(x[i])-1) for i in range(len(x)-1)]
    v.sort(key=lambda y:y[0], reverse = True)
    alreadyI = [0] * V
    alreadyJ = [0] * V
    compteur=0
    while(compteur < V-1):
        if(alreadyI[v[0][1]] == 0 and alreadyJ[v[0][2]]==0):
            r = c.deepcopy(result)
            r.append([[v[0][1]],[v[0][2]]])
            r = deepTransfoPl(r)
            b=True
        
            for i in r :
                if(i[0] == i[len(i)-1]):
                    b= False
            if(b):
                compteur = compteur+1
                result = r
                

                alreadyI[v[0][1]]=1
                alreadyJ[v[0][2]]=1
        del(v[0])
    result = result[0]
    result.insert(0,len(result))
    return result

def heuristique_arrondi2(H,data ,NB):
    result = heuristique_arrondi(H,data)
    return descente_stochastique(data, result,NB)

def convertir_list(sub_lists,data):
    sub_lists2 = []
    for l in sub_lists:
        sub_data = []
        for picture in l:
            sub_data.append((data[picture[0]]))
        sub_lists2.append(sub_data)
    return sub_lists2

def apply_greedy_all(sub_lists):
    sub_lists2 = []
    for l in sub_lists:
        H,V = separerH_V(l)
        print(len(H))
        print("V")
        print(len(V))
        result = glouton2(H,V)
        result.pop(0)
        sub_lists2.append(result)
    return sub_lists2

def ordonnancement(sub_lists,data):
    result = []
    result.append(sub_lists.pop(0))
    i = 0
    while(sub_lists):
        max_transi = 0
        max_position = 0
        for j in range(len(sub_lists)):
            k = evalCouple2(result[i][0],sub_lists[j][0],data)
            if(k>max_transi):
                max_transi = k
                max_position = j
                print("Changement")
        result.append(sub_lists.pop(max_position))
    result = [photo for souslist in result for photo in souslist]
    result.insert(0,len(result))
    return result
        

def notre_methode(H,V,len_slice,data,nb):
    old_result = glouton2(H,V)
    print("Evaluation avant:" + str(evaluation(data,old_result,nb)))
    old_result.pop(0)
    sub_lists = [old_result[i:i+len_slice] for i in range(0,len(old_result),len_slice)]
    sub_lists = convertir_list(sub_lists,data)
    sub_lists = apply_greedy_all(sub_lists)
    result = ordonnancement(sub_lists,data)
    print("Evaluation apres:" + str(evaluation(data,result,nb)))
    
def comparaison_des_methodes_H(data,timeout,pl = False):
    result = []
    taille = len(data)
    result.append([taille/10,taille*20/100,taille*30/100,taille*40/100,taille*50/100,taille*60/100,taille*70/100,taille*80/100,taille*90/100,taille])
    # resultats des methodes gloutonnes
    vec=[]
    print("glouton1")
    vec.append("glouton1")
    HList=[]
    for i in range(10,110,10):
        H,V = separerH_V(data[ : int(len(data)*i/100) ])
        HList.append(H)
        t1 = t.time()
        r = glouton(H,[])
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i)])
    
        
        if(time > timeout):
            for j in range(int((110- i)/10)  -1):
                vec.append("TIMEOUT")
            break
    result.append(vec)


    vec=[]
    vec.append("glouton1 + stoch1")
    print("glouton1 + stoch1")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton(HList[i],[])
        r = descente_stochastique(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton1 + stoch2")
    print("glouton1 + stoch2")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton(HList[i],[])
        r = descente_stochastique2(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton2")
    print("glouton2")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton2(HList[i],[])
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton2 + stoch1")
    print("glouton2 + stoch1")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton2(HList[i],[])
        r = descente_stochastique(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton2 + stoch2")
    print("glouton2 + stoch2")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton2(HList[i],[])
        r = descente_stochastique2(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    if(pl):
        vec=[]
        vec.append("pl")
        print("pl")
        for i in range(len(HList)):
            t1 = t.time()
            r = pl_binary(HList[i],data)
            t2 = t.time()
            time = t2-t1
            vec.append([time,evaluation(data,r,i*10)])
        
            
            if(time > timeout):
                for j in range(10- i):
                    vec.append("TIMEOUT")
                break
        result.append(vec)
        
    vec=[]
    vec.append("Heuristique")
    print("Heuristique")
    for i in range(len(HList)):
        t1 = t.time()
        r = heuristique_arrondi(HList[i],data)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("Heuristique + stoch 1")
    print("Heuristique + stoch 1")
    for i in range(len(HList)):
        t1 = t.time()
        r = heuristique_arrondi2(HList[i],data, i *10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("Heuristique + stoch 2")
    print("Heuristique + stoch 2")
    for i in range(len(HList)):
        t1 = t.time()
        r = heuristique_arrondi(HList[i],data)
        r = descente_stochastique2(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
        
    return result



def comparaison_des_methodes(data,timeout):
    result = []
    taille = len(data)
    result.append([taille/10,taille*20/100,taille*30/100,taille*40/100,taille*50/100,taille*60/100,taille*70/100,taille*80/100,taille*90/100,taille])
    # resultats des methodes gloutonnes
    vec=[]
    print("glouton1")
    vec.append("glouton1")
    HList=[]
    for i in range(10,110,10):
        H,V = separerH_V(data[ : int(len(data)*i/100) ])
        HList.append([H,V])
        t1 = t.time()
        r = glouton(H,V)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i)])
    
        
        if(time > timeout):
            for j in range(int((110- i)/10)  -1):
                vec.append("TIMEOUT")
            break
    result.append(vec)


    vec=[]
    vec.append("glouton1 + stoch1")
    print("glouton1 + stoch1")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton(HList[i][0],HList[i][1])
        r = descente_stochastique(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton1 + stoch2")
    print("glouton1 + stoch2")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton(HList[i][0],HList[i][1])
        r = descente_stochastique2(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton2")
    print("glouton2")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton2(HList[i][0],HList[i][1])
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton2 + stoch1")
    print("glouton2 + stoch1")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton2(HList[i][0],HList[i][1])
        r = descente_stochastique(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
    vec=[]
    vec.append("glouton2 + stoch2")
    print("glouton2 + stoch2")
    for i in range(len(HList)):
        t1 = t.time()
        r = glouton2(HList[i][0],HList[i][1])
        r = descente_stochastique2(data,r,i*10)
        t2 = t.time()
        time = t2-t1
        vec.append([time,evaluation(data,r,i*10)])
    
        
        if(time > timeout):
            for j in range(10- i):
                vec.append("TIMEOUT")
            break
    result.append(vec)
    
        
    return result
   
    
    

filename = "c_memorable_moments.txt"
nb = 10
data = lecture_fichier(filename,nb)
H,V = separerH_V(data)
result = glouton2(H,V)
notre_methode(H,V,5,data,np)
#print(comparaison_des_methodes(data,20))

