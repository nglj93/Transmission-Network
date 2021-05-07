#!/usr/bin/env python3.2


'''
DistanceFilter.py created by Ng Liang Jie and Ng Kim Tien || March 2015

Revision:	1) 26 May 2016
		2) 24 June 2016


		1) Adding remove edges & remove nodes based on virus load. 		   
		2) Exporting object using pickle
		   Removing Menu module to Clustering.py
		   Removing MenuV1 module to Clustering.py
		   Create Permutation function for removing Node by edges poportion
		   create load function for network object	


Class	node
	 	edge
	 	network
	 
network	_init_(self)
		getNumNodes(self): # return the number of node
		getNodeIDList(self): #return a list with nodes ID
		getNumEdgtes(self): # return the number of Edges
		removeNode_from_loss_edge(self): #remove node from the loss edge
		loadEdgeNNode(self,pointer1,outputHandle=None,headerTF=False): #read edge information from distance file
		readNodeDate(self,pointerArray,col,outputHandle=None,headerTF=False): # read the Node's date from the csv file
		readNodeColor(self,pointerArray,col,outputHandle=None,headerTF=False): # read the Node's color from the csv file
		readNodeShape(self,pointerArray,col,outputHandle=None,headerTF=False): # read the node shape from the csv file
		readNodeSize(self,pointerArray,col,outputHandle=None,headerTF=False): # read the node size
		readVirusLoad(self,pointerArray,col,outputHandle=None,unit=1000,headerTF=False): #determine the size of the node according to their virus load
		edgeFilter_byDate(self,maxDate=30,outputHandle=True,headerTF=False): #filter the edges by their date onset
		defineCluster(self): # define the cluster group
		getNumClusters(self): # return the number of clusters can be formed
		printClusters(self,handle): # print the clusters in a txt file
		getNodeDegree(self,handle): # get the node Degree
		removeEdge_from_loss_node(self): # remove the edge from their loss node
		generateDot(self,outputHandle): # generate the dot file
		removeNode(self,sampleList,outputHandle=None):
		selectNode_viralLoad(self,viralLoad): # 28 May 2016 added by Liang Jie； select node based on viral load
		clusterSummary(self,outputHandle):
		readPointerArray(self,handle,headerTF=False):
		loadNetwork(self,filename): ## 25 June 2016 added by Liang Jie: load stored obj from file
		
		
Function	inputFile (fileName):
		removeNode_random(network1,proportion,handle):
		outfile (content,filename,filetype=None):
		filterCluster(content,bstrapThre):
		filterDistance(content,clusterFiltered):
		runTn93(AdvancedCommand,command,RunBootstrap,bootstrapNum,saveName):
		menu():
		runFilter(network1,handle,daysFilter,colorNode,widthNode,shapeNode): #input2 contains script for diagraph
		runSfdp(dotFileName):
		menuV1():
		removeEdgeOfNode_random(network1,proportion,nodeID,handle): #28 May 2016 added by Liang Jie; remove the edges by proportion of a node
		removeEdges_viralLoad(network1,viralLoad,proportion):# 28 May 2016 added by Liang Jie； remove the edges of node based on viral load by proportion.
		removeNodes_viralLoad(network1,viralLoad,handle):#31 May 2016 added by Liang Jie; remove node based on viral Load
		
			
		
'''


import csv
from datetime import datetime,date,time
from copy import deepcopy
import random
import sys, os
import pickle
import numpy as np
from scipy import stats


class node:
        def __init__(self,nodeID):
                self.nodeID=nodeID
                self.nodeDate=""
                self.nodeColor="grey"
                self.nodeSize=0.5
                self.nodeShape="ellipse"
                self.label=nodeID
                self.viralLoad=0.0 # 28 May 2016 added by Liang Jie; 

        
        

class edge:
        def __init__(self,node1,node2):
                self.node1=node1
                self.node2=node2
                self.distance=None
                self.direction=None
                self.style="dotted"

