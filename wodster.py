from __future__ import print_function

import argparse
from datetime import datetime, date, timedelta

from utils import exec_sql

def get_latest_wod(level):
	latest_wod_sql = 'SELECT MAX(workout_date) FROM {tbl} WHERE workout_level = \"{wod_level}\"'.\
		format(tbl=WORKOUTS_TABLE, wod_level=level)

	today = date.today()
	days_subtract = today.weekday() + 7
	last_monday = today - timedelta(days=days_subtract)

	results = exec_sql(latest_wod_sql, WORKOUTS_FILE)
	if results[0][0] is not None:
		latest_date_str = results[0][0]
		latest_wod_date = datetime.strptime(latest_date_str, '%Y-%m-%d').date()
		if latest_wod_date > last_monday:
			return latest_wod_date

	return last_monday
	

def get_list_dates_to_retrieve(level):

	list_of_dates_to_retrieve = []
	latest_wod_date = get_latest_wod(level)
	today = date.today()
	delta = today - latest_wod_date
	for i in range(1, delta.days):
		list_of_dates_to_retrieve.append(latest_wod_date + timedelta(days=i))		
	return list_of_dates_to_retrieve

def update_wods():
	print('Updating WOD database ...')
	for level in LEVELS:
		list_of_dates = get_list_dates_to_retrieve(level)
		if len(list_of_dates) > 0:
			for wod_date in list_of_dates:
				wod_day = wod_date.strftime('%A')
				wod = WOD(wod_date, wod_day, level)
				wod.retrieve()
				wod.save()
				# print(wod)
			print('All WODs updated for %s' % level)
		else:
			print('Nothing to update for %s' % level)

def main():
	update_wods()

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='WODSTER')
	parser.add_argument('-p', '--program', type=str,  
		default='comptrain',
		choices=['comptrain', 'invictus'],
		help='Specify source programming (Default: comptrain)'
		)

	args = parser.parse_args()
	if args.program == 'invictus':
		from get_invictus import WOD, WORKOUTS_TABLE, LEVELS, WORKOUTS_FILE
	else:
		from get_comptrain import WOD, WORKOUTS_TABLE, LEVELS, WORKOUTS_FILE

	print(update_wods())