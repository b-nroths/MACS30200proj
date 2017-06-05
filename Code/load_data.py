import requests
import json
from postgres import Postgres
from datasets import datasets
import pprint

## boundaries
## us, congressional districts
## us, state congressional districts
## census blocks
## zipcodes
## tax increment financing districts
## neighborhoods
## police beats
## census tracts
## police districts
## ward precincts
## state congressional discrits
## community areas, etc

class Download():

	def __init__(self):
		self.name 	= 'Ben'

	def download_data(self, dataset_name=None):
		if dataset_name == 'redlight_tickets':
			url = 'http://plenar.io/v1/api/datadump?obs_date__le=2014-03-02&obs_date__ge=2013-12-02&dataset_name=chicago_redlight_tickets_csv&data_type=json'
		else:
			url = 'http://plenar.io/v1/api/datadump?dataset_name=%s&data_type=json&obs_date__ge=2016-01-01' % datasets[dataset_name]['dataset_name']
		print url
		return requests.get(url).json()

	def transform_json(self, json):
		arr = []
		for row in json:
			arr.append(row['properties'])
		return arr


if __name__ == '__main__':
	p = Postgres()
	d = Download()
	
	for table in datasets.keys():
		# p.delete_from_table(table)
		if not datasets[table]['done']:
			res = d.download_data(table)
			print table
			# print res
			print [str(x) for x in res['features'][0]['properties'].keys()]
			pprint.pprint(res['features'][0]['properties'])
			# exit(0)
			new_json = d.transform_json(res['features'])
			p.insert_json_raw(table, new_json)
