import os
import sys
try:
    os.chdir(r'I:\git\RATool')
    sys.path.append(os.path.join("."))
    sys.path.append(os.path.join(os.getcwd()))  
except:
    sys.path.append(os.path.join("."))
    sys.path.append(os.path.join(os.getcwd()))  
import numpy as np
import matplotlib.pyplot as plt
from RNG import RNGenerator
from pricer import eq
from pricer import eqEO
from pricer import eqAT
from pricer import eqDD
from pricer import eqCT
from pricer import eqRS
from tradeslist import tradeslist
from tradeslist import EOption
from tradeslist import Autocall
from tradeslist import DDoption
from tradeslist import ContingentOption
from tradeslist import RSoption

from datetime import date
import math
import copy as copy
from PFE import PFEs
import matplotlib.pyplot as plt
import csv

def terminationDate (newTradeObj, today):
    ''' termination Date calculation
    This is used to return a longest termination Date among all the trades uploaded
    
    Args:
        param1: trade input, this should be a numpy array, can be 1D (single trade) or 2D (a basket of trades)
        param2: today's date

    Returns:
        The return value. termination Date, floored by today's date
    
    '''
    
    terminationdate = today
    try:
        if(type(newTradeObj[4]) is date):
            terminationdate = newTradeObj[4]
        else:
            for trade in newTradeObj:
                if(terminationdate < trade[4]):
                    terminationdate = trade[4]
    except:
        for trade in newTradeObj:
            if(terminationdate < trade[4]):
                terminationdate = trade[4]
    return terminationdate
                
def prepare_trade (tradem, terminationdate, today, newTrades):
    newTrade = tradeslist('l',0,1000,terminationdate,100,today)
    newEOTrade = EOption('l',0,"Call",100,10000,terminationdate,100,today)
    settlement = np.array([date(2018, 12, 5),date(2019, 12, 5),date(2020, 12, 5)])
    ko = np.array([100,100,100])
    ki = 0.7
    coupon = np.array([0.05,0.05,0.05])
    newATTrade = Autocall('l',0, settlement,0,100,ko,ki,10000,date(2020, 12, 5),coupon,100,today)
    cp = np.array([1,-1])
    newDDTrade = DDoption('l',0,cp,100,10000,terminationdate,100,today,date(2020, 12, 5))
    newCTTrade = ContingentOption('l',0,cp,100,10000,terminationdate,100,today,date(2020, 12, 5))
    observation = 0
    newRSTrade = RSoption('l',0,-1,100,100,observation,100,terminationdate,100,today,'Add')
    
    simpleList = []
    for count in range(0,tradem):
        # each iteration creates a slightly different attribute value, and then prints it to
    # prove that step is working
    # but the problem is, I'm always updating a reference to 'x' and what I want to add to
    # simplelist is a new instance of x that contains the updated attribute
        if str(newTrades[count][0]) == "EQ":
            simpleList.append(copy.copy(newTrade))
        elif str(newTrades[count][0]) == "EO":
            simpleList.append(copy.copy(newEOTrade))
            simpleList[count].setcp(str(newTrades[count][8]))
            simpleList[count].setstrike(float(newTrades[count][7]))
        elif str(newTrades[count][0]) == "AT":
            simpleList.append(copy.copy(newATTrade))
            simpleList[count].setcp((newTrades[count][8]))
            simpleList[count].setsettlement(newTrades[count][9])
            simpleList[count].setcouponbarrier(newTrades[count][10])
            simpleList[count].setknockout(newTrades[count][11])
            simpleList[count].setknockin(newTrades[count][12])
            simpleList[count].setcoupon(newTrades[count][13])
        elif str(newTrades[count][0]) == "DD":
            simpleList.append(copy.copy(newDDTrade))
            simpleList[count].setcp((newTrades[count][8]))
            simpleList[count].setstrike((newTrades[count][7]))
            simpleList[count].setsettlement(newTrades[count][9])
        elif str(newTrades[count][0]) == "CT":
            simpleList.append(copy.copy(newCTTrade))
            simpleList[count].setcp((newTrades[count][8]))
            simpleList[count].setstrike((newTrades[count][7]))
            simpleList[count].setsettlement(newTrades[count][9])
            simpleList[count].setContingentAssetId((newTrades[count][10]))
            simpleList[count].setContingentAssetStrike((newTrades[count][11]))
            simpleList[count].setContingentDirection(newTrades[count][12])
        elif str(newTrades[count][0] == "RS"):
            simpleList.append(copy.copy(newRSTrade))
            simpleList[count].setcp((newTrades[count][7]))
            simpleList[count].setstrike((newTrades[count][8]))
            simpleList[count].setobservation((newTrades[count][9]))
            simpleList[count].setthreshold((newTrades[count][10]))
            simpleList[count].setmethod((newTrades[count][11]))
            simpleList[count].setlimit((newTrades[count][12]))              
        #simpleList.append(newTrades)
        #newTrades.setassetid(newTrades.getassetid()+1)
        simpleList[count].setlongshort(str(newTrades[count][1]))
        simpleList[count].setnotional(float(newTrades[count][3]))
        simpleList[count].setassetid((newTrades[count][2]))
        simpleList[count].setterminationdate(newTrades[count][4])
        simpleList[count].setTradeprice(float(newTrades[count][5]))
        simpleList[count].setdealdate(newTrades[count][6])
        
    return simpleList
    
