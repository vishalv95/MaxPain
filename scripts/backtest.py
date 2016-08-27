from zipline.api import (
	# add_history,
	history,
	order_target_percent,
	order,
	record,
	symbol,
	get_datetime,
	schedule_function,
)
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo
import numpy as np 
import pandas as pd 
from datetime import datetime 

def initialize(context):
	context.target_window = dict()

	# context.underlying = pd.read_csv('../data/underlying/FB.csv')
	# context.underlying = pd.to_datetime(context.underlying['Date'])

	context.options = pd.read_csv('../data/cleaned_data/FB.csv')
	context.options['date'] = pd.to_datetime(context.options['date'])
	context.options['expiration'] = pd.to_datetime(context.options['expiration'])

# (7) Trade
def handle_data(context, data):
	# check if the spot is outside CI of MPP
	day_option_df = context.options[context.options['date'] == get_datetime()]
	call_sums = call_otm(day_option_df, 'FB', get_datetime())
	put_sums = put_otm(day_option_df, 'FB', get_datetime())
	
	add_to_window(context, 10, max_pain_strike(call_sums, put_sums), 'FB')
	ci = CI(context.window, 1)

	price = history(1, '1d', 'price').iloc[0,0]
	if price < ci[0]: order_target_percent(symbol('FB'), 1)
	elif price > ci[1]: order_target_percent(symbol('FB'), 0)


# (3) Compute cumulative open interest sum for OTM call options at each strike 
def call_otm(df, ticker, date):
	copy_df = df
	copy_df = copy_df[copy_df['type'] == 'C']
	copy_df = copy_df[copy_df['date'] == date]
	copy_df = copy_df[copy_df['ticker'] == ticker]
	copy_df.sort_values('strike', axis=0, ascending = False, inplace = True)
	
	copy_df['cumsum_c'] = pd.Series.cumsum(copy_df['open_interest'])
	
	return copy_df

# (4) Compute cumulative open interest sum for OTM call options at each strike 
def put_otm(df, ticker, date):
	copy_df = df
	copy_df = copy_df[copy_df['type'] == 'P']
	copy_df = copy_df[copy_df['ticker'] == ticker]
	copy_df = copy_df[copy_df['date'] == date]
	copy_df.sort_values('strike', axis=0, ascending = True, inplace = True)

	copy_df['cumsum_p'] = pd.Series.cumsum(copy_df['open_interest'])
	return copy_df

# (5) Find strike with maximum cumulative options OTM. Log target in window.
# target_window is just for one stock
def max_pain_strike(call_sums, put_sums):
	cumulative = call_sums.join(put_sums, on = 'strike', how = 'inner')
	cumulative['cp_sum'] = cumulative['cumsum_c'] + cumulative['cumsum_p']
	mpp = cumulative.ix[cumulative['cp_sum'].idxmax()]['strike']
	
	return mpp

def add_to_window(context, window_size, datapoint, ticker):
	tw = context.target_window[ticker]

	tw.append(datapoint)
	context.target_window[ticker] = tw[-window_size:] if len(tw) > window_size else tw
	

# (6) Create CI for n-day window as price target range
# Return tuple with upper and lower bound
def CI(window, sds):
	mean = 	np.mean(window)
	sd = np.std(window)

	return (mean - sds * sd, mean + sds * sd)

if __name__ == '__main__':
	universe = ['FB']
	data = load_from_yahoo(stocks=universe,
		indexes={}, start=datetime(2016, 4, 3), 
		end=datetime.today())  
	olmar = TradingAlgorithm(initialize=initialize, handle_data=handle_data, capital_base=10000)  
	backtest = olmar.run(data)
	backtest.to_csv('backtest-50-2012.csv') 
	print backtest['algorithm_period_return'][-1]

	import pyfolio as pf
	returns, positions, transactions, gross_lev = pf.utils.extract_rets_pos_txn_from_zipline(backtest)
	pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions, gross_lev=gross_lev, live_start_date='2004-10-22')