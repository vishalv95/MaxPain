import xlrd
import pandas as pd 

# (2) Clean Bloomberg data 
def get_tickers():
	return open('../data/sp500_tickers.txt','rb').read().splitlines()

# Load book from filename
def load_raw(filename):
	book = xlrd.open_workbook(filename)
	return book 

# Read the first row to get ticker information 
def read_first(sheet):
	# Get the start index of each ticker 
	start_frames = [(i, ticker) for i, ticker in enumerate(sheet.row_values(0)) if ticker != u'']

	# Parse out information from ticker 
	# Ex. FB US 08/19/16 C120 Equity
	ticker_info = dict()
	for i, ticker in start_frames:
		meta = ticker.split()
		underlying = meta[0]
		settlement = meta[2]
		opt_type = meta[3][0]
		strike = meta[3][1:]
		ticker_info[i] = (underlying, settlement, opt_type, strike)
	return ticker_info


def parse_rows(sheet, ticker_info, start_index):
	if not is_valid_col(sheet, start_index): return

	dates = sheet.col_values(start_index, 2)
	dates = [xlrd.xldate_as_tuple(date,0) for date in dates if date != -1 and date != '']

	open_interest = sheet.col_values(start_index+1, 2) 
	open_interest = filter(lambda x: x != '', open_interest) 

	underlying, settlement, opt_type, strike = ticker_info[start_index]
	df_tuples = zip(dates, open_interest)

	df = pd.DataFrame.from_records(df_tuples, columns=['date', 'open_interest'])
	df['ticker'] = underlying
	df['expiration'] = settlement
	df['type'] = opt_type
	df['strike'] = strike 
	df['date'] = map(lambda x: str(x[0]) + '-' + str(x[1]) + '-' +  str(x[2]), df['date'])

	save_cleaned(df, '../data/cleaned_data/FB.csv')

def parse_sheet(sheet):
	ticker_info = read_first(sheet)
	for i in ticker_info.keys():
		parse_rows(sheet, ticker_info, i)


def parse_book_sheets(book):
	for sheet in book.sheets()[1:]:
		parse_sheet(sheet)


def save_cleaned(df, filename):
	file = open(filename, 'a')
	df.to_csv(file, header=False, index=False)


def is_valid_col(sheet, start_index):
	return sheet.col_values(start_index) > 3 and sheet.col_values(start_index)[3] != ''


if __name__ == '__main__':
	book = load_raw('../data/raw_options/FB options strikes.xlsx')
	parse_book_sheets(book)
	