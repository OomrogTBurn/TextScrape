# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:40:49 2021

@author: jfalk


Pulling stock data using pandas-datareader
Analyzing it...somehow
FUCKING TENDIES BABYYYYYYYYYYYYYY

Want to estimate the low for the day to guess best time to buy


"""

import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt

import pandas_datareader.data as web


startdate = datetime.datetime(2010,12,1)

enddate = datetime.datetime(2021,1,1)

pull = web.DataReader("TXMD", "yahoo", startdate, enddate)

pull.Close.plot()

pull.corr()


cs = pull.Close
ema = cs.ewm(span=20).mean()
ema = ema[::-1].ewm(span=20).mean()[::-1]
plt.plot(pull.Close.values,color='b')
plt.plot(ema.values,color='r')
plt.show()