import numpy as np
import matplotlib.pyplot as plt
from RNG import RNGenerator
import copy as copy
from scipy.stats import norm
import matplotlib.pyplot as plt
from datetime import timedelta
import math

def eq(trade, marketdata, pricingdata, today, step, steps,vol):
    #print(trade.getls()+'/n')
    ls = 0
    #print(trade.getls())
    if('l' == trade.getls()):
        ls = 1.0
    if('s' == trade.getls()):
        ls = -1.0
    [m, n] = marketdata[0].shape
    print('m = ' + str(m) + ', n = ' + str(n))
    pvstock = []
    pvstock = simulateStock(trade,marketdata,today,step,steps,vol,trade.getassetid())
#   
    return pvstock

def eqEO(trade, marketdata,pricingdata, today, step, steps,vol,BS_r):
    #print(trade.getls()+'/n')
    ls = 0
    #print(trade.getls())
    if('l' == trade.getls()):
        ls = 1.0
    if('s' == trade.getls()):
        ls = -1.0
    [m, n] = marketdata[0].shape
    print('m = ' + str(m) + ', n = ' + str(n))
    pvtrades = []
    newpricenode = []
    if('Call' == trade.getcp()):
        BS_cp = 1.0
    if('Put' == trade.getcp()):
        BS_cp = -1.0
    eq_vol = vol[trade.getassetid()]
    BS_vol = eq_vol
    for j in range(0,steps):
        BS_T = ((trade.getterminationdate() - today).days - j * step) /365.25
        pvtradesnode = []
        newpricepass = []
        
        for i in range(0,n):            
            todayprice = marketdata[j][trade.getassetid()][i]            
            if(j == 0):                
                newprice = trade.getp0()*np.exp(-0.5*(eq_vol**2)*5.0/260.0+float(todayprice)*eq_vol*((5.0/260.0)**.5))
                price_change = newprice# - trade.getp0()
            else:
                newprice = newpricenode[j-1][i]*np.exp(-0.5*(eq_vol**2)*5.0/260.0+float(marketdata[j][trade.getassetid()][i])*eq_vol*((5.0/260.0)**.5))
                price_change = newprice          
            
            if (BS_T > 0):
                BS_d1 = (np.log(newprice/trade.getstrike()) + (BS_r + BS_vol **2 ) * BS_T)/(BS_vol * (BS_T)**0.5)
                BS_d2 = BS_d1 - BS_vol * (BS_T)**0.5
                price_change = BS_cp * (newprice * norm.cdf(BS_cp * BS_d1) - trade.getstrike() *  np.exp(-BS_r*BS_T) * norm.cdf(BS_cp * BS_d2))
            elif (BS_T == 0):
                BS_d1 = (np.log(newprice/trade.getstrike()) + (BS_r + BS_vol **2 ) * BS_T)/(BS_vol * (BS_T)**0.5)
                BS_d2 = BS_d1 - BS_vol * (BS_T)**0.5
                price_change = BS_cp * (newprice * norm.cdf(BS_cp * BS_d1) - trade.getstrike() *  np.exp(-BS_r*BS_T) * norm.cdf(BS_cp * BS_d2))
            else:
                price_change = 0
            newpricepass.append( copy.copy(newprice))            
            pvtradesnode.append( copy.copy(float(trade.getnotional()) * ls * price_change))        
        newpricenode.append(copy.copy(newpricepass))
        pvtrades.append(copy.copy(pvtradesnode))

    return pvtrades


def discount(inputmatirx,discto):
    
    return (inputmatirx[:,0].mean()+inputmatirx[:,2].mean())

