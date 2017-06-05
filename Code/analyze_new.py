from postgres import Postgres

import numpy as np
import pandas as pd
import warnings
from datetime import datetime, timedelta
from random import randint
import pprint
import time

from sklearn.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model


warnings.filterwarnings('ignore')

class Crime():
	def __init__(self):
		self.p 		= Postgres(False)
		self.cross_val 	= {
			1: {
				'train': {'start':'2016-10-01', 'end': '2017-03-31'},
				'test':  {'start':'2017-04-01', 'end': '2017-04-30'}
			},
			2: {
				'train': {'start':'2016-09-01', 'end': '2017-02-28'},
				'test':  {'start':'2017-03-01', 'end': '2017-03-31'}
			},
			3: {
				'train': {'start':'2016-08-01', 'end': '2017-01-31'},
				'test':  {'start':'2017-02-01', 'end': '2017-02-28'}
			},
			4: {
				'train': {'start':'2016-07-01', 'end': '2016-12-31'},
				'test':  {'start':'2017-01-01', 'end': '2017-01-31'}
			},
			5: {
				'train': {'start':'2016-06-01', 'end': '2016-11-30'},
				'test':  {'start':'2016-12-01', 'end': '2016-12-31'}
			},
			6: {
				'train': {'start':'2016-05-01', 'end': '2016-10-31'},
				'test':  {'start':'2016-11-01', 'end': '2016-11-30'}
			},
			7: {
				'train': {'start':'2016-04-01', 'end': '2016-09-30'},
				'test':  {'start':'2016-10-01', 'end': '2016-10-31'}
			},
			8: {
				'train': {'start':'2016-03-01', 'end': '2016-08-31'},
				'test':  {'start':'2016-09-01', 'end': '2016-09-30'}
			},
			9: {
				'train': {'start':'2016-02-01', 'end': '2016-07-31'},
				'test':  {'start':'2016-08-01', 'end': '2016-08-31'}
			},
			10: {
				'train': {'start':'2016-01-01', 'end': '2016-06-30'},
				'test':  {'start':'2016-07-01', 'end': '2016-07-31'}
			},
		}

	def get_cv(self, future_days, training_days):
		days_to_run = []
		future_days = future_days - 1
		# print  future_days, training_days
		for iterations in range(0):
			base = randint(1, 380)
			rand_date_in_range = datetime(2016, 3, 1) + timedelta(base)
			days_to_run.append({
				'train': {	
					'start': (rand_date_in_range - timedelta(training_days)).strftime('%Y-%m-%d'),  
					'end': (rand_date_in_range - timedelta(1)).strftime('%Y-%m-%d')},
				'test':  {
					# 'rand_date_in_range': rand_date_in_range.strftime('%Y-%m-%d'), 
					'start': (rand_date_in_range + timedelta(future_days)).strftime('%Y-%m-%d'),
					'end': (rand_date_in_range + timedelta(future_days)).strftime('%Y-%m-%d')}
			})
		# pprint.pprint(days_to_run)
		return days_to_run

	def get_data(self, dates, shape):
		final_res = {'train': None, 'test': None}
		# print dates
		# exit(0)
		for data_set in ['train', 'test']:
			query = """
			SELECT * FROM (
				SELECT 
					dt,
					gid,
					gid_crime_theft,
					
					LAG(gid_lights_ally_homeless_false, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_lights_ally_homeless_false,
					LAG(gid_lights_ally_homeless_true, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_lights_ally_homeless_true,
					LAG(gid_building_violations, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_building_violations,
					LAG(gid_crime_non_theft, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_crime_non_theft,
					LAG(gid_crime_theft, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_crime_theft,
					LAG(gid_food_fail, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_food_fail,
					LAG(gid_food_pass, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_food_pass,
					LAG(gid_food_pass_w_conditions, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_food_pass_w_conditions,
					LAG(gid_graffitti, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_graffitti,
					LAG(gid_sanitation_requests, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_sanitation_requests,
					LAG(gid_vacant_gang_false, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_vacant_gang_false,
					LAG(gid_vacant_gang_true, 1) OVER (partition by gid ORDER BY dt ASC) prev_gid_vacant_gang_true,
					
					LAG(neigh_lights_ally_homeless_false, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_lights_ally_homeless_false,
					LAG(neigh_lights_ally_homeless_true, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_lights_ally_homeless_true,
					LAG(neigh_building_violations, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_building_violations,
					LAG(neigh_crime_non_theft, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_crime_non_theft,
					LAG(neigh_crime_theft, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_crime_theft,
					LAG(neigh_food_fail, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_food_fail,
					LAG(neigh_food_pass, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_food_pass,
					LAG(neigh_food_pass_w_conditions, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_food_pass_w_conditions,
					LAG(neigh_graffitti, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_graffitti,
					LAG(neigh_sanitation_requests, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_sanitation_requests,
					LAG(neigh_vacant_gang_false, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_vacant_gang_false,
					LAG(neigh_vacant_gang_true, 1) OVER (partition by gid ORDER BY dt ASC) prev_neigh_vacant_gang_true,
					
					gid_tweets_bad,
					gid_tweets_good,
					gid_liquor_licenses,
					gid_red_light_tickets,

					neigh_tweets_bad,
					neigh_tweets_good,
					neigh_liquor_licenses,
					neigh_red_light_tickets
				FROM final_data.%s
				) C
			WHERE
				prev_gid_crime_theft IS NOT NULL AND
				dt >= '%s' AND
				dt <= '%s'
			""" % (	shape,
					dates[data_set]['start'], 
					dates[data_set]['end']
					)
			# print query
			res = self.p.query_list(query)
			d = pd.DataFrame(res, columns=[
					'dt',
					'gid',
					'gid_crime_theft',
					'prev_gid_lights_ally_homeless_false',
					'prev_gid_lights_ally_homeless_true',
					'prev_gid_building_violations',
					'prev_gid_crime_non_theft',
					'prev_gid_crime_theft',
					'prev_gid_food_fail',
					'prev_gid_food_pass',
					'prev_gid_food_pass_w_conditions',
					'prev_gid_graffitti',
					'prev_gid_sanitation_requests',
					'prev_gid_vacant_gang_false',
					'prev_gid_vacant_gang_true',
					'prev_neigh_lights_ally_homeless_false',
					'prev_neigh_lights_ally_homeless_true',
					'prev_neigh_building_violations',
					'prev_neigh_crime_non_theft',
					'prev_neigh_crime_theft',
					'prev_neigh_food_fail',
					'prev_neigh_food_pass',
					'prev_neigh_food_pass_w_conditions',
					'prev_neigh_graffitti',
					'prev_neigh_sanitation_requests',
					'prev_neigh_vacant_gang_false',
					'prev_neigh_vacant_gang_true',
					'gid_tweets_bad',
					'gid_tweets_good',
					'gid_liquor_licenses',
					'gid_red_light_tickets',
					'neigh_tweets_bad',
					'neigh_tweets_good',
					'neigh_liquor_licenses',
					'neigh_red_light_tickets'
				])
			final_res[data_set] = d
		return final_res

	def plot(self, x, y, y_hat):
		plt.scatter(x, y,  color='black')
		plt.plot(x, y_hat, color='blue', linewidth=3)

		plt.xticks(())
		plt.yticks(())

		plt.show()

	def run_spatial_ols(self, dates, shape):
		data = self.get_data(dates, shape)
		
		y_train = data['train']['gid_crime_theft'].values
		x_train = data['train'][[	'prev_gid_lights_ally_homeless_false',
					'prev_gid_lights_ally_homeless_true',
					'prev_gid_building_violations',
					'prev_gid_crime_non_theft',
					'prev_gid_crime_theft',
					'prev_gid_food_fail',
					'prev_gid_food_pass',
					'prev_gid_food_pass_w_conditions',
					'prev_gid_graffitti',
					'prev_gid_sanitation_requests',
					'prev_gid_vacant_gang_false',
					'prev_gid_vacant_gang_true',
					'prev_neigh_lights_ally_homeless_false',
					'prev_neigh_lights_ally_homeless_true',
					'prev_neigh_building_violations',
					'prev_neigh_crime_non_theft',
					'prev_neigh_crime_theft',
					'prev_neigh_food_fail',
					'prev_neigh_food_pass',
					'prev_neigh_food_pass_w_conditions',
					'prev_neigh_graffitti',
					'prev_neigh_sanitation_requests',
					'prev_neigh_vacant_gang_false',
					'prev_neigh_vacant_gang_true',
					'gid_tweets_bad',
					'gid_tweets_good',
					'gid_liquor_licenses',
					'gid_red_light_tickets',
					'neigh_tweets_bad',
					'neigh_tweets_good',
					'neigh_liquor_licenses',
					'neigh_red_light_tickets'
					]]

		y_test = data['test']['gid_crime_theft'].values
		x_test = data['test'][['prev_gid_lights_ally_homeless_false',
					'prev_gid_lights_ally_homeless_true',
					'prev_gid_building_violations',
					'prev_gid_crime_non_theft',
					'prev_gid_crime_theft',
					'prev_gid_food_fail',
					'prev_gid_food_pass',
					'prev_gid_food_pass_w_conditions',
					'prev_gid_graffitti',
					'prev_gid_sanitation_requests',
					'prev_gid_vacant_gang_false',
					'prev_gid_vacant_gang_true',
					'prev_neigh_lights_ally_homeless_false',
					'prev_neigh_lights_ally_homeless_true',
					'prev_neigh_building_violations',
					'prev_neigh_crime_non_theft',
					'prev_neigh_crime_theft',
					'prev_neigh_food_fail',
					'prev_neigh_food_pass',
					'prev_neigh_food_pass_w_conditions',
					'prev_neigh_graffitti',
					'prev_neigh_sanitation_requests',
					'prev_neigh_vacant_gang_false',
					'prev_neigh_vacant_gang_true',
					'gid_tweets_bad',
					'gid_tweets_good',
					'gid_liquor_licenses',
					'gid_red_light_tickets',
					'neigh_tweets_bad',
					'neigh_tweets_good',
					'neigh_liquor_licenses',
					'neigh_red_light_tickets'
					]]
		
		y_train.resize(len(y_train),1)
		y_test.resize(len(y_test),1)
		
		regr = linear_model.LinearRegression()
		regr.fit(x_train, y_train)
		# print regr.summary()
		# print "spatial ols", mse(y_test, regr.predict(x_test))
		print regr.predict(x_test)
		return mse(y_test, regr.predict(x_test))
		# 9888290.8158

	def run_ols(self, dates, shape):
		data = self.get_data(dates, shape)

		y_train = data['train']['gid_crime_theft'].values
		x_train = data['train'][[	'prev_gid_lights_ally_homeless_false',
					'prev_gid_lights_ally_homeless_true',
					'prev_gid_building_violations',
					'prev_gid_crime_non_theft',
					'prev_gid_crime_theft',
					'prev_gid_food_fail',
					'prev_gid_food_pass',
					'prev_gid_food_pass_w_conditions',
					'prev_gid_graffitti',
					'prev_gid_sanitation_requests',
					'prev_gid_vacant_gang_false',
					'prev_gid_vacant_gang_true',
					'gid_tweets_bad',
					'gid_tweets_good',
					'gid_liquor_licenses',
					'gid_red_light_tickets',
					]]

		y_test = data['test']['gid_crime_theft'].values
		x_test = data['test'][['prev_gid_lights_ally_homeless_false',
					'prev_gid_lights_ally_homeless_true',
					'prev_gid_building_violations',
					'prev_gid_crime_non_theft',
					'prev_gid_crime_theft',
					'prev_gid_food_fail',
					'prev_gid_food_pass',
					'prev_gid_food_pass_w_conditions',
					'prev_gid_graffitti',
					'prev_gid_sanitation_requests',
					'prev_gid_vacant_gang_false',
					'prev_gid_vacant_gang_true',
					'gid_tweets_bad',
					'gid_tweets_good',
					'gid_liquor_licenses',
					'gid_red_light_tickets',
					]]
		
		y_train.resize(len(y_train),1)
		# x.resize(len(x),1)
		
		regr = linear_model.LinearRegression()
		regr.fit(x_train, y_train)
		
		# print "ols", mse(y_test, regr.predict(x_test))
		return mse(y_test, regr.predict(x_test))
		# 10987133.1401
		
	def run(self):
		pass
		# print ols.summary

