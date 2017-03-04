import csv

seconds_in_hour = 60*60

filepath = 'data/delay_data/fahrzeitensollist2016010320160109'

data_file = open(filepath+'.csv', 'r')
csv_file = csv.reader(data_file)
data_rows = [row for row in csv_file]
data_file.close()

headers = data_rows[0]
data_rows = data_rows[1:-1]

headers_map = dict([(t[1], t[0]) for t in enumerate(headers)])
lines = set([row[headers_map['\ufefflinie']] for row in data_rows])
dates = set([row[headers_map['betriebsdatum']] for row in data_rows])

def select_line_rows(rows, line):
    lines_rows = [row for row in rows if row[0]==line]
    return lines_rows

def select_timeframe(rows, start, end):
    time_rows = [row for row in rows if start <= int(row[11]) and int(row[12]) <= end]
    return time_rows

def delay(row):
    return max(0, int(row[headers_map['ist_an_von']]) - int(row[headers_map['soll_an_von']]))

def timeframe_delay(rows, start, end):
    delays = [delay(row) for row in select_timeframe(start, end)]
    return sum(delays)

def hourly_time_resolution():
    return [(seconds_in_hour*i, seconds_in_hour*(i+1)) for i in range(24)]

def gen_delay_row(rows, line, date):
    timeframes = hourly_time_resolution()[6:23]
    rows_on_date = [row for row in rows if row[headers_map['betriebsdatum']] == date]
    delays = [sum([delay(row) for row in select_timeframe(select_line_rows(rows_on_date, line), tf[0], tf[1])]) for tf in timeframes]
    result = [line, date]
    result.extend(delays)
    return result

def gen_delay_row_without_line(rows, date):
	timeframes = hourly_time_resolution()[6:23]
	rows_on_date = [row for row in rows if row[headers_map['betriebsdatum']] == date] 
	delays = [sum([delay(row) for row in select_timeframe(rows_on_date, tf[0], tf[1])]) for tf in timeframes]
	result = [date]
	result.extend(delays)
	return result

def write_out_csv(out_path, rows):
    out_file = open(out_path+'.csv', 'w')
    out_csv = csv.writer(out_file)
    delay_rows = [gen_delay_row_without_line(rows, date) for date in dates]
    out_csv.writerows(delay_rows)
    out_file.close()
        
out_path = filepath+'_delays_without_line'

write_out_csv(out_path, data_rows)



