import pandas as pd 
import pandas.io.data as web
from datetime import datetime 

# (1) Get underlying data

def get_tickers(filename):
	return open(filename,'rb').read().splitlines()

def save_ts(ticker_file):
	for stock in get_tickers(ticker_file):
		if stock != 'FB': continue 
		start = datetime.strptime("1/1/1975", "%m/%d/%Y")
		end = datetime.today()
		try:
			f = web.DataReader(stock, 'yahoo', start, end)
			f['Returns'] = (f['Close'][1:] - f['Open'][:-1]) / f['Open'][:-1]
			stock = stock.replace('/','-')
			f.to_csv('../data/underlying/' + stock + '.csv')
		except:
			continue
	

if __name__ == '__main__':
	save_ts('../data/sp500_tickers.txt')