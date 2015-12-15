#!/usr/bin/python
from yahoo_finance import Share
import config_parser
import csv
import datetime

def get_stock_info(stock, target_date):
    f = open('./history/' + stock['name'] + '.csv', 'r')
    records = csv.DictReader(f)
    for record in records:
        record_date = datetime.datetime.strptime(record['Date'], '%Y-%m-%d')
        if record_date <= target_date:
            return record

def get_stock_close_price(stock, date):
    stock_info = get_stock_info(stock, date)
    close_price = float(stock_info['Adj_Close'])
    return close_price

def get_rate(old_val, new_val):
    if old_val != 0:
        return round( (new_val - old_val) / old_val * 100, 2)
    else:
        return 0

def print_cur_asset(stocks, total_cost):
    total_value = 0
    for stock_name, stock in stocks.iteritems():
        print "{0}:\t{1} -> {2} \t({3}%)".format(
              stock_name,
              stock['pre_price'],
              stock['cur_price'],
              get_rate(stock['pre_price'], stock['cur_price'])
              )
        print "{0}:\t{1} -> {2} \t({3}%)".format(
              stock_name,
              stock['pre_val'],
              stock['cur_val'],
              get_rate(stock['pre_val'], stock['cur_val'])
              )
        total_value = total_value + stock['cur_hold'] * stock['cur_price']

    print "Summary: {0}/{1} ({2}%)".format(
          round(total_value, 0),
          total_cost,
          get_rate(total_cost, total_value))

# Evaluation parameters
start_date = '2013-06-04'
interval = datetime.timedelta(days=90)
end_date = '2015-12-15'
invest_amount = 75000

# Initialize date
cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
idx = 0

# Initialize stock info
stocks = config_parser.get_all("stock_cfg.ini")
for stock_name, stock in stocks.iteritems():
    stock['name'] = stock_name
    stock['pre_price'] = 0
    stock['pre_hold'] = 0
    stock['pre_val'] = 0
    stock['cur_price'] = 0
    stock['cur_hold'] = 0
    stock['cur_val'] = 0

#for idx, invest_date in enumerate(invest_dates):
while(cur_date <= end_date):
    print cur_date

    for stock_name, stock in stocks.iteritems():
        stock['pre_price'] = stock['cur_price']
        stock['pre_hold'] = stock['cur_hold']
        stock['pre_val'] = stock['cur_val']

    # Calculate total market value
    total_value = 0
    for stock_name, stock in stocks.iteritems():
        stock['cur_price'] = get_stock_close_price(stock, cur_date)
        stock['cur_val'] = stock['cur_hold'] * stock['cur_price']
        total_value = total_value + stock['cur_val']

    print_cur_asset(stocks, (idx) * invest_amount)

    # New invest, based on weight
    total_value = total_value + invest_amount
    for stock_name, stock in stocks.iteritems():
        stock['cur_hold'] = total_value * float(stock['weight']) / stock['cur_price']
        stock['cur_val'] = stock['cur_hold'] * stock['cur_price']

    #print_cur_asset(stocks, (idx) * invest_amount)

    print "-------------------------------"

    idx = idx + 1
    cur_date = cur_date + interval
