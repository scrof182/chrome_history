import argparse
import sqlite3
import os
import pandas as pd
import datetime

def danger_state(state):
	state = str(state)
	state_converter = {"0":"Not Dangerous", "1":"Dangerous", "2":"Dangerous URL", "3":"Dangerous Content", \
	"4":"Content May Be Malicious", "5":"Uncommon Content", "6":"Dangerous But User Validated", \
	"8":"Potentially Unwanted", "9":"Whitelisted by Policy"}
	for key in state_converter.keys():
		state = state.replace(key, state_converter[key])
	return state

def download_state(state):
	state = str(state)
	state_converter = {"0":"In Progress", "1":"Complete", "2":"Cancelled", "3":"Interrupted", "4":"Interrupted"}
	for key in state_converter.keys():
		state = state.replace(key, state_converter[key])
	return state

def interrupt_reason(reason):
	reason = str(reason)
	reason_converter = {"0":"No Interrupt", "1":"File Error", "2":"Access Denied", "3":"Disk Full", \
	"5":"Path Too Long", "6":"File Too Large", "7":"Virus", "10":"Temporary Problem", \
	"11":"Blocked", "12":"Security Check Failed", "13":"Resume Error", "20":"Network Error", \
	"21":"Operation Timed Out", "22":"Connection Lost", "23":"Server Down", "30":"Server Error", \
	"31":"Range Request Error", "32":"Server Precondition Error", "33":"Unable to get file", \
	"34":"Server Unauthorized", "35":"Server Certificate Problem.", "36":"Server Access Forbidden", \
	"37":"Server Unreachable", "38":"Content Length Mismatch", "39":"Cross Origin Redirect", \
	"40":"Cancelled", "41":"Browser Shutdown", "50":"Browser Crashed"}
	for key in reason_converter.keys():
		reason = reason.replace(key, reason_converter[key])
	return reason 

def date_from_webkit(webkit_timestamp):
	epoch_start = datetime.datetime(1601,1,1)
	delta = datetime.timedelta(microseconds=int(webkit_timestamp))
	return epoch_start + delta

def downloads(filename, path):
	downloads_csv_path = path + "/downloads.csv"
	downloads_html_path = path + "/downloads.html"
	downloads_query = "SELECT id, current_path, target_path, start_time, received_bytes, total_bytes, state, danger_type, \
interrupt_reason, end_time, opened, last_access_time, referrer, site_url, tab_url, tab_referrer_url, mime_type FROM downloads"
	conn = sqlite3.connect(filename, isolation_level=None,
	                       detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query(downloads_query, conn)
	db_df['start_time'] = db_df['start_time'].apply(date_from_webkit)
	db_df['end_time'] = db_df['end_time'].apply(date_from_webkit)
	db_df['last_access_time'] = db_df['last_access_time'].apply(date_from_webkit)
	db_df['state'] = db_df['state'].apply(download_state)
	db_df['danger_type'] = db_df['danger_type'].apply(danger_state)
	db_df['interrupt_reason'] = db_df['interrupt_reason'].apply(interrupt_reason)
	db_df.to_csv(downloads_csv_path, index=False)
	db_df.to_html(downloads_html_path, index=False)

def web_history(filename, path):
	history_csv_path = path + "/history.csv"
	history_html_path = path + "/history.html"
	history_query = "SELECT visits.id, visits.visit_time, urls.url, urls.title FROM visits INNER JOIN urls ON visits.url = urls.id"
	conn = sqlite3.connect(filename, isolation_level=None,
	                       detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query(history_query, conn)
	db_df['visit_time'] = db_df['visit_time'].apply(date_from_webkit)
	db_df.to_csv(history_csv_path, index=False)
	db_df.to_html(history_html_path, index=False)

def main():
	parser = argparse.ArgumentParser(description='Converts Chrome History File to CSV')
	parser.add_argument('-i', '--input', required=True, help='Input File Name')
	parser.add_argument('-o', '--output', required=True, help='Output Directory Name')
	args = parser.parse_args()
	os.mkdir(args.output)
	downloads(args.input, args.output)
	web_history(args.input, args.output)

if __name__ == '__main__':
    main()
