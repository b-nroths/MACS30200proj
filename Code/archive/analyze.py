import numpy as np
import pysal
from pysal.spreg.ols import OLS
from postgres import Postgres
import pandas as pd
import pysal as ps
from sklearn.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt

class Crime():
	def __init__(self):
		self.name 	= 'Ben'
		self.p 		= Postgres()

	def get_data(self):
		query = """
		SELECT 
			CAST(date AS DATE),
			COUNT(CASE WHEN primary_type IN ('THEFT', 'BURGLARY', 'ROBBERY', 'MOTOR VEHICLE THEFT') THEN 1 END),
			COUNT(CASE WHEN primary_type NOT IN ('THEFT', 'BURGLARY', 'ROBBERY', 'MOTOR VEHICLE THEFT') THEN 1 END)
		FROM crimes
		GROUP BY 1
		"""
		res = self.p.query_list(query)
		d = pd.DataFrame(res, columns=['date', 'theft', 'not_theft'])
		return d

	def plot(self, x, y, y_hat):
		plt.scatter(x, y,  color='black')
		plt.plot(x, y_hat, color='blue', linewidth=3)

		plt.xticks(())
		plt.yticks(())

		plt.show()

	def run_ols(self):
		data = self.get_data()
		# print data
		y = data['theft'].values
		x = data['not_theft'].values
		y.resize(len(y),1)
		x.resize(len(x),1)
		# print y
		# print y.values, x.shape, x.dtype
		# print x.values, y.shape, y.dtype
		# print type(x)
		# print type(y)
		# # print y, x
		# print y.values
		# print x.values
		m1 = ps.spreg.OLS(y, x, name_x=['not_theft'], name_y='theft')

		print(m1.summary)
		print mse(y, m1.predy.flatten())
		# self.plot(x, y, m1.predy)


	def run(self):
		pass
		# print ols.summary

class Analyze():

	def __init__(self):
		self.name = 'Ben'

	def run_ols(self):
		db = pysal.open(pysal.examples.get_path('columbus.dbf'),'r')
		# print db.head
		hoval = db.by_col("HOVAL")
		print db.header
		y = np.array(hoval)
		y.shape = (len(hoval), 1)

		X = []
		X.append(db.by_col("INC"))
		X.append(db.by_col("CRIME"))
		X = np.array(X).T

		ols = OLS(y, X, name_y='home value', name_x=['income','crime'], name_ds='columbus', white_test=True)

	def run(self):
		pass
		# print ols.summary

if __name__ == '__main__':
	# a = Analyze()
	# a.run_ols()
	c = Crime()
	d = c.get_data()
	c.run_ols()
	# print d




