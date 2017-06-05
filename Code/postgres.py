import requests
import psycopg2
import json
from datasets import datasets
import subprocess, sys
import uuid

class Postgres():

	def __init__(self, debug=False):
		self.shapefiles = [
			# 'census_blocks',
			'community_areas',
			'congressional_districts',
			'empowerment_zones',
			'neighborhoods',
			'police_beats',
			'police_districts',
			'state_congressional_districts',
			'state_senate_districts',
			'tax_increment_financing_districts',
			'ward_precincts',
			'wards',
			'zip_codes'
			]
		self.debug = debug
		self.conn = psycopg2.connect(dbname="uchicago", 
										user="bnroths", 
										password=pw, 
										host=host, 
										port="5432",
										)
		self.conn.autocommit = True
		self.cur = self.conn.cursor()

	def list_tables(self):
		query = """
		SELECT tablename FROM pg_catalog.pg_tables WHERE tableowner='bnroths'
		"""
		return self.query_list(query)

	def execute(self, query):
		if self.debug:
			print query
		return self.cur.execute(query)

	def query_list(self, query):
		self.execute(query)
		return self.cur.fetchall()

	def import_shapefile(self, shapefile):
		# for file in self.shapefiles:
		print shapefile
		self.execute("DROP TABLE IF EXISTS shapes.%s" % shapefile)
		cmd = "shp2pgsql shapefiles/%s/sql_statement.dbf shapes.%s | psql -h uchicago.ctluqxmlzcvq.us-east-1.rds.amazonaws.com -d uchicago -U bnroths" % (shapefile, shapefile)
		print cmd
		with open("shapefiles/%s/stdout.txt" % (shapefile),"wb") as out, open("shapefiles/%s/stdout.txt" % (shapefile),"wb") as err:
			subprocess.Popen(cmd, 
				shell=True, 
				stdout=out,
				stderr=err)
		print cmd
		print "\n"


	def delete_from_table(self, dataset_name):
		query = """
		DELETE FROM %s
		""" % dataset_name
		self.execute(query)
		return True

	def insert_neighbor(self, table, gid_1, gid_2):
		self.execute("INSERT INTO shapes.%s_neighbors VALUES (%s, %s)" % (table, gid_1, gid_2))

	def insert_json(self, table, json):
		# exit(0)
		cols = ["%%(%s)s" % x for x in datasets[table]['columns']]
		query = """
		INSERT INTO "datasets"."%s" ("%s") VALUES (%s)
		""" % (table, '","'.join(datasets[table]['columns']), ",".join(cols))
		# exit(0)
		self.cur.executemany(query, json)
		print self.cur.query

	def create_table(self, table):
		query = """
		CREATE TABLE IF NOT EXISTS datasets.%s (
			id varchar(100),
			dt timestamp without time zone,
			lat double precision,
			lng double precision,
			json_data text
		)
		""" % table
		self.cur.execute(query)

	def drop_table(self, table, schema="datasets"):
		query = """
		DROP TABLE IF EXISTS %s.%s 
		""" % (schema, table)
		self.cur.execute(query)

	def get_ids(self, table):
		query = """
		SELECT DISTINCT id
		FROM datasets.%s 
		""" % table
		res = self.query_list(query)
		simp_res = []
		for row in res:
			simp_res.append(row[0])
		return simp_res

	def insert_json_raw(self, table, json_response, check_ids=True):
		# exit(0)
		if check_ids:
			ids_in_table = self.get_ids(table)
		else:
			self.create_table(table)
			self.drop_table(table)
			self.create_table(table)
		for i, row in enumerate(json_response):
			# print i, row
			query = """
			INSERT INTO datasets.%s (id, dt, lat, lng, json_data) VALUES (%%s, %%s, %%s, %%s, %%s)
			""" % table
			# print query
			# exit(0)

			if datasets[table]['columns'][0]:
				row_id = str(row[datasets[table]['columns'][0]])
			else:
				row_id = str(uuid.uuid4())

			# print ids_in_table
			# print type(row_id)
			# exit(0)
			if row_id not in ids_in_table:

				print "insert", row_id
				self.cur.execute(query, (
					row_id, # id
					row[datasets[table]['columns'][1]], # date
					row[datasets[table]['columns'][2]], # lat
					row[datasets[table]['columns'][3]], # lng
					json.dumps(row) # everything
				 ))
			else:
				print "pass", row_id
			# print self.cur.query()

if __name__ == '__main__':
	p = Postgres()
	p.import_shapefiles()