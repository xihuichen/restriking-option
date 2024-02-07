# restriking-option
This tool is designed for calculating the counterparty risk exposure for a lot of non standard OTC derivatives, for example re-striking option, auto-calls, snow balls, digital options, contingent options using monte carlo simulation. The brief introduction "mc on mc" means for path dependent derivatives, monte carlo on monte carlo is used to simulate the price evolution and calculate the exposure.
For details of risk metrics calculated (Potential Future Exposure) see link:https://web.stanford.edu/~duffie/Chapter_09.pdf
Structure of the tool:
1. RNGenerator
   Dependency: numpy, scipy
   A tool used to simulate variables following standard normal(0,1) distribution, given specified covariance matrix,random seed, number of samples and steps. Method by default is cholesky, alternative could be eigenvectors but needs to configure at function level.

2. tradeslist
   define the trading product, how its cashflow is structured
3. pricer
   Dependency:RNGenerator and its dependencies,datetime,math, tradeslist
   Even though there is no explicit import of tradeslist module but the trade object (an instance of tradeslist class) would be the input of the pricing function. The simulated cashflow of Equity, Equity Option, wouldn't be discounted at current interest rate, at the time of development this wasn't a problem because the interest rate was negative to near zero, but should be altered given current high interest rate environment(2024).
   Everytime there's a new product to be priced, user need to define a simulate cashflow function according to its termsheet and leverage the simulateAllStocks() function to define a pricing function for that product/instrument.
   For re-striking option, see SimRSOptionPrice and simulateRSStock, eqRS.
   In a hindsight, the product definition functions should be moved to pricer class to achieve single responsibility principle in Object Oriented Software Development.

4. PFE:
   Dependency: RNGenator
   Use monte carlo generated cashflow to calculate the PFE of given portfolio, depending on margin call frequency and percentile of stress scenario taking.
   Hard-coded percentile 97.7 to get two standard deviation from the simulated sample mean (standard normal distribution mentioned above)
5. PFE_daily: similar to PFE but specified for daily margined trades
6. RaTool
   Dependencies: os, sys, numpy, matplotlib,RNGenerator, tradeslist,pricer,copy,PFE, csv
   Using above classes to compile a portfolio(consisted of different type of products), apply different netting/margining Credit Support Annex(A credit support annex is a legal document regulating the terms and conditions under which collateral is posted to mitigate counterparty credit risk in bilateral derivatives transactions. It is a voluntary annex within the International Swaps and Derivatives Association Master Agreement), calculate the portfolio's PFE profile, plot the profile and save the simulated exposure data to csv.
7. Run_trade_example
   The sample file for user to use this tool
