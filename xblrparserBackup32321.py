# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 13:40:15 2021

@author: jfalk

Take fifty million at getting fucking usable SEC data

Downloading text files from SEC website in XBLR format
Attempting to parse them into something tabular
Crossing my fingers the data is more complete.....

"""

from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir("C:/Users/jfalk/Documents/SECDOCS/cik_dvn")

xblr_string = 'C:/Users/jfalk/Documents/SECDOCS/cik_dvn/10-k/0001564590-18-002582.txt'

DVNDIR = 'C:/Users/jfalk/Documents/SECDOCS/cik_dvn/10-k'

DVNTest = pd.DataFrame(columns=['Symbol', 'Revenue','RevAdded', 'Acceptdttme','Periodend', 'Docfiscyear'])

revenuelist = []
RevAdded = []
Acceptdttme = ''
symbol = ''
Periodend = ''
Docfiscyear = ''

for root, dirs, files in os.walk(DVNDIR):
    if not files:
        continue
    prefix = os.path.basename(root)
    

    for f in files: 
        filename = DVNDIR + '/'+ f
        print(filename)
        revenuelist = []
        RevAdded = []
        Acceptdttme = ''
        symbol = ''
        Periodend = ''
        Docfiscyear = ''
        with open (filename, "r") as myfile:
            data=myfile.read().replace('\n', '')
        soup = BeautifulSoup(data, 'lxml')
        tag_list = soup.find_all()
        for tag in tag_list:
            if tag.name == 'us-gaap:revenues':
                if len(tag.attrs['contextref']) <=30:
                    revenuelist.append(tag.text)
                    RevAdded.append(tag.attrs['contextref'])
            if tag.name == 'dei:tradingsymbol':
                symbol = tag.text
            if tag.name == 'dei:documentperiodenddate':
                Periodend = tag.text
            if tag.name == 'dei:documentfiscalyearfocus':
                Docfiscyear = tag.text
            if tag.name == 'acceptance-datetime':
                Acceptdttme = tag.text
        findict = {"Symbol": symbol, "Revenue":revenuelist, "RevAdded":RevAdded, "Acceptdttme":Acceptdttme,
                   "Periodend":Periodend, 
                   "Docfiscyear":Docfiscyear}
        findf = pd.DataFrame(findict)
        
        DVNTest = DVNTest.append(findf)
        
DVNTestclean = DVNTest.copy()
DVNTestclean = DVNTestclean.drop_duplicates()       

DVNTestclean['RevStart'] = DVNTestclean.RevAdded.str.split('_').str[-2]  
DVNTestclean['RevEnd'] = DVNTestclean.RevAdded.str.split('_').str[-1]  
DVNTestclean['RevStartDte'] = DVNTestclean.RevStart.str[-4:]
DVNTestclean['RevEndDte'] = DVNTestclean['RevEnd'].str[-4:]   
DVNTestclean = DVNTestclean.loc[DVNTestclean.RevEndDte == '1231']       
DVNTestclean = DVNTestclean.loc[DVNTestclean.RevStartDte == '0101']      


DVNFinal = DVNTestclean.groupby(['RevStart', 'RevEnd'], sort=False)['Docfiscyear'].transform(max) == DVNTestclean['Docfiscyear'] 
            
DVNFinallist = DVNTestclean[DVNFinal]

            # try:
            #     numdf = pd.read_csv(filename, delimiter='\t', low_memory=False, header=0)
            #     numdf = numdf.loc[(numdf.qtrs == 1) | (numdf.qtrs==4)]
            #     numdf = numdf.loc[(numdf.iprx==0) & (numdf.dimh == '0x00000000')]
            #     numlist.append(numdf)
            # except:
            #     continue
      
        


with open (xblr_string, "r") as testfile:
    test=testfile.read().replace('\n', '')
    
testsoup = BeautifulSoup(test, 'lxml')
testtag_list = testsoup.find_all()

for tag in testtag_list:
    if tag.name == 'us-gaap:revenues':
        if len(tag.attrs['contextref']) <=30:
            print(tag.attrs['contextref'])

# for tag in tag_list:
#     if tag.name == 'us-gaap:revenues':
#         if tag.attrs['contextref'] == 'C_0001090012_20170101_20171231': 
#             print(tag.text)
        # print('Revenues: ' + tag.text)

for tag in tag_list:
    if tag.name == 'dei:tradingsymbol':
        print(tag)


for tag in tag_list:
    if tag.name == 'dei:documentperiodenddate':
        print(tag)



uniquetags = []

for n in tag_list:
    if n.name not in uniquetags:
        uniquetags.append(n.name)