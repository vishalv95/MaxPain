## Max Pain Theory Strategy 

Max pain theory postulates that the price of underlying has a tendency to gravitate towards a point where the maximum number of options expire worthless. Using historical open interest data, we are backtesting to see if we can identify companies where the max pain theory holds true. For qualifying companies, we could enter stock positions according to where the open interest data predicts the underlying price to be on the third week of each month. 

#### Algorithm Overview
1. Get historical options data (underlying, expiration, strikes, open interest) for all tickers in SP500, and underlying data
2. Clean Bloomberg data 
3. Compute cumulative open interest sum for OTM call options at each strike 
4. Compute cumulative open interest sum for OTM put options at each strike 
5. Find strike with maximum cumulative options OTM. Log target in window.
6. Create CI for n-day window as price target range
    + Window width 
    + CI MOE
7. Trade
    + If underlying trades below lower bound, BUY 
    + If underlying trades above upper bound, SELL/SHORT
    + If underlying trades within bounds 
        + Do nothing if not holding
        + SELL if holding 

#### Remaining Work:
+ Decide action upon approaching expiration while holding
+ Scrape options data from Bloomberg
+ Reduce data pull to a tractable set 
+ Write test cases for helper functions in backtest.py
+ Add trade logic in handle_data() 