# def reject_outliers(data, m = 2.):
#     d = np.abs(data - np.median(data))
#     mdev = np.median(d)
#     s = d/mdev if mdev else 0.
#     return data[s<m]

if __name__ == '__main__':
	
	c = Crime()
	shapes = [
			# 'congressional_districts',
			# 'neighborhoods',
			'police_beats',
			# 'police_districts',
			# 'state_senate_districts',
			# 'tax_increment_financing_districts',
			# 'ward_precincts',
			# 'wards',
			# 'zip_codes'
			]

	for shape in shapes:
		print "\n"
		print shape

		future_days 	= [14]
		training_days	= [28]
		for future_dt in future_days:
			for training_dt in training_days:
				cv = c.get_cv(future_days=future_dt, training_days=training_dt)
				# print cv
				
				# print "\tpredicting out %s day in future" % future_dt
				# print "\tusing %s of historical data" % training_dt
				t1 = time.time()
				ols_mse = []
				sols_mse = []
				for days in cv:
					# print days
					ols_mse.append(c.run_ols(days, shape))
					sols_mse.append(c.run_spatial_ols(days, shape))
						# print ols_mse
						# print sols_mse
				t2 = time.time()
				# ols_mse = reject_outliers(ols_mse)
				# sols_mse = reject_outliers(sols_mse)
				print ("shape",
					shape, 
					"%s" % future_dt, 
					"%s" % training_dt, 
					"ols", 
					np.average(ols_mse), 
					np.std(ols_mse), 
					"sols", 
					np.average(sols_mse), 
					np.std(sols_mse), 
					round(t2 - t1, 0))




