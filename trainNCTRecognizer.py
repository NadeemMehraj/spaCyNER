# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:28:08 2019

@author: applied informatics
"""

import os
import random
import pickle
import spacy
from spacy.util import minibatch, compounding

currentDir = os.path.dirname(os.path.abspath(__file__))
trainingDataDir = os.path.join(currentDir,'ner_training_data')
outputDir = os.path.join(currentDir,'.\\ner_models\\nct_id')
LABELS = ['NCT','ID']
n_iter = 40

def trainNCTRecognizer():
    '''
    This function trains a blank spacy model to recognize investigator entities
    The function loads the pre created training data from the current directory
    and saves the trained model to the current directory
    '''
    with open(os.path.join(trainingDataDir,'training_nct_id.txt'),'rb') as pf:
        print("Reading: ", os.path.join(trainingDataDir,'training_nct_id.txt'))
        TRAIN_DATA = pickle.load(pf)
        
    print('*'*50)
    print(len(TRAIN_DATA))
    input()
        
    TRAIN=[]
    
    #Remove newlines
    for data in TRAIN_DATA[:]:
        (item,d)=data[0].replace('\n',' ').replace('\t',' '),data[1]
        TRAIN.append((item,d))
    
    len(TRAIN)
    input()
    TRAIN_DATA = TRAIN
    print(len(TRAIN_DATA))
    input()
        
    nlp = spacy.blank("en")
    print("Created blank 'en' model")
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
        
    else:
        ner = nlp.get_pipe("ner")

    for label in LABELS:
        ner.add_label(label)
    
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    with nlp.disable_pipes(*other_pipes):
        nlp.begin_training()

    for itn in list(range(n_iter)):
        random.shuffle(TRAIN_DATA)
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        
        for batch in batches:
            texts, annotations = zip(*batch)
            
            nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
        print("Iteration #",itn + 1)
        print("Losses", losses)

    nlp.to_disk(outputDir)
    print("Saved model to", outputDir)
    
if __name__ == '__main__':
    trainNCTRecognizer()