class network:
        def __init__(self):
                self.nodes=[]
                self.edges=[]
                self.network_clusters=[]
                self.nodesDegree={}

        def loadNetwork(self,filename): ## 25 June 2016 added by Liang Jie: load stored obj from file
                with open(filename,'rb') as objInput:
                        networkRead = pickle.load(objInput)
	        
                return networkRead

        def getNumNodes(self): # return the number of node
                return len(self.getNodeIDList())
        
        def getNodeIDList(self): #return a list with nodes ID
                nodeIDList=[]
                for oneNode in self.nodes:
                        nodeIDList.append(oneNode.nodeID)
                return nodeIDList
        def getNumEdges(self): # return the number of Edges
                return len(self.edges)

        def removeNode_from_loss_edge(self): #remove node from the loss edge
                tempNodes=[]
                i=0
                while i< len(self.nodes):
                        flag=False
                        for oneEdge in self.edges:
                                if self.nodes[i].nodeID == oneEdge.node1 or self.nodes[i].nodeID == oneEdge.node2:
                                        flag=True
                                        break
                        if flag==False:
                                tempNodes.append(self.nodes[i].nodeID)
                                self.nodes.remove(self.nodes[i])
                                i-=1
                        i+=1
                return tempNodes
                
        def loadEdgeNNode(self,pointer1,outputHandle=None,headerTF=False): #read edge information from distance file
                if headerTF==True:
                        header1=next(pointer1)
                        
                for line in pointer1:
                        if line[0] not in self.getNodeIDList():
                                self.nodes.append(node(line[0]))
                        if line[1] not in self.getNodeIDList():
                                self.nodes.append(node(line[1]))

                        oneEdge=edge(line[0],line[1])
                        oneEdge.distance=line[2]
                        self.edges.append(oneEdge)
                print("Number of Nodes:",self.getNumNodes(),"\n Number of Edges:",self.getNumEdges())
				

        def readNodeDate(self,pointerArray,col,outputHandle=None,headerTF=False): # read the Node's date from the csv file
                
                nodes=self.getNodeIDList()
                if headerTF==True:
                        startPos=1
                else:
                        startPos=0

                for line in pointerArray[startPos:]:
                        #print(line[0],line[1])
                        try:
                                k=nodes.index(line[0])
                                self.nodes[k].nodeDate=datetime.strptime(line[1],"%d/%m/%Y")
                                #print("This is k",k,self.nodes[k].nodeID,"This is the date:%syaya"%(line[1]))
                                #print("This is k",k,self.nodes[k].nodeID,self.nodes[k].nodeDate)

                        except ValueError:
                                continue


        def readNodeColor(self,pointerArray,col,outputHandle=None,headerTF=False): # read the Node's color from the csv file
                if headerTF==True:
                        startPos=1
                else:
                        startPos=0

                nodes=self.getNodeIDList()

                for line in pointerArray[startPos:]:
                        try:
                                k=nodes.index(line[0])
                                self.nodes[k].nodeColor=line[col]
                        except ValueError:
                                continue
                        

        def readNodeShape(self,pointerArray,col,outputHandle=None,headerTF=False): # read the node shape from the csv file
                if headerTF==True:
                        startPos=1
                else:
                        startPos=0

                nodes=self.getNodeIDList()

                for line in pointerArray[startPos:]:
                        try:
                                k=nodes.index(line[0])
                                self.nodes[k].nodeShape=line[col]
                        except ValueError:
                                continue

        def readNodeSize(self,pointerArray,col,outputHandle=None,headerTF=False): # read the node size
                if headerTF==True:
                        startPos=1
                else:
                        startPos=0

                nodes=self.getNodeIDList()

                for line in pointerArray[startPos:]:
                        try:
                                k=nodes.index(line[0])
                                self.nodes[k].nodeSize=float(line[col]) #22 June 2016 change to float
                        except ValueError:
                                continue

        def readVirusLoad(self,pointerArray,col,outputHandle=None,unit=1000,headerTF=False): #determine the size of the node according to their virus load
                if headerTF==True:
                        startPos=1
                else:
                        startPos=0

                nodes=self.getNodeIDList()

                for line in pointerArray[startPos:]:
                        try:
                                k=nodes.index(line[0])
                                self.nodes[k].viralLoad=float(line[col]) #28 May 2016 added by Liang Jie; provided additional info
                        except ValueError:
                                continue
                                                        
                                        
        def edgeFilter_byDate(self,maxDate=30,outputHandle=True,headerTF=False): #filter the edges by their date onset

                nodes=self.getNodeIDList()
                i=0
                while i<len(self.edges):
                        k=nodes.index(self.edges[i].node1)
                        l=nodes.index(self.edges[i].node2)
                        #print(self.edges[i].node1,k,nodes[k],self.nodes[k].nodeDate)
                        #print(self.edges[i].node2,l,nodes[l],self.nodes[l].nodeDate)
                        if self.nodes[k].nodeDate > self.nodes[l].nodeDate:
                                if (self.nodes[k].nodeDate-self.nodes[l].nodeDate).days<maxDate:
                                        self.edges[i].direction='<'
                                        self.edges[i].style="bold"
                                        
                                else:
                                        self.edges.remove(self.edges[i])
                                        i-=1

                        elif self.nodes[k].nodeDate< self.nodes[l].nodeDate:
                                if( self.nodes[l].nodeDate- self.nodes[k].nodeDate).days<maxDate:
                                        self.edges[i].direction='>'
                                        self.edges[i].style="bold"
                                        
                                else:
                                        self.edges.remove(self.edges[i])
                                        i-=1

                        elif self.nodes[k].nodeDate== self.nodes[l].nodeDate:
                                self.edges[i].direction=None
                                self.edges[i].style="bold"

                        i+=1
                                



        def defineCluster(self): # define the cluster group ####### Important ##### Only those with edges are considered in cluster
                edges=self.edges[:]
                network_clusters=[]
                while len (edges)!=0:
                        oneEdge=edges.pop()
                        tempCluster=[]
                        tempTransverse=[oneEdge.node1,oneEdge.node2]
                        while len(tempTransverse)!=0:
                                tempNode=tempTransverse.pop()
                                tempCluster.append(tempNode)
                                i=0
                                while i<len(edges):
                                        if tempNode in [edges[i].node1,edges[i].node2]:
                                                if tempNode != edges[i].node1 and edges[i].node1 not in tempTransverse:
                                                        tempTransverse.append(edges[i].node1)
                                                elif tempNode != edges[i].node2 and edges[i].node2 not in tempTransverse:
                                                        tempTransverse.append(edges[i].node2)
                                                edges.remove(edges[i])
                                                i-=1
                                        i+=1
                        network_clusters.append(tempCluster)

                self.network_clusters=network_clusters
                 
        def getNumClusters(self): # return the number of clusters can be formed
                return len(self.network_clusters)

        def printClusters(self,handle): # print the clusters in a txt file
                #handle.write("Number of clusters : %d\n"%len(self.network_clusters))
                nodes=self.getNodeIDList()
                handle.write("Node,Cluster No,color,size,Shape\n")
                for i in range (0, len(self.network_clusters)):
                        for node in self.network_clusters[i]:
                                k=nodes.index(node)
                                handle.write("%s,%d,%s,%.2f,%s\n"%(node,i+1,self.nodes[k].nodeColor,self.nodes[k].nodeSize,self.nodes[k].nodeShape))
                handle.close()

        def getNodeDegree(self,handle): # get the node Degree
                nodes= self.getNodeIDList()
                edges= self.edges[:]
                self.nodesDegree={}
                handle.write("NodeID,degree\n")
                for node in nodes:
                        tempDegree=0
                        for oneEdge in edges:
                                if node == oneEdge.node1 or node==oneEdge.node2:
                                        tempDegree+=1
                        self.nodesDegree[node]=tempDegree
                        handle.write("%s,%d\n"%(node,tempDegree))
                handle.close()

        def removeEdge_from_loss_node(self): # remove the edge from their loss node
                nodes= self.getNodeIDList()
                i=0
                while i<len(self.edges):
                        if self.edges[i].node1 not in nodes:
                                self.edges.remove(self.edges[i])
                                i-=1
                        elif self.edges[i].node2 not in nodes:
                                self.edges.remove(self.edges[i])
                                i-=1
                        else:
                                i+=1

        def generateDot(self,outputHandle): # generate the dot file
                outputHandle.write('digraph network{\noverlap=scale;\nsplines =line;\noutputorder = edgesfirst;\nedge [len=5.0];\nnode[style=filled];\nranksep=2.8;\nfontname="Times-Roman";\n')
                for node in self.nodes:
                        outputHandle.write('"%s"[label="%s",size="%.3f",fillcolor="%s",shape="%s"];\n'%(node.nodeID,node.nodeID,node.nodeSize,node.nodeColor,node.nodeShape))
                for edge in self.edges:
                        if edge.direction==">":
                                outputHandle.write('"%s"->"%s"[style="%s",label="",arrowhead="normal"];\n'%(edge.node1,edge.node2,edge.style))
                        elif edge.direction=="<":
                                outputHandle.write('"%s"->"%s"[style="%s",label="",arrowhead="normal"];\n'%(edge.node2,edge.node1,edge.style))
                        elif edge.direction==None:
                                outputHandle.write('"%s"->"%s"[style="%s",label="",arrowhead="none"];\n'%(edge.node1,edge.node2,edge.style))
                outputHandle.write("};\n")
                outputHandle.close()

        def removeNode(self,sampleList,outputHandle=None):
                nodes=self.getNodeIDList()
                i=0
                while i<len(self.nodes):
                        if self.nodes[i].nodeID in sampleList:
                                self.nodes.remove(self.nodes[i])
                                i-=1
                        i+=1
                if outputHandle!=None:
                        outputHandle.write("Removed Node\n")
                        for node in sampleList:
                                outputHandle.write("%s\n"%node)
                        print(len(sampleList)," have been removed, ",len(self.nodes)," have been remained")
                
        def clusterSummary(self,outputHandle):
                outputHandle.write("===============Summary=========================\n")
                outputHandle.write("Number of Nodes : %d\n Number of Edges :%d\n"%(len(self.nodes),len(self.edges)))
                outputHandle.write("Number of Clusters: %d\n"%(len(self.network_clusters)))
                outputHandle.write("Size of each cluster: [" +",".join([str(len(x)) for x in self.network_clusters])+"]\n")
                print("===============Summary=========================")
                print("Number of Nodes : %d\n Number of Edges :%d"%(len(self.nodes),len(self.edges)))
                print("Number of Clusters: %d"%(len(self.network_clusters)))
                print("Size of each cluster: [" ,",".join([str(len(x)) for x in self.network_clusters]),"]")
                outputHandle.close()
                
        def selectNode_viralLoad(self,viralLoad): # 28 May 2016 added by Liang Jie； select node based on viral load
                selected_node=[]
                for node in self.nodes:
                        if node.viralLoad<=viralLoad:
                                selected_node.append(node.nodeID)
                                
			
                return selected_node	
				
				

        def readPointerArray(self,handle,headerTF=False):
				
                pointerArray=[]
                if headerTF==True:
                        next(handle)
                                        
                for line in handle:
                        pointerArray.append(line.rstrip().split(","))
                
                return pointerArray
      

		