def priceAT(trade, newpricenodeAMC, newpricenode, today,step, steps):
    newpricenodeAMC =newpricenode
    settlementsteps = []
    for getsettlementarray in range(0,len(trade.getsettlement())):
        settlementsteps.append(int(math.ceil((float(((trade.getsettlement()[getsettlementarray]-today)).days))/float(step))))
    price0 = []
    noset = len(trade.getsettlement())
    price0npath = []
    for pathloop in range(0, len(newpricenode[0,0,:])):
        price0node = []
        terminatePath = steps+1
        payment = []
        lenofsteps = len(settlementsteps)
        for settlementstep in reversed(settlementsteps):
            lenofsteps = lenofsteps -1
            if(newpricenode[:,settlementstep,pathloop].min()*100 > trade.getknockout()[lenofsteps]):
                terminatePath = settlementstep     
                payment = [trade.getcoupon()[0:lenofsteps+1].sum(),lenofsteps]        
        price0node0 = []
        for j in range(0,steps+1):
            priceDate = today+timedelta(days=step*j)
            todayPrice = newpricenode[:,j,:]
            k = priceDate
            todayPricePath = todayPrice[trade.getassetid().tolist(),pathloop]
            if(j < terminatePath):
                temp = np.zeros((len(newpricenode[0,j,:]), 3))
                #temp[:,] = (trade.getcoupon().sum(), noset,0)
                temp[:,] = (0, noset,0)
                for i in range(0,noset):
                    if(k<trade.getsettlement()[i]):
                        furturedays = int(math.ceil((float((trade.getsettlement()[i]-k).days))/float(step)))                        
                        temp[((todayPricePath*newpricenodeAMC[trade.getassetid().tolist(),furturedays,:].T*100).T.min(0) > trade.getknockout()[i])\
                             * (temp[:,1] == noset ) \
                             *((todayPricePath*newpricenodeAMC[trade.getassetid().tolist(),furturedays,:].T*100).T.min(0) > trade.getcouponbarrier()[i])] \
                             = (trade.getcoupon()[:i+1].sum(),i,0)
                    
                
                furturedays = int(math.ceil((float((trade.getterminationdate()-k).days))/float(step)))            
                if(type(trade.getcp()) == str):
                    temp[:,2] = ((todayPricePath*newpricenodeAMC[trade.getassetid().tolist(),furturedays,:].T*100 - trade.getstrike()).T.min(0)/100) \
                                *((todayPricePath*newpricenodeAMC[trade.getassetid().tolist(),furturedays,:].T).T.min(0)<trade.getknockin()) \
                                 *(temp[:,1] == noset)
                if(type(trade.getcp()).__module__ == np.__name__):                    
                    temp[:,2] = -((trade.getcp()*(todayPricePath*newpricenodeAMC[trade.getassetid().tolist(),furturedays,:].T*100 - trade.getstrike())).T.max(0)/100) \
                                *((trade.getcp()*(todayPricePath*newpricenodeAMC[trade.getassetid().tolist(),furturedays,:].T - trade.getknockin())).T.max(0) > 0) \
                                 *(temp[:,1] == noset)
                price0node0 = discount(temp, priceDate)
                
                price0node.append(price0node0)
                
            else:
                price0node.append(payment[0])
                
        
        price0node = np.asarray(price0node)
        
        price0npath.append(price0node)
    
    price0 = np.asarray(price0npath)   
   
    return np.array(np.swapaxes(price0,0,1))

def priceAT1(trade, newpricenodeAMC, newpricenode, today, priceDate,step):
    j = int(math.ceil((float((priceDate-today).days))/float(step)))
    return newpricenode[j,:]

def simulateStock(trade,marketdata,today,step,steps,vol,assetid):
    eq_vol = vol[assetid]
    [m, n] = marketdata[0].shape
    ONEs = np.ones(n)
    newpricenode = ONEs    
    for j in range(0,steps):
           
        
        if(j == 0):
            newprice = ONEs * np.exp(-0.5*(eq_vol**2)*step/365.25 + np.array(marketdata[j][assetid])*eq_vol*((step/365.25)**.5))
            
            newpricenode = np.vstack((newpricenode, newprice))
            
        else:
            
            if(newpricenode.ndim == 1):
                newprice = newpricenode*np.exp(-0.5*(eq_vol**2)*step/365.25+np.array(marketdata[j][assetid])*eq_vol*((step/365.25)**.5))
            else:
                newprice = newpricenode[j,:]*np.exp(-0.5*(eq_vol**2)*step/365.25+np.array(marketdata[j][assetid])*eq_vol*((step/365.25)**.5))
            newpricenode =np.vstack((newpricenode, newprice))
    return newpricenode

