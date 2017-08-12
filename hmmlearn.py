# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 20:55:40 2017

@author: yanbaliang
"""

"""
Read training data and build the model
The model has transition probability: tag->tag
and emission probability: tag->word
"""
import sys
tfile=sys.argv[1]

#read input file

tran_dict={}  # dictionary store transitions
tran_dict["start"]={}
emit_dict={}  # dictionary store emissions
tagList = set()
"""
build up the count dictionary
"""
with open(tfile) as train_file:
    data_lines=train_file.readlines()
    for data_line in data_lines:
        word_N_tag = data_line.split( )
        first_tag=word_N_tag[0][len(word_N_tag[0])-2:]
        tagList.add(first_tag)
        first_word=word_N_tag[0][0:len(word_N_tag[0])-3]
        if first_tag in tran_dict["start"]:
            tran_dict["start"][first_tag]+=1
        else:
            tran_dict["start"][first_tag]=1
        if first_tag in emit_dict:
            if first_word in emit_dict[first_tag]:
                emit_dict[first_tag][first_word]+=1
            else:
                emit_dict[first_tag][first_word]=1
        else:
            emit_dict[first_tag]={first_word: 1}
        i=1;
        while i<len(word_N_tag):
            curSeg = word_N_tag[i]
            preSeg = word_N_tag[i-1]
            i=i+1
            preTag = preSeg[len(preSeg)-2 :]
            curTag = curSeg[len(curSeg)-2 :]
            curWord = curSeg[0: len(curSeg)-3]
            tagList.add(curTag)
            if preTag in tran_dict:
                if curTag in tran_dict[preTag]:
                    tran_dict[preTag][curTag]+=1
                else:
                    tran_dict[preTag][curTag]=1
            else:
                tran_dict[preTag]={curTag: 1}
            if curTag in emit_dict:
                if curWord in emit_dict[curTag]:
                    emit_dict[curTag][curWord]+=1
                else:
                    emit_dict[curTag][curWord]=1
            else:
                emit_dict[curTag]={curWord: 1}

"""
calculate the transition probability and emission probability
"""
tran_prob={}
emit_prob={}
totalTag=len(tagList)
tran_prob["start"]={}
 #calculate the start probability
for firstTag in tagList:  #count total for start transition
    if firstTag in tran_dict["start"].keys():
        totalTag+=tran_dict["start"][firstTag]
for firstTag in tagList:
    tranProb=1
    if firstTag in tran_dict["start"].keys():
        tranProb=1.0*(tran_dict["start"][firstTag]+1)/totalTag
    else:
        tranProb=1.0/totalTag
    #print(firstTag)
    tran_prob["start"][firstTag]=tranProb

#calculate all possible tag to tag transition
for pre_tag in tagList:
    totalTag=len(tagList)
    tran_prob[pre_tag]={}
    if pre_tag in tran_dict.keys():
        for follow_tag in tran_dict[pre_tag].keys():
            totalTag+=tran_dict[pre_tag][follow_tag]
        for follow_tag in tagList:
            tranProb=1
            if follow_tag in tran_dict[pre_tag].keys():
                tranProb=1.0*(tran_dict[pre_tag][follow_tag]+1)/totalTag
            else:
                tranProb=1.0/totalTag
            tran_prob[pre_tag][follow_tag]=tranProb
    else:
        for follow_tag in tagList:
            tranProb=1.0/totalTag
            tran_prob[pre_tag][follow_tag]=tranProb

#calculate emission probability
for emit_tag in tagList:
    emit_prob[emit_tag]={}
    if emit_tag in emit_dict.keys():
        totalWords=0
        for word in emit_dict[emit_tag].keys():
            totalWords+=emit_dict[emit_tag][word]
        for word in emit_dict[emit_tag].keys():
            emitProb=1.0*emit_dict[emit_tag][word]/totalWords
            emit_prob[emit_tag][word]=emitProb

"""
output the count
"""
output=open("hmmmodel.txt","w")

output.write(str(len(tagList))+'\n')
for tag in tagList:
    output.write(tag+'\n')
'''
for preTag in tran_dict.keys():
    for curTag in tran_dict[preTag].keys():
        tranCount = preTag+"->"+curTag+": "+str(tran_dict[preTag][curTag])
        output.write(tranCount+'\n')
for tag in emit_dict.keys():
    for word in emit_dict[tag].keys():
        emitCount = tag+"->"+word+": "+str(emit_dict[tag][word])
        output.write(emitCount+'\n')
'''

#output.write("transition probability"+'\n')
for preTag in tran_prob.keys():
    for curTag in tran_prob[preTag].keys():
        tranProb = preTag+" "+curTag+" "+str(tran_prob[preTag][curTag])
        output.write(tranProb+'\n')
        
#output.write("emission probability"+'\n')
for emitTag in emit_prob.keys():
    for cur_word in emit_prob[emitTag].keys():
        emitProb = emitTag+" "+cur_word+" "+str(emit_prob[emitTag][cur_word])
        output.write(emitProb+'\n')
output.close()        
        
        