def removeNode_random(network1,proportion,handle):
	network2=deepcopy(network1)
	nodeList=network2.getNodeIDList()
	k=int(round(len(nodeList)*proportion/100))
	sample=random.sample(nodeList,k)
	network2.removeNode(sample,handle)
	network2.removeEdge_from_loss_node()	
	tempNode=network2.removeNode_from_loss_edge()	
	
	if handle!= None:# 25 June 2016 added by Liang JIe
		print("================= Additional Node Removal ========================")
		print("Additional Removed Node",len(tempNode))
		handle.write("============= Additional Removed Node ==================\n")
		handle.write("Number of Additional Removed Node: %d"%len(tempNode))#28 May 2016 added by Liang Jie ;write the number of additional removal node
		handle.write("Additional Removed Node: [%s]"%",".join(tempNode))#28 May 2016 added by Liang Jie ;write the nodeID for additional removal node             
		
	return network2
	
def removeNodes_viralLoad(network1,viralLoad,handle):#31 May 2016 added by Liang Jie; remove node based on viral Load
	network2=deepcopy(network1)
	nodeList=network2.selectNode_viralLoad(viralLoad)		
	network2.removeNode(nodeList,handle)
	network2.removeEdge_from_loss_node()	
	tempNode=network2.removeNode_from_loss_edge()	
	

	if handle != None:# 25 June 2016 added by Liang JIe
		print("================= Additional Node Removal ========================")
		print("Additional Removed Node",len(tempNode))
		handle.write("============= Additional Removed Node ==================\n")
		handle.write("Number of Additional Removed Node: %d"%len(tempNode))#28 May 2016 added by Liang Jie ;write the number of additional removal node
		handle.write("Additional Removed Node: [%s]"%",".join(tempNode))#28 May 2016 added by Liang Jie ;write the nodeID for additional removal node             
	return network2

	
