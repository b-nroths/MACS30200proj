import requests
import json
from postgres import Postgres
from datasets import datasets
import pprint
import boto3
import botocore
import os
import uuid

class Download():

	def __init__(self):
		self.s3 	= boto3.resource('s3')
		self.bucket = self.s3.Bucket('bnroths')

	def download_data(self):
		for key in self.bucket.objects.filter(Prefix='twitter'):
			print(key)
			f_name = key.key.split('/')[-1]
			self.s3.Bucket('bnroths').download_file(key.key, 'twitter/tweets/%s.json' % f_name)

	def transform_json(self, json):
		arr = []
		for row in json:
			arr.append(row['properties'])
		return arr


if __name__ == '__main__':
	p = Postgres()
	d = Download()
	# d.download_data()

	table = 'tweets'
	# p.drop_table(table)
	# p.create_table(table)

	for file in os.listdir("twitter/tweets"):
		
		file_name = os.path.join("twitter/tweets", file)
		if 'twitter' in file:
			print file
			with open(file_name) as f:
				print file_name
				for line in f:
					print line
					# exit(0)
					row = json.loads(line)
					query = """
					INSERT INTO datasets.%s (id, dt, lat, lng, json_data) VALUES (%%s, %%s, %%s, %%s, %%s)
					""" % table
					# print query
					# exit(0)

					if 'id' in row:
						row_id = str(row[datasets[table]['columns'][0]])
					else:
						row_id = str(uuid.uuid4())

					ids_in_table = p.get_ids(table)
					if row_id not in ids_in_table:

						print "insert", row_id
						p.cur.execute(query, (
							row_id, # id
							row[datasets[table]['columns'][1]], # date
							row[datasets[table]['columns'][2]], # lat
							row[datasets[table]['columns'][3]], # lng
							json.dumps(row) # everything
						 ))
					else:
						print "pass", row_id