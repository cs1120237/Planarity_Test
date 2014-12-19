import math
import string, sys
from sys import stdin

fin = open('input.txt', 'r')
lines = fin.readlines()
fin.close()
num_vertex = lines[0]
g = [[]]*int(num_vertex)
for l in range(1,len(lines)):
	line = lines[l]
	line = line.split()
	g[int(line[0])] = g[int(line[0])] + [int(line[1])]
	g[int(line[1])] = g[int(line[1])] + [int(line[0])]

	
#g=[[3,4,5],[3,4,5],[3,4,5],[0,1,2],[0,1,2],[0,1,2]]
g = map(sorted, g)

def find_all_paths(grp, start_vertex, end_vertex, path=[]): 
	path = path + [start_vertex]
	if start_vertex == end_vertex:
		return [path]
	if start_vertex not in range(0,len(grp)):
		return []
	paths = []
	for vertex in grp[start_vertex]:
		if vertex not in path:
			extended_paths = find_all_paths(grp,vertex, end_vertex,path)
			for p in extended_paths: 
				paths.append(p)
	return paths

#print find_all_paths(g,1,4)

def fltpaths(hgrp,pathlist):
	ans=[]
	for i in range(0,len(pathlist)):
		fl=1
		if(len(pathlist[i])==2):
			if( len(hgrp[pathlist[i][0]])==0 or len(hgrp[pathlist[i][1]])==0 or ( (pathlist[i][0]) in hgrp[pathlist[i][1]] ) ):
				fl=0
		else:	
			for j in pathlist[i][1:len(pathlist[i])-1]:
				if(len(hgrp[j])>0):
					fl=0
					break
		if(fl==1):
			ans.append(pathlist[i])
	return ans

def fndfrg(hgrp):
	frgmnts=[]
	for i in range(0,len(hgrp)):
		if(len(hgrp[i])>0):
			for j in range(i+1,len(hgrp)):
				if(len(hgrp[j])>0):
					frgmnts=frgmnts+(fltpaths(hgrp,find_all_paths(g,i,j)))
	return frgmnts


def getfragments(hgrp):
	oldfrg=fndfrg(hgrp)
	ans=[]
	for pth in oldfrg:
		new=[[]]*len(hgrp)
		for i in range(0,len(pth)):
			if(i>0):
				#print new[pth[i]]
				new[pth[i]]=new[pth[i]]+[pth[i-1]]
			if(i<(len(pth)-1)):
				#print new[pth[i]]
				new[pth[i]]=new[pth[i]]+[pth[i+1]]
		ans.append(new)
	return ans
def findCycle(graph):
    numverts = len(graph)
    visited = [False for i in range(numverts+1)]
    cycle = [0]
    findCycle0(graph,0, visited, cycle)
    return (toGraph(cycle, len(graph)),[(0,cycle), (1,cycle)])
def toGraph(cycle, lengthofgraph):
    length = len(cycle)
    gr = [[] for i in range(lengthofgraph)]
    for i in range(length):
        gr[cycle[i]].append(cycle[(i+1)%length])
        if(i != 0):
            gr[cycle[i]].append(cycle[(i-1)])
        else:
            gr[cycle[i]].append(cycle[(length-1)])
    return gr
def findCycle0(graph,start, visited, cycle):
    visited[start] = True
    for child in graph[start]:
        if(child == 0 and len(cycle) > 2):
            return True;
        elif(not visited[child]):
            cycle.append(child)
            result = findCycle0(graph, child, visited, cycle)
            if(result == True):
                return True
            else:
                result.remove(child)
    return False
#print findCycle(graph)
def getEndPoints(frag):
    v = []
    for i in range(len(frag)):
        if(len(frag[i]) == 1):
            v.append(i)
    return v
def getall(frag):
    v = []
    for i in range(len(frag)):
        if(len(frag[i]) > 1):
            v.append(i)
    return v

def update (face,frag):
    v = getEndPoints(frag)
    vs = getall (frag)
    mark1,mark2=0,0
    if face[0] == 0:
        for i in range(len(face[1])):
            if face[1][i] == v[0]:
                mark1 = i
            elif face[1][i] == v[1]:
                mark2 = i
      #      else:
        if (mark2<=mark1):
            temp = mark1
            mark1 = mark2
            mark2 = temp
        F1 = face[1][:(mark1+1)] + vs + face[1][mark2:]
        F2 = face[1][mark1:(mark2+1)] + vs
        
        return [(0,F1),(0,F2)]
    else:
        for i in range(len(face[1])):
            if face[1][i] == v[0]:
                mark1 = i
            elif face[1][i] == v[1]:
                mark2 = i
        if (mark2<=mark1):
            temp = mark1
            mark1 = mark2
            mark2 = temp
        F1 = face[1][:(mark1+1)] + vs + face[1][mark2:]
        F2 = face[1][mark1:(mark2+1)] + vs
        return [(1,F1),(0,F2)]
                

def getFaces(f, b):
    ans = []
    for f_ in f:
        flag = True
        for i in range(len(b)):
            if(b[i] != [] and len(b[i]) == 1):
                flag = (i in f_[1])
                if(flag == False):
                    break
        if(flag == True):
            ans.append(f_)
    return ans
def dounion (graph1, graph2):
    ans = []
    for i in range(0,len(graph1)):
        ans.append(graph1[i]+filter(lambda x:x not in graph1[i], graph2[i]))
    return ans    
def testPlaner(graph):
    v = len(graph)
    e = sum(map(len, graph))/2
    if(e >= 3*v-6):
        return False
    (h, f) = findCycle(graph)
    h = map(sorted, h)
    while(h != graph):
        beta = getfragments(h)
        fofb = [[] for i in range(len(beta))]
        for i in range(len(beta)):
            fofb[i] = (getFaces(f,beta[i]))
        b0 = 0
        for i in range(len(beta)):
            if(fofb[i] == []):
                return False
            if(len(fofb[i])  == 1):
                b0 = i
                break
        face = fofb[b0]
        frag = beta[b0]
        #h = dounion(h, dounion(frag, toGraph(face[1], len(graph))))
        h = dounion(h, frag)
        h = map(sorted, h)
        new_f = update(face[0],frag)
        f.remove(face[0])
        f = f + new_f
    return True
result = testPlaner(g)
if result == True:
	print 'Planar'
else:
	print 'NonPlanar'
