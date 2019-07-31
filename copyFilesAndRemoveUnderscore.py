# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:06:21 2019

@author: applied informatics
"""

import os
import glob
from shutil import copyfile
textFileDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'protocolDocumentsText')
textFiles = glob.glob(textFileDir + '\\*.txt')
textFiles.extend(glob.glob(textFileDir + '\\Batch1\\*.txt'))
textFiles.extend(glob.glob(textFileDir + '\\Batch2\\*.txt'))
textFiles.extend(glob.glob(textFileDir + '\\Batch3\\*.txt'))
outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'protoDocsText')


def copyFiles():
    for filename in textFiles:
        if '_' in os.path.basename(filename):
            newBaseName = removeUnderscoresFromFileName(os.path.basename(filename))
            dst = os.path.join(outDir,newBaseName)
            copyfile(filename,dst)

def removeUnderscoresFromFileName(basename):
    newBaseName = basename.replace('_','')
    return newBaseName
            
if __name__ == '__main__':
    copyFiles()