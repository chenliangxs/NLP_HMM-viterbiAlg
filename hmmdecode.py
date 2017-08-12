# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 21:28:30 2017

@author: yanbaliang
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
vocab=set()
tagNo=0
with open("hmmmodel.txt") as model_file:
    model_data=model_file.readlines()
    tagNo=int(model_data[0])
    for singleTag in model_data[1:tagNo+1]:
        sTag=singleTag[0:2]
        tagList.append(sTag)
        hmmTran[sTag]={}
        hmmEmit[sTag]={}
    transLineNo=tagNo*(tagNo+1)
    for transition in model_data[(tagNo+1):(tagNo+1+transLineNo)]:
        tranInfo=transition.split( )
        preTag=tranInfo[0]
        curTag=tranInfo[1]
        tranProb=math.log(float(tranInfo[2]))
        hmmTran[preTag][curTag]=tranProb
    for emission in model_data[(tagNo+1+transLineNo):]:
        emitInfo=emission.split()
        emitTag=emitInfo[0]
        emitWord=emitInfo[1]
        vocab.add(emitWord)
        emitProb=math.log(float(emitInfo[2]))
        hmmEmit[emitTag][emitWord]=emitProb

#creat transition probability matrix
tranProbs=[[0 for j in range(tagNo)] for i in range(tagNo)]
for i in range(tagNo):
    for j in range(tagNo):
        tranProbs[i][j]=hmmTran[tagList[i]][tagList[j]]

output=open("hmmoutput.txt","w")
with open(testFile) as testData:
    test_lines=testData.readlines()
    for test_line in test_lines:
        test_words=test_line.split( )
        col=len(test_words)
        row=tagNo
        probMatrix=[[float('-inf') for j in range(col)] for i in range(row)]
        backpointer=[[0 for j in range(col)] for i in range(row)]
        first_word=test_words[0]
        if first_word in vocab:
            for i in range(row):
                if first_word in hmmEmit[tagList[i]]:
                    probMatrix[i][0]=hmmTran["start"][tagList[i]]+hmmEmit[tagList[i]][first_word]
                backpointer[i][0]=0
        else:
            for i in range(row):
                probMatrix[i][0]=hmmTran["start"][tagList[i]]
            backpointer[i][0]=0

        for j in range(1,col):
            emit_word=test_words[j]
            if emit_word in vocab:
                for i in range(row):
                    if emit_word in hmmEmit[tagList[i]]:
                        for x in range(row):
                            probMatrix[i][j]=max(probMatrix[i][j],probMatrix[x][j-1]+tranProbs[x][i])
                            if probMatrix[i][j]==probMatrix[x][j-1]+tranProbs[x][i]:
                                backpointer[i][j]=x
                        probMatrix[i][j]+=hmmEmit[tagList[i]][emit_word]
            else:
                for i in range(row):
                    for x in range(row):
                        probMatrix[i][j]=max(probMatrix[i][j],probMatrix[x][j-1]+tranProbs[x][i])
                        if probMatrix[i][j]==probMatrix[x][j-1]+tranProbs[x][i]:
                            backpointer[i][j]=x

        maxProb=float('-inf')
        maxPos=0
        for i in range(row):
            maxProb=max(maxProb,probMatrix[i][col-1])
            if maxProb==probMatrix[i][col-1]:
                maxPos=i
                
        res=test_words[col-1]+"/"+tagList[maxPos]
        maxPos=backpointer[maxPos][col-1]
        for j in range(col-2,-1,-1):
            res=test_words[j]+"/"+tagList[maxPos]+" "+res
            maxPos=backpointer[maxPos][j]
        output.write(res+'\n')
output.close()
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      