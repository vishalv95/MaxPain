import zipline
import numpy as np 
import pandas as pd 
import datetime 

def initialize(context):
	context.target_window = dict()
	context.df = pd.read_csv(file)

# (7) Trade
def handle_data(context, data):
	pass

# (3) Compute cumulative open interest sum for OTM call options at each strike 
def call_otm(df, ticker, date):
	copy_df = df
	copy_df = copy_df[copy_df['type'] == 'C']
	copy_df = copy_df[copy_df['date'] == date]
	copy_df = copy_df[copy_df['ticker'] == ticker]
	copy_df.sort('strike', ascending = False, inplace = True)
	
	copy_df['cumsum_c'] = pd.cumsum(copy_df['open_interest'])
	
	return copy_df

# (4) Compute cumulative open interest sum for OTM call options at each strike 
def put_otm(df, ticker, date):
	copy_df = df
	copy_df = copy_df[copy_df['type'] == 'P']
	copy_df = copy_df[copy_df['ticker'] == ticker]
	copy_df = copy_df[copy_df['date'] == date]

	copy_df.sort('strike', ascending = True, inplace = True)

	copy_df['cumsum_p'] = pd.cumsum(copy_df['open_interest'])
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
