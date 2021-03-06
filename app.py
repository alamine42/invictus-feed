from __future__ import print_function

from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, session, flash, redirect, url_for
from utils import exec_sql
from workout import WOD, WORKOUTS_TABLE, LEVELS
from invictus import update_wods

# Create application object
app = Flask(__name__)

def format_query(starting_date, ending_date, level='fitness'):
	return 'SELECT * FROM {tbl} ' \
		'WHERE workout_date >= \"{start_date}\" ' \
		'AND workout_date < \"{end_date}\" ' \
		'AND workout_level = \"{wod_level}\";'.\
		format(tbl=WORKOUTS_TABLE, 
			start_date=str(starting_date),
			end_date=str(ending_date), 
			wod_level=level)

def get_workouts(starting_date, ending_date, level='fitness'):
	query = format_query(starting_date, ending_date, level)
	wods = exec_sql(query)
	return wods

def get_week_start_end(week):
	pass


@app.route("/")
def view_all():

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_till_end_of_week = 7 - today.weekday()

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	next_monday_date = today + timedelta(days=days_till_end_of_week)

	this_week_fitness_wods = get_workouts(last_monday_date, next_monday_date, 'fitness')
	this_week_performance_wods = get_workouts(last_monday_date, next_monday_date, 'performance')

	this_week_wods = {
		'fitness': this_week_fitness_wods, 
		'performance': this_week_performance_wods
		}

	data = {
		'today': today
	}

	return render_template('index.html', weekly_wods=this_week_wods, data=data)

@app.route("/fitness")
def view_fitness():

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_till_end_of_week = 7 - today.weekday()

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	next_monday_date = today + timedelta(days=days_till_end_of_week)

	this_week_fitness_wods = get_workouts(last_monday_date, next_monday_date, 'fitness')

	this_week_wods = {
		'fitness': this_week_fitness_wods
		}

	return render_template('fitness.html', weekly_wods=this_week_wods)

@app.route("/performance")
def view_performance():

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_till_end_of_week = 7 - today.weekday()

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	next_monday_date = today + timedelta(days=days_till_end_of_week)

	this_week_fitness_wods = get_workouts(last_monday_date, next_monday_date, 'performance')

	this_week_wods = {
		'performance': this_week_fitness_wods
		}

	return render_template('performance.html', weekly_wods=this_week_wods)

@app.route("/lastweek")
def view_last_week():

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_since_start_of_last_week = days_since_start_of_week + 7

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	monday_before_last = today - timedelta(days=days_since_start_of_last_week)

	last_week_fitness_wods = get_workouts(monday_before_last, last_monday_date, 'fitness')
	last_week_performance_wods = get_workouts(monday_before_last, last_monday_date, 'performance')

	last_week_wods = {
		'fitness': last_week_fitness_wods, 
		'performance': last_week_performance_wods
		}

	return render_template('index.html', weekly_wods=last_week_wods)

@app.route("/lastyear")
def view_last_year():

	today = date.today()
	one_year_ago = today - timedelta(days=365)

	days_since_start_of_week = one_year_ago.weekday()
	days_till_end_of_week = 7 - one_year_ago.weekday()

	previous_monday_date = one_year_ago - timedelta(days=days_since_start_of_week)
	following_monday_date = one_year_ago + timedelta(days=days_till_end_of_week)

	last_year_fitness_wods = get_workouts(previous_monday_date, following_monday_date, 'fitness')
	last_year_performance_wods = get_workouts(previous_monday_date, following_monday_date, 'performance')

	last_year_wods = {
		'fitness': last_year_fitness_wods, 
		'performance': last_year_performance_wods
		}

	return render_template('index.html', weekly_wods=last_year_wods)

if __name__ == '__main__':
	app.run(port=8000, debug=True)