def simulateMultiStocks(trade,marketdata,today,step,steps,vol):
    try:
        assetlen = len(trade.getassetid())
        
    except:
        assetlen = 0
        assetid = trade.getassetid()
        
    if(assetlen == 0):
        return simulateStock(trade,marketdata,today,step,steps,vol,assetid)
    else:
        for i in range(0,assetlen):
            if(i == 0):
                Spv = simulateStock(trade,marketdata,today,step,steps,vol,trade.getassetid()[i])
            else:
                Spv = np.minimum(Spv, simulateStock(trade,marketdata,today,step,steps,vol,trade.getassetid()[i]))
        return Spv
        
        
        
def eqAT(trade, marketdata, pricingdata, today, step, steps,vol,BS_r):
    #print(trade.getls()+'/n')
    ls = 0
    #print(trade.getls())
    if('l' == trade.getls()):
        ls = 1.0
    if('s' == trade.getls()):
        ls = -1.0
    if(len(trade.getsettlement())>1):
        Autofag = 1
    elif(len(trade.getsettlement())==1):
        Autofag = 0
    marketdata = np.asarray(marketdata)
    pricingdata = np.asarray(pricingdata)
    [m, n] = marketdata[0].shape
    print('m = ' + str(m) + ', n = ' + str(n))
    #pvtrades = []
    newpricenode = []
    newpricenode = simulateAllStocks(trade,marketdata,today,step,steps,vol)   
    newpricenodeAMC =simulateAllStocks(trade,pricingdata,today,step,steps,vol)
    
    pvtradesnode = []
    pvtradesnode = priceAT(trade, newpricenodeAMC, newpricenode,today, step, steps)
    
    marginpvtrades = -pvtradesnode
    
    return marginpvtrades

def simulateAllStocks(trade,marketdata, today,step,steps,vol):
    
    [m,assetlen,n] = marketdata.shape
    #print("assetlen is ", assetlen, m, n)
    if(assetlen == 0):
        return simulateStock(trade,marketdata,today,step,steps,vol,assetlen)
    else:
        for i in range(0,assetlen):
            if(i == 0):
                
                Spv = simulateStock(trade,marketdata,today,step,steps,vol,i)
                [m,n] = Spv.shape
                Spv = Spv.reshape(1,m,n)
            else:
                               
                Spv = np.vstack((Spv,simulateStock(trade,marketdata,today,step,steps,vol,i).reshape(1,m,n)))
                
        return Spv

def priceDD(trade, newpricenodeAMC, newpricenode, today,step, steps):
    settlementsteps = []
    for getsettlementarray in range(0,len(trade.getsettlement())):
        settlementsteps.append(int(math.ceil((float(((trade.getsettlement()[getsettlementarray]-today)).days))/float(step))))

    price0 = []
    nostrike = len(trade.getstrike())
    price0npath = []
    for pathloop in range(0, len(newpricenode[0,0,:])):
        price0node = []
        price0node0 = []
        for j in range(0,steps+1):
            priceDate = today+timedelta(days=step*j)
            todayPrice = newpricenode[:,j,:]
            todayPricePath = todayPrice
            k = priceDate
            todayPricePath = todayPrice[:,pathloop]
            
            temp = np.zeros((len(newpricenodeAMC[0,j,:]), 3))
            temp[:,] = (trade.getnotional(), nostrike,0)
            furturedays = int(math.ceil((float((trade.getsettlement()[0]-k).days))/float(step)))
            for noasset,noid in zip(trade.getassetid(),range(0, len(trade.getstrike()))):
                if(trade.getcp()[noid] == 1) :
                    temp[(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:]*100 < trade.getstrike()[noid]) \
                    * (temp[:,1] == nostrike)] \
                    = (0,noid,0) 
                else:
                    temp[(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:]*100 > trade.getstrike()[noid]) \
                    * (temp[:,1] == nostrike)] \
                    = (0,noid,0)
                    
            price0node0 = discount(temp, priceDate)
            price0node.append(price0node0)
            
        price0node = np.asarray(price0node)        
        price0npath.append(price0node)
        
    price0 = np.asarray(price0npath)
    
    return np.array(np.swapaxes(price0,0,1))
  