def removeEdgeOfNode_random(network1,proportion,nodeID): #28 May 2016 added by Liang Jie; remove the edges by proportion of a node
	network2=deepcopy(network1)
	i=0
	affected_edges=[]
	while i<len(network2.edges):
		if nodeID in [network2.edges[i].node1,network2.edges[i].node2]:
			affected_edges.append(i)
		i+=1
		
	k=int(round(len(affected_edges)*proportion/100))
	sample=random.sample(affected_edges,k)
	sample=sorted(sample,reverse=True)
	for index in sample:
		del network2.edges[index]
		
	'''
	for delete multiple items in a list
	1) reverse delete
	2) replace the item (None) and delete all
	3) using enumerator
	
	please refers stack overflow
	
	
	'''

	
	return network2
	

	
def removeEdges_viralLoad(network1,viralLoad,proportion):# 28 May 2016 added by Liang Jie； remove the edges of node based on viral load by proportion.
	selected_node=network1.selectNode_viralLoad(viralLoad)
	network2=deepcopy(network1)
	for nodeID in selected_node:
		network2=removeEdgeOfNode_random(network2,proportion,nodeID)
	
	network2.removeEdge_from_loss_node()	
	network2.removeNode_from_loss_edge()	
	return network2 

	
def inputFile (fileName):
	handle=open(fileName)
	return handle
		


