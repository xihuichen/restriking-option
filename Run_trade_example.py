# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 15:20:08 2018

@author: lt54159
"""
import os
import sys
 # Here is your local git folder Path
os.chdir(r'I:\git\RATool')  

sys.path.append(os.path.join("."))
sys.path.append(os.path.join(os.getcwd()))  
from RaTool import price
from datetime import date
import numpy as np

# Dual Ditigal example

# Here is the valuation date
today = date.today() 
# Here is to define which asset underlying the contract
asset = np.array([0,1])  
# Here is to define strike price of the contract strike/spot in %  
strike = np.array([98.8,100.8])  
# Here is to define the direction, -1 mean less than or put  
cp = np.array([-1,-1])  
# Here is to define the final observation date  
settlement = np.array([date(2019, 10, 10)])    

newTrade2 = np.array([
        'DD',    # trade type, DD means dual digital
        'l',     # Citi position, l(long) or s(short)
        asset,    # asset id, see comments above
        10000,    # notional (total payoff) of the trade
        date(2019, 10, 10),    # trade ternimation date
        100,     # simulation start price. keep this number as 100
        today,    # simulation date
        strike,    # strike price, see comments above
        cp,    # call/put, see comments above
        settlement    # settlement date, see comments above
        ])


# below shows the vol and correlation, here we have three assets defined. Although only two used for pricing
vol = np.array([0.078, 0.078, 0.07925865])
r = np.array([
        [1, -0.82, -0.173249412],
        [-0.82, 1, -0.038537897],
        [-0.173249412, -0.038537897, 1],
        ])
price(
      newTrade2,
      vol,
      r
      )


# This is for   contigient option         
today = date.today()
asset = np.array([0])
strike = np.array([96.4])
cp = np.array([-1])
settlement = np.array([date(2019, 9, 21)])
ContingentAssetId = np.array([1])
ContingentAssetStrike = np.array([104.5])
ContingentDirection = np.array([1])
newTradeCT = np.array(['CT','s',asset,10000,date(2019, 9, 21),100,today,strike,cp,settlement,ContingentAssetId,ContingentAssetStrike,ContingentDirection])
vol = np.array([0.124,0.039, 0.0877])
r = np.array([[1, -0.075, 0.23],
              [-0.075, 1, 0.20],
              [0.23, 0.20, 1],])
price(newTradeCT,vol,r)

# This is for a portfolio of trade    
today = date.today()
vol = np.array([0.2099,0.1689, 0.1837])
r = np.array([[1, 0.88613, 0.97718],
              [0.88613, 1, 0.96428],
              [0.97718, 0.96428, 1],])
newTrade0 = np.array([['EO','l',0,500000,date(2020, 12, 18),100,today,100.00,'Call'],
                          ['EO','l',1,500000,date(2020, 12, 18),100,today,100.00,'Call'],
                          ['EO','s',2,1000000,date(2020, 12, 18),100,today,100.00,'Call'],])
price(newTrade0,vol,r)

# This is for a portfolio of trade    
today = date.today()
vol = np.array([0.2099,0.1689, 0.1837])
r = np.array([[1, 0.999999, 0.999999],
              [0.999999, 1, 0.999999],
              [0.999999, 0.999999, 1],])
newTrade0 = np.array([['EO','l',0,500000,date(2020, 12, 18),100,today,100.00,'Call'],
                          ['EO','l',1,500000,date(2020, 12, 18),100,today,100.00,'Call'],
                          ['EO','s',2,1000000,date(2020, 12, 18),100,today,100.00,'Call'],])
price(newTrade0,vol,r)

# This is for a Single option
today = date.today()
newTrade0 = np.array(['EO','l',0,10000,date(2020, 12, 5),100,today,100.00,'Call'])
price(newTrade0,vol,r)

# This is for autocall
today = date.today()

# Auto call 
today = date.today()
vol = np.array([0.23,0.24,0.298])
r = np.array([[1, 0.104, 0.325],
              [0.104, 1, 0.389],
              [0.325, 0.389, 1],])
settlement = np.array([date(2019, 9, 6),date(2020, 9, 6),date(2021, 9, 6),date(2022, 9, 6),date(2023, 9, 6),date(2024, 9, 6)])
ko = np.array([100,100,100,100,100,100])
ki = 0.6
coupon = np.array([0.05,0.05,0.05,0.05,0.05,0.05])
barrier = np.array([0.6,0.6,0.6,0.6,0.6,0.6])
asset = np.array([0,1,2])
cp = np.array([-1,-1,-1])
newTrade3 = np.array(['AT','l',asset,10000,date(2024, 9, 6),100,today,100.00,cp,settlement,barrier,ko,ki,coupon])
price(newTrade3,vol,r)

# Auto call 
today = date.today()
vol = np.array([0.23,0.23,0.23])
r = np.array([[1, 0.999999, 0.999999],
              [0.999999, 1, 0.999999],
              [0.999999, 0.999999, 1],])
settlement = np.array([date(2019, 9, 6),date(2020, 9, 6),date(2021, 9, 6)])
ko = np.array([100,100,100])
ki = 0.00001
coupon = np.array([0.05,0.05,0.05])
barrier = np.array([100,100,100])
asset = np.array([0,1,2])
cp = np.array([-1,-1,-1])
newTrade3 = np.array(['AT','l',asset,10000,date(2021, 9, 6),100,today,100.00,cp,settlement,barrier,ko,ki,coupon])
price(newTrade3,vol,r)

# Auto call 
today = date.today()
settlement = np.array([date(2018, 11, 6),date(2018, 12, 6),date(2019, 1, 6),date(2019, 2, 6),date(2019, 3, 6),date(2019, 4, 6),date(2019, 5, 6),date(2019, 6, 6),date(2019, 7, 6),date(2019, 8, 6),date(2019, 9, 6),date(2019, 10, 6),date(2019, 11, 6)])
ko = np.array([100,100,100,100,100,100,100,100,100,100,100,100,100])
ki = 0.70
coupon = np.array([0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01])
barrier = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
asset = np.array([0,1,2])
cp = np.array([-1,-1,-1])
newTrade3 = np.array(['AT','l',asset,10000,date(2019, 11, 6),100,today,100.00,cp,settlement,barrier,ko,ki,coupon])
vol = np.array([0.23,0.24,0.298])
r = np.array([[1, 0.104, 0.325],
              [0.104, 1, 0.389],
              [0.325, 0.389, 1],])
price(newTrade3,vol,r)

# Auto call 
today = date.today()
vol = np.array([0.23,0.23,0.23])
r = np.array([[1, 0.999999, 0.999999],
              [0.999999, 1, 0.999999],
              [0.999999, 0.999999, 1],])
settlement = np.array([date(2018, 10, 10),date(2018, 10, 17)])
ko = np.array([100,100])
ki = 100
coupon = np.array([0.05,0.05])
barrier = np.array([100,100])
asset = np.array([0,1,2])
cp = np.array([-1,-1,-1])
newTrade3 = np.array(['AT','l',asset,10000,date(2018, 10, 17),100,today,100.00,cp,settlement,barrier,ko,ki,coupon])
price(newTrade3,vol,r)

today = date.today()
'Restriking Option'
p0=100
cp=-1 # 1 means call and -1 represents put
method='PegMax' #if the restriking method is initial strike plus reset gap, then here should be 'Add',otherwise 'Multiply'
start_date=date(2018,10,23)
settlement=date(2019,10,23)
initial_strike1=90
initial_strike2=70
observation=30 #in days
threshold=5 #this corresponding to threshold, in %. for example, 5% threshold, here entry is 5
vol=0.2
cap=150 #'Reset gap is 5% between 105% and 150%, then the cap should be entered 150 here, means stock price over 150 wouldnt trigger any further restrike up'
floor=70 #if the cap&floor here is given as maximum strike time, then we manually calculate the cap/floor in percentage and apply here
r=np.array([[1]]) #covariance matrix, only one underlying then r=np.array([[1]])
newTrade2 = np.asarray([['RS','l',0,100,settlement,p0,start_date,cp,initial_strike2,observation,threshold,method,105],
                        ['RS','s',1,100,settlement,p0,start_date,cp,initial_strike1,observation,threshold,method,cap]])
newTrade1=np.asarray(['RS','l',0,100,settlement,p0,start_date,cp,initial_strike1,observation,threshold,method,cap])
#(self, ls, id, callput,inputterminationdate, strike,nnotional,threshold,observation,p0=100,inputdealdate=date.today(),method)
pv=price(newTrade1,vol,r,start_date, step = 7, \
          numOPath = 1000, numberOfPricingPath = 1000, \
          rnseed = 1234567, rnPricingseed = 12121 , InterestRate = 0.01)


# This is for a Single option, comparison
vol = np.array([0.20,0.1689, 0.1837])
r = np.array([[1, 0.999999, 0.999999],
              [0.999999, 1, 0.999999],
              [0.999999, 0.999999, 1],])

newTrade0 = np.array(['EO','l',0,1,date(2020, 12, 5),100,date(2018,10,23),90,'Put'])
price(newTrade0,vol,r)