def eqDD(trade, marketdata, pricingdata,today, step, steps,vol,BS_r):
    #print(trade.getls()+'/n')
    ls = 0
    #print(trade.getls())
    if('l' == trade.getls()):
        ls = 1.0
    if('s' == trade.getls()):
        ls = -1.0
    try:
        if(len(trade.getsettlement())>1):
            Autofag = 1
    except:
        Autofag = 0
    marketdata = np.asarray(marketdata)
    pricingdata = np.asarray(pricingdata)
    [noasset, m, n] = marketdata.shape
    newpricenode = []
    newpricenode = simulateAllStocks(trade,marketdata,today,step,steps,vol)
    newpricenodeAMC =simulateAllStocks(trade,pricingdata,today,step,steps,vol)
    pvtradesnode = priceDD(trade, newpricenodeAMC, newpricenode, today,step, steps)
    marginpvtrades = pvtradesnode*ls
    return marginpvtrades

def priceCT(trade, newpricenodeAMC, newpricenode, today,step, steps):
    newpricenodeAMC =newpricenode
    settlementsteps = []
    for getsettlementarray in range(0,len(trade.getsettlement())):     
        settlementsteps.append(int(math.ceil((float(((trade.getsettlement()[getsettlementarray]-today)).days))/float(step))))
    price0 = []    
    nostrike = len(trade.getContingentAssetStrike())
    price0npath = []
    for pathloop in range(0, len(newpricenode[0,0,:])):
        price0node = []
        price0node0 = []
        for j in range(0,steps+1):
            priceDate = today+timedelta(days=step*j)
            todayPrice = newpricenode[:,j,:]
            todayPricePath = todayPrice
            k = priceDate
            todayPricePath = todayPrice[:,pathloop]
            
            temp = np.zeros((len(newpricenode[0,j,:]), 3))
            temp[:,] = (0, nostrike,0)
            #print('temp',temp.shape)            
            furturedays = int(math.ceil((float((trade.getsettlement()[0]-k).days))/float(step)))
            noasset = trade.getassetid()[0]
            if(trade.getcp()[0] == 1) :
                temp[:,2] = ((todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:].T*100 - trade.getstrike()[0]).T/100) \
                    *(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:].T*100 > trade.getstrike()[0])                 
            else:
                temp[:,2] = ((-todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:].T*100 + trade.getstrike()[0]).T/100) \
                    *(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:].T*100 < trade.getstrike()[0])           
            for noasset,noid in zip(trade.getContingentAssetId(),range(0, len(trade.getstrike()))):
                if(trade.getContingentDirection()[noid] == 1) :
                    temp[(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:]*100 < trade.getContingentAssetStrike()[noid]) \
                    * (temp[:,1] == nostrike)] \
                    = (0,noasset,0)
                    
                else:
                    temp[(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:]*100 > trade.getContingentAssetStrike()[noid]) \
                    * (temp[:,1] == nostrike)] \
                    = (0,noasset,0)    
            
            price0node0 = discount(temp, priceDate)
            price0node.append(price0node0)
        price0node = np.asarray(price0node)
        price0npath.append(price0node)
    price0 = np.asarray(price0npath)
    return np.array(np.swapaxes(price0,0,1))

