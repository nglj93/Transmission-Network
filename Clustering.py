#! usr/bin/env python3.2

import re
import csv
from datetime import datetime,date,time

def readFiles(dateFile,dotFile):
	
	input1=open(dateFile,"r")
	nodereader= csv.reader(input1)
	input2=open(dotFile,"r")
	
		
	return nodereader, input2



def runFilter(outFileName,daysInterval,dateFile,colorTF,widthTF,nodereader,input2):
	
	header=next(nodereader)
	print(header)
	
	if widthTF==True:
		virusLoadUnit=float(header[3])
		
	color="white"
	width=0.75
	output=open(outFileName,"w")


	nodesDate={}
	nodesExistence={}
	nodesColor={}
	nodesWidth={}

	for record in nodereader: # record [nodes ID , date, color, virus Load] virus load will reflect on zthe size of the node
		d=datetime.strptime(record[1],"%d/%m/%Y")
		nodesDate[record[0]]=d
		if colorTF==True:
			if record[2]!="":
				nodesColor[record[0]]=record[2]
			else:
				nodesColor[record[0]]=color
		else:
			nodesColor[record[0]]=color
		
		if widthTF==True:
			if record[3]!="":
				nodesWidth[record[0]]=float(record[3])/virusLoadUnit
			else:
				nodesWidth[record[0]]=width
		else:
			nodesWidth[record[0]]=width
		

	nodesInfo=[]
	edgesInfo=[]
	count=0
	output.write('digraph network{\noverlap=scale;\nsplines =line;\noutputorder = edgesfirst;\nedge [len=5.0];\nnode[style=filled];\nranksep=2.8;\nfontname="Times-Roman";\n')
	for line in input2:
		if line.find('->')!=-1:
			count+=1
			match=re.search('\"(.*?)\" -> \"(.*?)\"',line)
			node1=match.group(1)
			node2=match.group(2)
			if count %100 ==0:
				print(count,"s edges have been processed")
			if node1 in nodesDate.keys() and node2 in nodesDate.keys(): # nodes with dates info
				if nodesDate[node2]>nodesDate[node1]:
					if (nodesDate[node2]-nodesDate[node1]).days<daysInterval:
						edgesInfo.append('"%s" -> "%s" [style="bold" label = "" arrowhead = "normal" fillcolor= "white"];\n'%(node1,node2))
						if node1 not in nodesInfo:
							nodesInfo.append(node1)
						if node2 not in nodesInfo:
							nodesInfo.append(node2)
					
						#output.write('"%s" -> "%s" %s'%(node1,node2,line[end:])) # filter out those above maximum days
					
				elif nodesDate[node1]>nodesDate[node2]:
					if (nodesDate[node1]-nodesDate[node2]).days<daysInterval:
						edgesInfo.append('"%s" -> "%s" [style="bold" label = "" arrowhead = "normal" fillcolor= "white"];\n'%(node2,node1))
						if node1 not in nodesInfo:
							nodesInfo.append(node1)
						if node2 not in nodesInfo:
							nodesInfo.append(node2)
					
						#output.write('"%s" -> "%s" %s'%(node2,node1,line[end:])) # filter out those above maximum days
					
				else:
					edgesInfo.append('"%s" -> "%s" [style="dotted" label = "" arrowhead = "none" fillcolor= "white"];\n'%(node1,node2))
					if node1 not in nodesInfo:
						nodesInfo.append(node1)
					if node2 not in nodesInfo:
						nodesInfo.append(node2)
					
					
				
			else:
				edgesInfo.append('"%s" -> "%s" [style="bold" label = "" arrowhead = "none" fillcolor= "white"];\n'%(node1,node2)) # for those without date info
			continue # since already been written into edges

		
		
		elif re.search('fillcolor .* shape',line)!=None:
			continue
			
		elif line.startswith('}'):
			for node in nodesInfo:
				output.write('"%s" [label = "%s", fillcolor = "%s", shape = circle, width = %.6f];\n'%(node,node,nodesColor[node],nodesWidth[node]))
			for edge in edgesInfo:
				output.write(edge)

			
			output.write("}")
			
							

	
	input2.close()
	output.close()

	return len(edgesInfo)





