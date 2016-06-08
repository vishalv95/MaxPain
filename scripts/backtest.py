import zipline
import numpy as np 
import pandas as pd 
import datetime 

# TODO: Parallelize operations 

def initialize(context):
	context.target_window = []

# (7) Trade
def handle_data(context, data):
	pass

# (3) Compute cumulative open interest sum for OTM call options at each strike 
def call_otm():
	pass

# (4) Compute cumulative open interest sum for OTM call options at each strike 
def put_otm():
	pass
# (5) Find strike with maximum cumulative options OTM. Log target in window.
def max_pain_strike(call_sums, put_sums, context, window_size):
	pass

# (6) Create CI for n-day window as price target range
# Return tuple with upper and lower bound
def CI(window, sds):
	pass