def eqCT(trade, marketdata, pricingdata, today, step, steps,vol,BS_r):
    #print(trade.getls()+'/n')
    ls = 0
    #print(trade.getls())
    if('l' == trade.getls()):
        ls = 1.0
    if('s' == trade.getls()):
        ls = -1.0
    try:
        if(len(trade.getsettlement())>1):
            Autofag = 1
    except:
        Autofag = 0
    marketdata = np.asarray(marketdata)
    pricingdata = np.asarray(pricingdata)
    [noasset, m, n] = marketdata.shape
    newpricenode = []
    newpricenode = simulateAllStocks(trade,marketdata,today,step,steps,vol)
    newpricenodeAMC =simulateAllStocks(trade,pricingdata,today,step,steps,vol)
    
    pvtradesnode = priceCT(trade, newpricenodeAMC, newpricenode, today,step, steps)
    marginpvtrades = pvtradesnode*ls
    
    return marginpvtrades



def SimRSOptionPrice(trade,randomvariables,spotpricePath,step,steps,vol):
    '''I want to define a new function that can simulate from spot price("today"'s price)
    step: what step we are on today
    steps: how many steps are there until maturity
    '''
    p0=trade.getp0()
    observation=trade.getobs()
    obs=math.floor(observation/step) 
    '''note here we get the observation is how many times of step length'''
    initial_strike=trade.getstrike()
    initialPrice=trade.getp0()
    threshold=trade.getthreshold()
 #   [m,n]=spotpricePaths.shape
#    print('spot',[m,n])
    spotpricePaths=[]
    for i in range(0,len(randomvariables[0][0])):
        spotpricePaths.append(spotpricePath)
        
        
      
    spotpricePaths=np.asarray(spotpricePaths)
    
    [m,n]=spotpricePaths.shape
#    print([m,n])
    spotpricePaths=spotpricePaths.transpose()
#    print(spotpricePaths.shape)
 #   spotpricePaths=spotpricePaths.reshape(len(randomvariables[0]),len(spotpricePath))
    spotprice = spotpricePaths[n-1]
#    print(spotpricePaths.shape)
    newpricemtx=[]
    payoff=[[]]
    for i in range(0,steps):
      #  PriceDate= today+timedelta(days=step*i)
        if i==0:
            newprice = spotprice * np.exp(-0.5*(vol**2)*step/365.25 + np.array(randomvariables[i])*vol*((step/365.25)**.5))
            newpricemtx = np.vstack((spotprice,newprice))
            
        else:
            #print(newpricenode[j-1])
            #print(np.array(marketdata[j][trade.getassetid()]))
            newprice = newpricemtx[i,:]*np.exp(-0.5*(vol**2)*step/365.25+np.array(randomvariables[i])*vol*((step/365.25)**.5))
                #print('newpricenode[j-1,:]' , newpricenode[j-1,0],'newprice',newprice[0])
            newpricemtx =np.vstack((newpricemtx, newprice))
    '''NOTE HERE I HAVE TO GET MAX PRICE AND MIN PRICE OF EACH PATH, IT IS TRICKY, NEED TO INCLUDE PREVIOUS PRICES'''        
#    print('newpricemtx',newpricemtx.shape)
    wholemtx=np.vstack((spotpricePaths,newpricemtx))
#    print('whole',wholemtx.shape)
    observed=wholemtx[::obs,:]
    cp = trade.getcp()
    method=trade.getmethod()
    limit=trade.getlimit()