def dataPlot(PFE, portfolionode, steps, numOPath):
    t = np.arange(0., steps+1, 1)
    t0 = np.arange(0., steps, 1)
    print(np.average(portfolionode,axis=1).shape)
    print(t.shape)
    t20 = np.arange(0., steps-1, 1)
    try:
        plt.plot(t , np.average(portfolionode,axis=1))
        plt.show()
        print(portfolionode.shape)
        plt.plot(t, portfolionode)
        plt.show()
        plt.plot(t, PFE)
        plt.show()
        print('PFE value is ',PFE)
        t2 = np.arange(0., steps, 1)
        marginRpv = np.diff(portfolionode, axis=0)
        #print(marginRpv.shape)
        plt.plot(t2, marginRpv)
        plt.show()
        marginRpvPF = np.percentile(marginRpv, 0.977*100, axis=1) 
        #print(marginRpvPF.shape)  
        plt.plot(t2, marginRpvPF)
        plt.show()
        print(marginRpvPF)
        print(portfolionode.shape)
        plt.plot(np.arange(0., numOPath , 1), np.sort(portfolionode[steps,:]))
        plt.show()
    except:
        plt.plot(t0 , np.average(portfolionode,axis=1))
        plt.show()
        print(portfolionode.shape)
        plt.plot(t0, portfolionode)
        plt.show()
        plt.plot(t0, PFE)
        plt.show()
        print('PFE value is ',PFE)
        
        marginRpv = np.diff(portfolionode, axis=0)
        #print(marginRpv.shape)
        plt.plot(t20, marginRpv)
        plt.show()
        marginRpvPF = np.percentile(marginRpv, 0.977*100, axis=1) 
        #print(marginRpvPF.shape)  
        plt.plot(t20, marginRpvPF)
        plt.show()
        print('daily margin PFE value is ',marginRpvPF)
#    np.savetxt("output.csv", nppvlist, delimiter=",") 
        
def price(newTradeObj, vol , r, today = date.today(), step = 7, \
          numOPath = 1000, numberOfPricingPath = 10000, \
          rnseed = 1234567, rnPricingseed = 12121 , InterestRate = 0.01):
    ''' price funciton of the code
    This is an example entrance to the library
    
    Args:
        param1: trade input, this should be a numpy array, can be 1D (single trade) or 2D (a basket of trades)
        param2: market factor volatility, this should be a 1D np array
        param3: market factor correlation matrix, this should be a 2D np array
        param4: Simulation steps, this should match with margin periode
        param5: simulation path number
        param6: MC pricing path number
        param7: simulation random seed
        param8: MC pricing random seed
        param9: interestRate

    Returns:
        The return value. portfolio PV matrix.
    
    '''
    
    terminationdate = terminationDate(newTradeObj,today)
    d = terminationdate-today
    steps = int(math.ceil((float(d.days))/float(step)))
    
    # Then create an empty list
    #Range('Test', 'A1').value = newTradeObj
    if newTradeObj.ndim == 2:
        [tradem,traden] = newTradeObj.shape
    
        newTrades = newTradeObj[:]
        print('trade demintion = ', [tradem,traden])
    if newTradeObj.ndim == 1:
        # no trades there
        tradem = 1
        traden = newTradeObj.shape[0]
        newTrades = []
        newTrades.append(newTradeObj)
                
    simpleList = []    
    simpleList = prepare_trade (tradem, terminationdate, today, newTrades)
    
    [rm,rn] = r.shape
    if (rm != rn):
        print('Covariance matrix is not square!')
        
    
    # here we prepare randam number
    marketdata = RNGenerator(r, rnseed ,numOPath , steps)   #################################################Here we define the path
    pricingdata = RNGenerator(r, rnPricingseed ,numberOfPricingPath , steps)   #################################################Here we define the path                    
   
    pvlist = []
#    here we price all the trade
    for count in range(0,tradem):
        for i in range(0,traden):
            print(newTrades[count][i])
        if str(newTrades[count][0]) == "EQ":
            pvlist.append(eq(simpleList[count],marketdata,pricingdata,today, step,steps,vol))
        elif str(newTrades[count][0]) == "EO":
            pvlist.append(eqEO(simpleList[count],marketdata,pricingdata,today,step,steps,vol,InterestRate))
        elif str(newTrades[count][0]) == "AT":
            pvlist.append(eqAT(simpleList[count],marketdata,pricingdata,today,step,steps,vol,InterestRate))
        elif str(newTrades[count][0]) == "DD":
            pvlist.append(eqDD(simpleList[count],marketdata,pricingdata,today,step,steps,vol,InterestRate))
        elif str(newTrades[count][0]) == "CT":
            pvlist.append(eqCT(simpleList[count],marketdata,pricingdata,today,step,steps,vol,InterestRate))
        elif str(newTrades[count][0]) == "RS":
          
            pvlist.append(eqRS(simpleList[count],pricingdata,today, step,steps,vol,marketdata))

    #print(pvlist[0][0][0],3)
    #Range('Test', 'A1').value = pvlist
    nppvlist = np.asarray(pvlist)
    print(nppvlist.shape)
#    print(nppvlist)
    # here we do net up
    (PFE, portfolionode) = PFEs(nppvlist,simpleList,tradem,0.977)
    print('largest PFE is '+str(max(PFE)))
    #everything after here is for data show
    dataPlot(PFE, portfolionode, steps, numOPath)
    return portfolionode