###
	
def outfile (content,filename,filetype=None):
	
	outputHandle=open(filename,'w')
	if filetype=="bs":
		outputHandle.write("ID1,ID2,Boot-strap\n")
	else:
		outputHandle.write("ID1,ID2,Distance\n")
	for clusterID,value in content.items():
		outputHandle.write("%s,%s\n"%(clusterID,value))
	outputHandle.close()


def filterCluster(content,bstrapThre):
	newCluster={}
	for clusterID,value in content.items():
		if (float(value)/1000.0*100.0)>=float(bstrapThre):
			result=float(value)/1000.0*100.0
			newCluster[clusterID]=round(result)
			

	return newCluster

def filterDistance(content,clusterFiltered):
	newCluster={}
	for clusterID,value in content.items():
		if clusterID in clusterFiltered.keys():
			newCluster[clusterID]=value
	
	return newCluster
				
	


def runTn93(AdvancedCommand,command,RunBootstrap,bootstrapNum,saveName):

	rawbootstrap=saveName+" Bootstrap.txt"
	saveasbootstrap=saveName+"BSt.txt"
	saveasfiltered=saveName+"filtered.txt"
	print("Filename:")
	print("Distance:",saveName,".txt")
	print("Bootstrap:",saveasbootstrap)
	print("Filtered Distance:",saveasfiltered)
	cluster={}
	distance={}
		
	file2=os.popen(command)
	for line in file2:
		if line.startswith("ID"):
			continue
		line=line.rstrip()
		line_edited= line.split(",")
		if line_edited[0]<=line_edited[1]:
			clusterGrp=",".join(line_edited[:2])
		else:
			clusterGrp=",".join(line_edited[1::-1])
		distance[clusterGrp]=line_edited[2]
		outfile(distance,saveName+".txt")


	i=0
	print(AdvancedCommand)
	if RunBootstrap=="Y":
		
		while i<1000:
						
			if i%100==0:
				print("Running:",round(float(i/10),2)," %")			
	
			file1=os.popen(AdvancedCommand)
			for line in file1:
				if line.startswith("ID"):
					continue
				#line=line.rstrip()
				line_edited= line.split(",")
				if line_edited[0]<=line_edited[1]:
					clusterGrp=",".join(line_edited[:2])
				else:
					clusterGrp=",".join(line_edited[1::-1])
				if clusterGrp in cluster.keys():
					cluster[clusterGrp]+=1
				else:
					cluster[clusterGrp]=1
			i+=1

	
		clusterFiltered=filterCluster(cluster,bootstrapNum)
		outfile(clusterFiltered,rawbootstrap,"bs")
		outfile(cluster,saveasbootstrap,"bs")
		distanceFiltered=filterDistance(distance,clusterFiltered)
		outfile(distanceFiltered,saveasfiltered)
	else:
		outfile(distance,saveasfiltered)
	


