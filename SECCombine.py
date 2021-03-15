# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 18:02:45 2021

@author: jfalk

Looking over some files downloaded from the SEC repository

Num contains actual values of interest
join Num to sub on adsh to link name to numeric info

pre and tag files look pretty useless...

"""

import pandas as pd
import os

SECDIR = "C:/Users/jfalk/Documents/SECDATA"

os.chdir(SECDIR)

os.listdir(SECDIR)

numlist = []

for root, dirs, files in os.walk(SECDIR):
    if not files:
        continue
    prefix = os.path.basename(root)
    for f in files:
        if f in ('num.txt'): 
            filename = SECDIR + '/'+ prefix + '/'+ f
            print(filename)
            
            try:
                numdf = pd.read_csv(filename, delimiter='\t')
                numlist.append(numdf)
            except:
                continue
            
            
numfull = pd.concat(numlist, axis=0, ignore_index=True)

numfull = numfull.drop(columns=['coreg', 'uom', 'footnote'])
numfullhead = numfull.head(40)

numfull = numfull.drop_duplicates()

numfull.to_csv('fullnum.csv', index=False)


#Contains name of company
sub = pd.read_csv('sub.txt', delimiter='\t')

#Extracting name and adsh joining code
subnames = sub[['name', 'adsh']].copy()

#Contains financial info
num = pd.read_csv('num.txt', delimiter='\t')

numhead = num.head(50)

#Merging names to financial info
namednum = subnames.merge(num, left_on='adsh', right_on='adsh')

namednumhead = namednum.head(50)

#Keeping columns of interest
namednuminterest = namednum[['name', 'tag', 'version', 'ddate', 'qtrs', 'value']].copy()

#Dumping unnecessary clutter
del sub, subnames, num, numhead, namednum, namednumhead


namednumtags = pd.DataFrame(namednuminterest.tag.value_counts())

namednumtags = namednumtags.loc[namednumtags['tag'] > 5000]

Earningspershare = namednuminterest.loc[namednuminterest['tag'] == 'EarningsPerShareBasic']
