# import pandas as pd 
# import pandas.io.data as web
from datetime import datetime 
import calendar

def get_tickers(filename):
	return open(filename,'rb').read().splitlines()[:5]

def historical_dates():
	year = range(2014, 2017)
	month = [str(m) if m >= 10 else "0" + str(m) for m in range(1, 12, 3)]

	dates = []
	for yr in year:
		for m in month:
			i = 1
			while i < 32:
				dates.append(str(m) + "/" + str(i) + "/" + str(yr))
				i += 1
	return dates

def is_third_friday(date):
	try:
		d = datetime.strptime(date, "%m/%d/%Y")

	except:
		return 
	return d.weekday() == 4 and 14 < d.day < 22

def third_fridays():
	third_fridays = []
	for day in historical_dates():
		if is_third_friday(day):
			third_fridays.append(day)
	return third_fridays

def strikes():
	strikes = range(100, 250, 5)
	#how to generate strikes???
	return strikes

def calls():
	calls = []
	for s in strikes():
		calls.append("C" + str(s))
	return calls

def puts():
	puts = []
	for s in strikes():
		puts.append("P" + str(s))
	return puts

def option_name(ticker_file):
	tickers = []
	for stock in get_tickers('../data/sp500_tickers.txt'):
		for date in third_fridays():
			for c in calls():
				tickers.append(stock + " US " + date + " " + c + " Equity")
			for p in puts():
				tickers.append(stock + " US " + date + " " + p + " Equity")
	print len(tickers)

if __name__ == '__main__':
	option_name('../data/option_tickers.txt')