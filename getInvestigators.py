# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 18:59:28 2019

@author: applied informatics
"""
import simplejson
import glob
import os
import re
import pickle

xmlDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'nerXMLData')
xmlFiles = glob.glob(xmlDir + '\\*')
fileNameInvestigators = []
investigatorRe = re.compile('Investigator')

from ctgov_mm import ClinicalTrialDataManager

def getInvestigators():
    '''
    This function parses NCT XML files, extracting investigator names in 
    overall_official tag.For each file containing investigator, a tuple of
    NCT ID and investigator names is created and added to a list. The final
    list is dumped to the current directory
    '''
    #ctdm = ClinicalTrialDataManager(type = 'xml', source = '.\\nerXMLData\\NCT00001305.xml',params = 'local')
    ctdm = ClinicalTrialDataManager()
    for file in xmlFiles:
        #print("File: ",file)
        try:
            ctdm.set_source(file)
            investigators = []
            overall_officials = ctdm.get_overall_officials()
            
            for official in overall_officials:
                if 'role' in official and investigatorRe.search(official['role'],re.IGNORECASE) is not None and 'name' in official:
                    investigators.append(official['name'].split(',')[0])
                    
            if len(investigators) != 0:
                fileNameInvestigators.append((os.path.basename(file).replace('.xml',''),investigators))
        except:
            pass
    
    with open('.\\fileNameInvestigators.txt', 'wb') as pf:
        pickle.dump(fileNameInvestigators,pf)
    
    print(len(fileNameInvestigators))
    
if __name__ == '__main__':
    getInvestigators()