#    print(method)
    
    if cp == -1:
        if method == 'Add':   
            maxprice=np.amax(observed,axis=0)                          
            finalstrike1 = initial_strike + threshold * np.maximum(0, np.floor((np.minimum(maxprice,limit) - initialPrice)/threshold))
       #     finalstrike2= initial_strike + threshold * np.maximum(0, np.floor((maxprice - initialPrice)/threshold))
            
        #    print(finalstrike1,finalstrike2)
            payoff=np.maximum(np.zeros(m), finalstrike1 - newpricemtx[steps-1,:])
        elif method == 'Multiply':
            maxprice=np.amax(observed,axis=0)                          
            finalstrike = initial_strike * (1+threshold * np.maximum(0, np.floor((np.minimum(maxprice,limit) - initialPrice)/threshold))/100)
            payoff=np.maximum(np.zeros(m), finalstrike - newpricemtx[steps-1,:])
            
        elif method == 'PegMax':
            maxprice=np.amax(observed,axis=0)                          
            finalstrike = (initial_strike/p0) * maxprice
            payoff=np.maximum(np.zeros(m), finalstrike - newpricemtx[steps-1,:])
            
    elif cp == 1 :
        if method =='Add':
            minprice=np.amin(observed,axis=0)
            finalstrike = initial_strike - threshold * np.maximum(0, np.floor((  initialPrice- np.maximum(limit,minprice))/threshold))
            payoff=np.maximum(np.zeros(m), newpricemtx[steps-1,:]- finalstrike ) 
        elif method == 'Multiply':
            minprice=np.amin(observed,axis=0)
            finalstrike = initial_strike *(1- threshold * np.maximum(0, np.floor((  initialPrice- np.maximum(limit,minprice))/threshold))/100)
            payoff=np.maximum(np.zeros(m), newpricemtx[steps-1,:]- finalstrike )             
        elif method == 'PegMax':
            minprice=np.amin(observed,axis=0)
            finalstrike = (initial_strike/p0) * minprice
            payoff=np.maximum(np.zeros(m), newpricemtx[steps-1,:]- finalstrike )              
             
             
#    print(np.average(payoff))    
#    print(payoff.shape)
#    payoff=discount(payoff, priceDate) 
    optionprice=np.average(payoff)
#    print(optionprice)
#==============================================================================
#         payoffmtx=np.vstack((payoffmtx,payoff))        
#==============================================================================
    return optionprice   
    

#==============================================================================
# def Getstrike(trade,initial_strike, todayPrice):
#     
#     cp = trade.getcp()
#     if cp == 'put':
#                 today_strike = initial_strike + threshold * max(0, math.floor((todayPrice - initialPrice)/threshold))
#     if cp =='call':
#                 today_strike = initial_strike + threshold * min(0, math.floor((initialPrice-todayPrice)/threshold))   
#==============================================================================


def simulateRSStock(p0,marketdata,today,step,steps,eq_vol):
    """ From the trade termsheets we received before, the option always stays OTM and the restriking always 
    tries to pull delta closer to one when the spot trend is pushing the option further OTM.  
    for puts, the option strike = initial strike + max(0, the increase of the stock if it is greater than threshold)
    for calls, when the underlying price drops: the option strike = initial + min(0, the drop of stock if it is greater than the threshold)
    """
    
    
    [m, n] = marketdata[0].shape
    ONEs = np.ones(n)
    newpricenode = ONEs    
    for j in range(0,steps):
       
        
        if(j == 0):
            newprice = ONEs * np.exp(-0.5*(eq_vol**2)*step/365.25 + np.array(marketdata[j])*eq_vol*((step/365.25)**.5))
            #newpricenode = np.array(newprice)
            newpricenode = np.vstack((newpricenode, newprice))
            #print('size ',newpricenode.shape,'j = ',j)
        else:
            #print(newpricenode[j-1])
            #print(np.array(marketdata[j][trade.getassetid()]))
            if(newpricenode.ndim == 1):
                newprice = newpricenode*np.exp(-0.5*(eq_vol**2)*step/365.25+np.array(marketdata[j])*eq_vol*((step/365.25)**.5))
            else:
                newprice = newpricenode[j,:]*np.exp(-0.5*(eq_vol**2)*step/365.25+np.array(marketdata[j])*eq_vol*((step/365.25)**.5))
                #print('newpricenode[j-1,:]' , newpricenode[j-1,0],'newprice',newprice[0])
            newpricenode =np.vstack((newpricenode, newprice))
    newpricenode=p0*newpricenode
    return newpricenode




def eqRS(trade, pricingdata, today,step,steps,vol,randomvariables):
    ls = 0
    #print(trade.getls())
    if('l' == trade.getls()):
        ls = 1
    if('s' == trade.getls()):
        ls = -1

#    initial_strike=trade.getstrike()
    
