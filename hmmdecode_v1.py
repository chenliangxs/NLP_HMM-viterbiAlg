# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 12:33:46 2017

@author: yanbaliang
"""
"""
Read from hmmmodel and tag the input data
"""

import sys
testFile=sys.argv[1]

import math

"""
import the model file
"""
hmmTran={}
hmmTran["start"]={}
hmmEmit={}
tagList=[]
tagNo=0
with open("hmmmodel.txt") as model_file:
    model_data=model_file.readlines()
    tagNo=int(model_data[0])
    print(tagNo)
    for singleTag in model_data[1:tagNo+1]:
        sTag=singleTag[0:2]
        tagList.append(sTag)
        hmmTran[sTag]={}
        hmmEmit[sTag]={}
        #print(singleTag)
    transLineNo=tagNo*(tagNo+1)
    for transition in model_data[(tagNo+1):(tagNo+1+transLineNo)]:
        tranInfo=transition.split( )
        preTag=tranInfo[0]
        curTag=tranInfo[1]
        tranProb=math.log10(float(tranInfo[2]))
        #print(preTag+" "+curTag+" "+str(tranProb)+'\n')
        hmmTran[preTag][curTag]=tranProb
    for emission in model_data[(tagNo+1+transLineNo):]:
        emitInfo=emission.split()
        emitTag=emitInfo[0]
        emitWord=emitInfo[1]
        emitProb=math.log10(float(emitInfo[2]))
        hmmEmit[emitTag][emitWord]=emitProb
        
"""
classify input data
"""

class Node:
    def __init__(self):
        self.tag=""
        self.prob=-10
        self.word=""
        self.pre=None

with open(testFile) as testData:
    output=open("hmmoutput.txt","w")
    test_lines=testData.readlines()
    for test_line in test_lines:
        test_words=test_line.split( )
        col=len(test_words)
        row=tagNo
        matrix=[[Node() for j in range(col)] for i in range(row)]
        for i in range(row):      #initial 2D node array
            for j in range(col):
                matrix[i][j].tag=tagList[i]
                matrix[i][j].word=test_words[j]
        for i in range(row):     #initial start
            matrix[i][0].prob=hmmTran["start"][tagList[i]]
            if test_words[0] in hmmEmit[tagList[i]].keys():
                matrix[i][0].prob+=hmmEmit[tagList[i]][test_words[0]]
            else:
                matrix[i][0].prob=-10
        for j in range(1,col):
            print(j)
            for i in range(row):
                for x in range(row):
                    pre_prob=matrix[x][j-1].prob+hmmTran[matrix[x][j-1].tag][matrix[i][j].tag]
                    if matrix[i][j].word in hmmEmit[matrix[i][j].tag].keys():
                        pre_prob+=hmmEmit[matrix[i][j].tag][matrix[i][j].word]
                    else:
                        pre_prob=-10
                    matrix[i][j].prob=max(pre_prob,matrix[i][j].prob)
                    if matrix[i][j].prob==pre_prob:
                        matrix[i][j].pre=matrix[x][j-1]
        """
        maxPos=0
        maxProb=-10
        for i in range(row):
            maxProb=max(maxProb, matrix[i][col-1].prob)
            if maxProb==matrix[i][col-1].prob:
                maxPos=i
        """
        """
        tag_sequence=""
        maxNode=matrix[maxPos][col-1]
        for j in range(col-1,-1,-1):
            tag_sequence=maxNode.tag+" "+tag_sequence
            maxNode=maxNode.pre
        tag_result=tag_sequence.split( )
        tagged=""
        for i in range(col):
            tagged+=test_words[i]+"/"+tag_result[i]+" "
        """
        """
        output.write(str(maxPos)+" "+str(maxProb)+'\n')
    output.close()
    """


        for i in range(row):
            for j in range(col):
                info=matrix[i][j].word+"/"+matrix[i][j].tag+str(matrix[i][j].prob)
                output.write(info+" ")
            output.write('\n')
    output.close()

"""
output=open("hmmoutput.txt","w")
for pre_Tag in hmmTran.keys():
    for cur_Tag in hmmTran[pre_Tag].keys():
        tran_Prob=pre_Tag+" "+cur_Tag+" "+str(hmmTran[pre_Tag][cur_Tag])
        output.write(tran_Prob+'\n')
for emit_tag in hmmEmit.keys():
    for emit_word in hmmEmit[emit_tag].keys():
        emit_prob=emit_tag+" "+emit_word+" "+str(hmmEmit[emit_tag][emit_word])
        output.write(emit_prob+'\n')
output.close()
"""
