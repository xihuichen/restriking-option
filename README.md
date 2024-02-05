# restriking-option
This tool is designed for calculating the counterparty risk exposure for re-striking option.
For details of risk metrics calculated (Potential Future Exposure) see link:https://web.stanford.edu/~duffie/Chapter_09.pdf
Structure of the tool:
1. RNGenerator
   Dependency: numpy, scipy
   A tool used to simulate variables following standard normal(0,1) distribution, given specified covariance matrix,random seed, number of samples and steps. Method by default is cholesky, alternative could be eigenvectors but needs to configure at function level.

2. tradeslist
   define the trading product, how its cashflow is structured   
3. pricer
   Dependency:RNGenerator and its dependencies,datetime,math
   
   

4. RaTool
5. PFE:
   Dependency: RNGenator
   Use monte carlo generated cashflow to calculate the PFE of given portfolio, depending on margin call frequency and percentile of stress scenario taking.
6. PFE_daily: similar to PFE but specified for daily margined trades
7. Run_trade_example
