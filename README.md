# restriking-option
This tool is designed for calculating the counterparty risk exposure for re-striking option.
For details of risk metrics calculated (Potential Future Exposure) see link:https://web.stanford.edu/~duffie/Chapter_09.pdf
Structure of the tool:
1. RNGenerator
2. pricer
3. tradeslist
   define the trading product, how its cashflow is structured
5. RaTool
6. PFE:
   Dependency: RNGenator
   Use monte carlo generated cashflow to calculate the PFE of given portfolio, depending on margin call frequency and percentile of stress scenario taking.
7. PFE_daily: similar to PFE but specified for daily margined trades
8. Run_trade_example
