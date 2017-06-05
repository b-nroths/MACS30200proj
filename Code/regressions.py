import numpy as np
from postgres import Postgres
import pandas as pd
from sklearn.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model

class Crime():
	def __init__(self):
		self.p 		= Postgres(False)

	def get_data(self):
		query = """
		SELECT * FROM congressional_districts_data
		"""
		res = self.p.query_list(query)
		d = pd.DataFrame(res, columns=['gid', 'gid_theft', 'gid_not_theft', 'neigh_theft', 'neigh_not_theft'])
		return d

	def plot(self, x, y, y_hat):
		plt.scatter(x, y,  color='black')
		plt.plot(x, y_hat, color='blue', linewidth=3)

		plt.xticks(())
		plt.yticks(())

		plt.show()

	def run_spatial_ols(self):
		data = self.get_data()
		
		y = data['gid_theft'].values
		x = data[['gid_not_theft', 'neigh_not_theft']]
		
		y.resize(len(y),1)
		
		regr = linear_model.LinearRegression()
		regr.fit(x, y)

		print "spatial ols", mse(y, regr.predict(x))
		# 9888290.8158

	def run_ols(self):
		data = self.get_data()
		
		y = data['gid_theft'].values
		x = data['gid_not_theft'].values
		
		y.resize(len(y),1)
		x.resize(len(x),1)
		
		regr = linear_model.LinearRegression()
		regr.fit(x, y)
		
		print "ols", mse(y, regr.predict(x))
		# 10987133.1401
		
	def run(self):
		pass
		# print ols.summary

if __name__ == '__main__':
	
	c = Crime()
	c.run_ols()
	c.run_spatial_ols()




