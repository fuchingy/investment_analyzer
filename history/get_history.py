#!/usr/bin/python
from yahoo_finance import Share
import csv

def save_history_csv(stock_name):
    csv_f_name = stock_name+'.csv'
    print "Saving to %s" % (csv_f_name)
    # Get start date and end date
    from_date = Share(stock_name).get_info()['start']
    to_date = Share(stock_name).get_info()['end']

    # Retrieve all records and save as a csv file
    records = Share(stock_name).get_historical(from_date, to_date)
    with open(csv_f_name, 'w') as csvfile:
        w = csv.DictWriter(csvfile, records[0].keys())
        w.writeheader()
        for record in records:
            w.writerow(record)

save_history_csv('VTI')
save_history_csv('VGK')
save_history_csv('VPL')
save_history_csv('VWO')
save_history_csv('BND')
save_history_csv('BNDX')
save_history_csv('IPE')
save_history_csv('WIP')