def runFilter(network1,handle,daysFilter,colorNode,widthNode,shapeNode,viralLoadNode): #input2 contains script for diagraph; 1 June 2016 modified by Liang Jie
	network2=deepcopy(network1)
	pointerArray=network2.readPointerArray(handle,True)
	if daysFilter[0]==True:
		print("readNodeDate")
		network2.readNodeDate(pointerArray,daysFilter[2])
		print("edgeFilter_byDate")
		network2.edgeFilter_byDate(daysFilter[1])
		
	if colorNode[0]==True:
		network2.readNodeColor(pointerArray,colorNode[1])
	
	if widthNode[0]==True:
		network2.readNodeSize(pointerArray,widthNode[1])
		
	if shapeNode[0]== True:
		network2.readNodeShape(pointerArray,shapeNode[1])

	if viralLoadNode[0]== True:# 1 June 2016 added by Liang Jie
		network2.readVirusLoad(pointerArray,viralLoadNode[1],unit=1)
		
		
	return network2
		
def runSfdp(dotFileName):
	DotCommand='sfdp -Tpng '+dotFileName +' -o "'+dotFileName+'Figure.png" -Gsize=20,20\!'
	os.system(DotCommand)
		
		
def permutation_test(network1,filename,run_time,confidence,permutation_test_case,prob=0,viralLoad=0.0): #25 June 2016 added by Liang Jie: confidence --> 0.95 : prob -->%
	network2=deepcopy(network1)
	outputHandle=open(filename,'w')
	outputHandle.write("Clusters,Edges,Nodes\n")
	t_run_time=int(run_time*0.1)
	
	numNodesList=[]
	numEdgesList=[]
	numClustersList=[]
	if permutation_test_case=="removeNodeRandom":
		for i in range (0,run_time):
			if i%t_run_time==0:
				print("Running:",round(float(i/t_run_time),2)," %")
			network3=removeNode_random(network2,prob,None)
			numNodesList.append(network3.getNumNodes())
			numEdgesList.append(network3.getNumEdges())
			####### warning ###### only those with edges will form clusters, individual nodes are not considered as cluster
			network3.removeNode_from_loss_edge()			
			network3.defineCluster()
			numClustersList.append(network3.getNumClusters())
			outputHandle.write("%d,%d,%d\n"%(network3.getNumClusters(),network3.getNumEdges(),network3.getNumNodes()))

		printMeanNCI(numNodesList,numEdgesList,numClustersList,confidence,outputHandle)
		
	elif permutation_test_case =="removeEdgesViralLoad":
		for i in range(0,run_time):
			if i%t_run_time==0:
				print("Running:",round(float(i/t_run_time*10),2)," %")
			network3=removeEdges_viralLoad(network2,viralLoad,prob)
			numNodesList.append(network3.getNumNodes())
			numEdgesList.append(network3.getNumEdges())
			####### warning ###### only those with edges will form clusters, individual nodes are not considered as cluster
			network3.removeNode_from_loss_edge()
			network3.defineCluster()
			numClustersList.append(network3.getNumClusters())
			outputHandle.write("%d,%d,%d\n"%(network3.getNumClusters(),network3.getNumEdges(),network3.getNumNodes()))
		printMeanNCI(numNodesList,numEdgesList,numClustersList,confidence,outputHandle)

	elif permutation_test_case =="removeNodesViralLoad":
		for i in range(0,run_time):
			if i%t_run_time==0:
				print("Running:",round(float(i/t_run_time),2)," %")
			network3=removeNodes_viralLoad(network2,viralLoad,None)
			numNodesList.append(network3.getNumNodes())
			numEdgesList.append(network3.getNumEdges())
			####### warning ###### only those with edges will form clusters, individual nodes are not considered as cluster
			network3.removeNode_from_loss_edge()
			network3.defineCluster()				
			numClustersList.append(network3.getNumClusters())
			outputHandle.write("%d,%d,%d\n"%(network3.getNumClusters(),network3.getNumEdges(),network3.getNumNodes()))
		printMeanNCI(numNodesList,numEdgesList,numClustersList,confidence,outputHandle)	


