import numpy as np
import matplotlib.pyplot as plt
from RNG import RNGenerator

def PFEs(pvlist,simpleList,noTrades,ratio,perct):
    [steps, n] = pvlist[0].shape
    print('steps = ' + str(steps) + ', n = ' + str(n))
    portfolioexposure = np.zeros((steps, n))
    for count in range(0, int(noTrades)):
        portfolioexposure += pvlist[count] 
#    stepsM=np.round(steps/ratio,decimals=0)
    pvportfolionode = np.zeros((steps, n))
    for j in range(0, steps):
        for i in range(0, n):
            #pvportfolionode[j][i] = pvportfolionode[j - 1][i] + portfolioexposure[j][i]
            #pvportfolionode[j][i] =  portfolioexposure[j][i] -  portfolioexposure[0][i]
            pvportfolionode[j][i] =  portfolioexposure[j][i]
    portfolioPFE = np.zeros(steps)
    for i in range(0, steps):
        portfolioPFE[i]=np.percentile(pvportfolionode[i], perct*100)
    marginedportfolionode=pvportfolionode[::ratio,:]
    
    return (portfolioPFE, marginedportfolionode )