#    threshold=trade.getthreshold()
    
#==============================================================================
#     
#     settlementsteps = []
#     for getsettlementarray in range(0,len(trade.getsettlement())):
#         
#         settlementsteps.append(int(math.ceil((float(((trade.getsettlement()[getsettlementarray]-today)).days))/float(step))))
# 
#==============================================================================
    
    price0 = []
    randomvariables = np.asarray(randomvariables)
    pricingdata = np.asarray(pricingdata)
    #print(temp, temp.shape)
    
    p0=trade.getp0()
    newpricenode= simulateRSStock(p0,randomvariables,today,step,steps,vol)
    #print('len(newpricenode[0]',len(newpricenode[0]))
    price0npath = []
#    deltamatrix=[]
    #print(newpricenode[0])
    #for pathloop in range(0, len(newpricenode[0,:])):
    for pathloop in range(0,len(newpricenode[0,:])):
        price0node = []
   #     terminatePath = steps+1

#        lenofsteps = len(settlementsteps)  
    #    price0node0 = []
#        deltanode=[]
#        print('newpricenodeAMC',newpricenodeAMC.shape)
        for j in range(0,steps):
#            priceDate = today+timedelta(days=step*j)
            '''here I need to change today price to include previous price'''
        #    todayPrice = newpricenode[j,:]
            todayPricePath = newpricenode[:j+1,pathloop]
#            k = priceDate
#==============================================================================
#             todayPricePath = todayPrice[0][0][pathloop]
# 
#==============================================================================
#            print(j)
            payoff = SimRSOptionPrice(trade,pricingdata,todayPricePath,step,steps-j,vol)
#            print(payoff)
#            price0node0=discount(payoff,priceDate)
             
            '''
            
            temp = np.zeros((len(newpricenode[0,j,:]), 3)) #here needs get notional, function from tradeslist.py
            temp[:,] = (trade.getnotional(), nostrike,0)
            #print('temp',temp.shape)            
            furturedays = int(math.ceil((float((trade.getsettlement()[0]-k).days))/float(step)))
            for noasset in range(0, len(trade.getstrike())):
                #print(todayPricePath[noasset].shape,newpricenodeAMC[noasset,furturedays,:].shape)
                #print(temp.shape)
#                print(temp)
#                print(noasset)
                if(trade.getcp()[noasset] == 1) :
                    temp[(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:]*100 < trade.getstrike()[noasset]) \
                    * (temp[:,1] == nostrike)] \
                    = (0,noasset,0) 
#                    print(1,nostrike,trade.getstrike()[noasset],todayPricePath[noasset])
                else:
#                    print(todayPricePath[noasset],newpricenodeAMC[noasset,furturedays,:],trade.getstrike()[noasset])
                    temp[(todayPricePath[noasset]*newpricenodeAMC[noasset,furturedays,:]*100 > trade.getstrike()[noasset]) \
                    * (temp[:,1] == nostrike)] \
                    = (0,noasset,0)
#                    print(-1,nostrike,trade.getstrike()[noasset],todayPricePath[noasset])
#                print(temp)
#            print(temp)
            
            price0node0 = discount(temp, priceDate)
            price0node.append(price0node0)
            
            '''
            price0node.append(payoff)
            
#            if (j > 0):
#                delta= (payoff - price0node[j-1])/(todayPricePath[j] - todayPricePath[j-1])
#                deltanode.append(delta)
            
                
        
        price0node = np.asarray(price0node)
#        deltanode=np.asarray(deltanode)
#        print(price0node.shape)
        
        price0npath.append(price0node)
#        deltamatrix.append(deltanode)
#        print('price0npath',len(price0npath))
    price0npath = np.asarray(price0npath)
    price0npath = price0npath*ls
#    price0 = np.asarray(price0npath)
#    print('price0',price0npath)
    #print('price0 = ',price0,'priceDate',priceDate)
#    try:
    return np.array(np.swapaxes(price0npath,0,1)) #originally price0
#    except:
#        return np.array(price0npath)