#for portfolio PFE
import numpy as np
import matplotlib.pyplot as plt
from RNG import RNGenerator

# This funciton helps get portfolio level PV matrix
def PFEs(pvlist,simpleList,noTrades,perct):
    [steps, n] = pvlist[0].shape
    print('steps = ' + str(steps) + ', n = ' + str(n))
    portfolioexposure = np.zeros((steps, n))
    for count in range(0, int(noTrades)):
        portfolioexposure += pvlist[count] 

    pvportfolionode = np.zeros((steps, n))
    for j in range(0, steps):
        for i in range(0, n):
            #pvportfolionode[j][i] = pvportfolionode[j - 1][i] + portfolioexposure[j][i]
            #pvportfolionode[j][i] =  portfolioexposure[j][i] -  portfolioexposure[0][i]
            pvportfolionode[j][i] =  portfolioexposure[j][i]
    portfolioPFE = np.zeros(steps)
    for i in range(0, steps):
        portfolioPFE[i]=np.percentile(pvportfolionode[i], perct*100)
    
    return (portfolioPFE, pvportfolionode, )