def printMeanNCI(numNodesList,numEdgesList,numClustersList,confidence,outputHandle): #25 June 2016 added by Liang Jie : help to print out the result
	meanNumClusters,meanNumEdges,meanNumNodes=np.mean(numClustersList),np.mean(numEdgesList),np.mean(numNodesList)
	outputHandle.write("mean\n")
	outputHandle.write("%.3f,%.3f,%.3f\n"%(meanNumClusters,meanNumEdges,meanNumNodes))
		
	stdNumClusters,stdNumEdges,stdNumNodes=np.std(numClustersList),np.std(numEdgesList),np.std(numNodesList)
	
	outputHandle.write("std\n")
	outputHandle.write("%.3f,%.3f,%.3f\n"%(stdNumClusters,stdNumEdges,stdNumNodes))

	t_Value=stats.t.ppf((1+confidence)/2.,len(numClustersList)-1)
	
	#standard error measurement
	semNumClusters=stats.sem(numClustersList)
	semNumEdges=stats.sem(numEdgesList)
	semNumNodes=stats.sem(numNodesList)
	
	outputHandle.write("CI\n")
	outputHandle.write("%.3f-%.3f,"%(meanNumClusters-(semNumClusters*t_Value),meanNumClusters+(semNumClusters*t_Value))
	outputHandle.write("%.3f-%.3f,"%(meanNumEdges-(semNumEdges*t_Value),meanNumEdges+(semNumEdges*t_Value))
	outputHandle.write("%.3f-%.3f\n"%(meanNumNodes-(semNumNodes*t_Value),meanNumNodes+(semNumNodes*t_Value))
	
                        
