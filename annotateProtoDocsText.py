# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:32:41 2019

@author: applied informatics
"""

import os
import glob
import pickle
import re

textFileDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'protocolDocumentsTextFull')
textFiles = glob.glob(textFileDir + '\\*.txt')
textFilesString = ','.join(textFiles)
textExt = '.txt'
currentDir = os.path.dirname(os.path.abspath(__file__))
trainData = []
entityType = 'INVESTIGATOR'
limitText = 'page no 5'
#investigatorRe = re.compile('INVESTIGATOR')


def annotateProtoDocsText():
    '''
    This function reads protocol documents text files one by one and annotates
    text in the first five pages of the file to create training data for 
    training spaCy model for recognition of investigator entities. The created
    training data is dumped to the current directory
    '''
    
    numberOfFilesAnnotated = 0
    with open('fileNameInvestigators.txt','rb') as pf:
        fileNameInvestigators = pickle.load(pf)
        
    for item in fileNameInvestigators:
        basename = item[0]
        newBaseNames = getTextFileBaseNames(basename)
        
        for basename in newBaseNames:
            textFileName = os.path.join(textFileDir,basename + textExt)
            #print(textFileName)
            #input()
            
            if os.path.isfile(textFileName):
                print('='*50)
                print('[INFO]: Annotating: ', textFileName)
                with open(textFileName, 'r') as inf:
                    entities = []
                    data = inf.read()
                    limitedData = data[:data.find(limitText)]
                    investigators = item[1]
                    addInvestigators(limitedData,investigators,entities)
                    trainData.append((limitedData,{'entities': entities}))
                numberOfFilesAnnotated += 1
                
    print("*"*50)
    print("[INFO]: Number of files annotated: ",numberOfFilesAnnotated)
    with open('spaCyTrainData.txt','wb') as pf:
        pickle.dump(trainData,pf)
        
def getTextFileBaseNames(basename):
    '''
    This function takes in NCT ID and returns a list of basenames of those 
    protocol documents text files whose base name contains this NCT ID
    '''
    basenameRe = re.compile(basename)
    newBaseNames = []
    spanList = [match.span() for match in basenameRe.finditer(textFilesString)]
    for span in spanList:
        newBaseNameStart = span[0]
        newBaseNameEnd = newBaseNameStart + textFilesString[newBaseNameStart:].find('.txt')
        newBaseNames.append(textFilesString[newBaseNameStart:newBaseNameEnd])
    return newBaseNames
                
def addInvestigators(text,investigators,entities):
    '''
    This function takes in text of protocol documents, finding investigator
    entities in them and returning entity objects as a list
    '''
    for investigator in investigators:
        investigatorSpanList = [match.span() for match in re.finditer(investigator,text,flags = re.IGNORECASE)]
        for span in investigatorSpanList:
            print("[INFO]: Added entity: ",text[span[0]:span[1]])
            entities.append((span[0],span[1],entityType))
            
if __name__ == '__main__':
    annotateProtoDocsText()
        
        