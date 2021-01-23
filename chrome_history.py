## takes a chrome history file sqlite db and outputs download and web history in CSV format
## usage: chrome_history.py -i $inputfile -o $outputdirectory
## chrome history file is typically located in C:\Users\$username\AppData\Local\Google\Chrome\User Data\Default

import argparse
import sqlite3
import os
import csv
import pandas as pd


def downloads(filename, path):
	downloads_path = path + "/downloads.csv"
	downloads_query = "SELECT id, current_path, target_path, start_time, received_bytes, total_bytes, state, danger_type, \
interrupt_reason, end_time, opened, last_access_time, referrer, site_url, tab_url, tab_referrer_url, mime_type FROM downloads"
	conn = sqlite3.connect(filename, isolation_level=None,
	                       detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query(downloads_query, conn)
	db_df.to_csv(downloads_path, index=False)


def web_history(filename, path):
	history_path = path + "/history.csv"
	history_query = "SELECT visits.id, visits.visit_time, urls.url, urls.title FROM visits INNER JOIN urls ON visits.url = urls.id"
	conn = sqlite3.connect(filename, isolation_level=None,
	                       detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query(history_query, conn)
	db_df.to_csv(history_path, index=False)


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
