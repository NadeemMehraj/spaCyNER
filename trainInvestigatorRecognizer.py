# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 13:09:20 2019

@author: applied informatics
"""

import os
import random
import pickle
import spacy
from spacy.util import minibatch, compounding

currentDir = os.path.dirname(os.path.abspath(__file__))
trainDataCount = 1500
n_iter = 20
batchSize = 50

def trainInvestigatorRecognizer():
    '''
    This function trains a blank spacy model to recognize investigator entities
    The function loads the pre created training data from the current directory
    and saves the trained model to the current directory
    '''
    with open(os.path.join(currentDir,'spaCyTrainDataNonEmptyEntities.txt'),'rb') as pf:
        TRAIN_DATA = pickle.load(pf)
        
    nlp = spacy.blank("en")
    print("Created blank 'en' model")
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
        
    else:
        ner = nlp.get_pipe("ner")

    ner.add_label('INVESTIGATOR')
    
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    with nlp.disable_pipes(*other_pipes):
        nlp.begin_training()

    for itn in list(range(n_iter)):
        random.shuffle(TRAIN_DATA)
        losses = {}
        batches = minibatch(TRAIN_DATA, size=batchSize)
        
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

    nlp.to_disk(currentDir)
    print("Saved model to", currentDir)
    
if __name__ == '__main__':
    trainInvestigatorRecognizer()

