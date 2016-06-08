import xlrd
import pandas as pd 
import csv 
import datetime 

# (2) Clean Bloomberg data 

def get_tickers():
	return open('../data/sp500_tickers.txt','rb').read().splitlines()

def load_raw(filename):
	pass

def get_underlying(cell):
	pass

def get_expiration(cell):
	pass

def get_strike(cell):
	pass

def get_open_interest(cell):
	pass

def save_cleaned(filename):
	pass

