# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 21:15:33 2021

@author: jfalk

Pulling data from Alpha Vantage API

"""

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import seaborn as sns
import os
from datetime import datetime
import requests
import json
from time import sleep

os.chdir('')
key = ''

fininfoannualfin = pd.DataFrame()
fininfoquarterlyfin = pd.DataFrame()

#Found list of stock symbols. Loading it to see what I've got
#Dropna for all the investment groups and collections of stocks that I don't care about
stocksymbols = pd.read_csv('nasdaq_screener_1615001058936.csv').dropna(subset=['Industry'])

symbollist = stocksymbols['Symbol'].tolist()

tickerlist = []


for symbol in symbollist[:450]:
    tickerlist.append(symbol)


for tick in tickerlist:
    print(tick)
    

    ticker = tick
    finurl = 'https://www.alphavantage.co/query?function=EARNINGS&symbol={}&apikey={}'.format(ticker, key)
    
    finresponse = requests.get(finurl)
    #Alpha Vantage only allows 5 API calls per minute so slowing this down a bit
    sleep(15.0)
    #If stock has no data the total length of this field is 80 something. Dodging those since otherwise they cause errors
    if len(finresponse.text)>100:
        #Section for annual stock data
        fininfoannual = pd.json_normalize(finresponse.json(), 'annualEarnings')
        if not fininfoannual.empty:
            #Adding field for the stock symbol
            fininfoannual['Symbol'] = ticker
            #Sorting by date
            fininfoannual = fininfoannual.sort_values('fiscalDateEnding')
            #Converting the reported EPS to a numeric field
            fininfoannual['reportedEPS'] = pd.to_numeric(fininfoannual.reportedEPS, errors='coerce')
            #Appending new data to the overall tracking dataframe
            fininfoannualfin = fininfoannualfin.append(fininfoannual)
    
        fininfoquarterly = pd.json_normalize(finresponse.json(), 'quarterlyEarnings')
        if not fininfoquarterly.empty:
            fininfoquarterly['Symbol'] = ticker
            fininfoquarterly = fininfoquarterly[['Symbol', 'fiscalDateEnding', 'reportedEPS']]
            fininfoquarterly['fiscalDateEnding'] = pd.to_datetime(fininfoquarterly.fiscalDateEnding)
            fininfoquarterly = fininfoquarterly.sort_values('fiscalDateEnding')
            fininfoquarterly['reportedEPS'] = pd.to_numeric(fininfoquarterly.reportedEPS, errors='coerce')
            fininfoquarterlyfin = fininfoquarterlyfin.append(fininfoquarterly)


# =============================================================================
# Annual Financial Data
# =============================================================================

#Extracting year from datetime
fininfoannualfin['year'] = pd.DatetimeIndex(fininfoannualfin['fiscalDateEnding']).year

#Only want years between 2017 and 2020
fininfoannualcurrent = fininfoannualfin.loc[(fininfoannualfin['year'] >=2017) & (fininfoannualfin['year'] <2021)].copy()
#Sorting to get things in right order for percent change calculation
fininfoannualcurrent.sort_values(['Symbol','year'], inplace = True, ascending=[True, True])

#Percent change of reported earnings per stock between years by stock
fininfoannualcurrent['pct_ch'] = (fininfoannualcurrent.groupby('Symbol')['reportedEPS']
                                  .apply(pd.Series.pct_change)*100)

#Resorting into a more intelligent manner
fininfoannualcurrent.sort_values(['Symbol','year'], inplace = True, ascending=[True, False])

fininfoannualcurrent.to_csv('annualfininfo.csv', index=False)

# =============================================================================
# Quarterly Financial Data
# =============================================================================

fininfoquarterlycurrent = fininfoquarterlyfin.copy()
fininfoquarterlycurrent['year'] = pd.DatetimeIndex(fininfoquarterlycurrent['fiscalDateEnding']).year
fininfoquarterlycurrent['month'] = pd.DatetimeIndex(fininfoquarterlycurrent['fiscalDateEnding']).month

fininfoquarterlycurrent = fininfoquarterlycurrent.loc[(fininfoquarterlycurrent['year'] >=2017) & \
                                                      (fininfoquarterlycurrent['year'] <=2021)]

fininfoquarterlycurrent.sort_values(['Symbol','month'], inplace = True, ascending=[True, True])

fininfoquarterlycurrent['pct_ch'] = (fininfoquarterlycurrent.groupby(['Symbol', 'month'])['reportedEPS']
                                  .apply(pd.Series.pct_change)*100)

fininfoquarterlycurrent.sort_values(['Symbol','month', 'year'], inplace = True, ascending=[True, True, False])

fininfoquarterlycurrent.to_csv('quarterlyfininfo.csv', index=False)






#Attempting Alpha Vantage API call for good old CTRM. YARGH!!!!!

    # fininfoannual['percentchange'] = (fininfoannual['reportedEPS'].diff() / \
    #                                      fininfoannual['reportedEPS'].abs().shift())*100
    # fininfoannual = fininfoannual[['Symbol', 'fiscalDateEnding', 'reportedEPS', 'percentchange']]
    # fininfoquarterly['percentchange'] = (fininfoquarterly['reportedEPS'].diff() / fininfoquarterly['reportedEPS'].abs().shift())*100


ticker = 'CTRM'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)


response = requests.get(url)
print(response.json()) 

jsonload = json.load(response.json())

testdf = pd.json_normalize(response.json()['Time Series (Daily)'])
