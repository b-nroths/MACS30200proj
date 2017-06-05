import requests
import json
from postgres import Postgres
from datasets import datasets
import pprint
from datetime import datetime

class CreateFinalData():

	def __init__(self):
		self.p = Postgres()

	def create_table(self, dataset_name=None):
		query = """
		CREATE TABLE final_data.{0} AS
		WITH dt_data AS (
			
			SELECT CAST(dt AS DATE), lat, lng, 'alley lights out' AS data_label
			FROM datasets.alley_lights_out_311
			
			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'building_violations' 
			FROM datasets.building_violations

			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'crimes theft=' || CASE WHEN json_data::json->>'primary_type' IN ('THEFT', 'BURGLARY', 'ROBBERY', 'MOTOR VEHICLE THEFT') THEN 'theft' ELSE 'non-theft' END
			FROM datasets.crimes
			
			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'food inspections results=' || CAST(json_data::json->>'results' AS text)
			FROM datasets.food_inspections
			WHERE json_data::json->>'results' IN ('Pass', 'Fail', 'Pass w/ Conditions')
			
			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'graffiti'
			FROM datasets.graffiti_311
			
			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'sanitation requests'
			FROM datasets.sanitation_311
			
			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'vacant gang/homeless=' || COALESCE(json_data::json->>'any_people_using_property_homeless_childen_gangs', 'false')
			FROM datasets.vacant_311

			
			),

		constant_data AS (
			SELECT CAST(dt AS DATE), lat, lng, 'tweets=' || 
						CASE WHEN CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) <= 0.25 THEN 'bad' 
						WHEN CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) >= 0.25 THEN 'good' END AS data_label
			FROM datasets.tweets
			WHERE
				CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) <= 0.25 OR 
				CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) >= 0.25	
				
			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'red light tickets'
			FROM datasets.redlight_tickets
			
			UNION ALL
			
			SELECT CAST(dt AS DATE), lat, lng, 'liquor_licenses'
			FROM datasets.liquor_licenses
		),

		dt_data_w_geo AS (
			
			SELECT gid, dt, data_label, COUNT(*) AS cnt
			FROM dt_data, shapes.{0}
				WHERE 
					st_within (ST_MakePoint(dt_data.lng, dt_data.lat), shapes.{0}.geom)
			GROUP BY 1, 2, 3),
			
		constants_w_geo AS (
			SELECT gid, data_label, COUNT(*) AS cnt
			FROM constant_data, shapes.{0}
				WHERE 
					st_within (ST_MakePoint(constant_data.lng, constant_data.lat), shapes.{0}.geom)
			GROUP BY 1, 2)
			

		SELECT 
			A.dt,
			A.gid,
			COALESCE(MAX(CASE WHEN A.data_label = 'alley gang/homeless=false' THEN A.cnt END), 0)       AS gid_lights_ally_homeless_false,
			COALESCE(MAX(CASE WHEN A.data_label = 'alley gang/homeless=true' THEN A.cnt END), 0)       AS gid_lights_ally_homeless_true,
			COALESCE(MAX(CASE WHEN A.data_label = 'building_violations' THEN A.cnt END), 0)       AS gid_building_violations,
			COALESCE(MAX(CASE WHEN A.data_label = 'crimes theft=non-theft' THEN A.cnt END), 0)       AS gid_crime_non_theft,
			COALESCE(MAX(CASE WHEN A.data_label = 'crimes theft=theft' THEN A.cnt END), 0)       AS gid_crime_theft,
			COALESCE(MAX(CASE WHEN A.data_label = 'food inspections results=Fail' THEN A.cnt END), 0)       AS gid_food_fail,
			COALESCE(MAX(CASE WHEN A.data_label = 'food inspections results=Pass' THEN A.cnt END), 0)       AS gid_food_pass,
			COALESCE(MAX(CASE WHEN A.data_label = 'food inspections results=Pass w/ Conditions' THEN A.cnt END), 0)       AS gid_food_pass_w_conditions,
			COALESCE(MAX(CASE WHEN A.data_label = 'graffiti' THEN A.cnt END), 0)       AS gid_graffitti,
			COALESCE(MAX(CASE WHEN A.data_label = 'sanitation requests' THEN A.cnt END), 0)       AS gid_sanitation_requests,
			COALESCE(MAX(CASE WHEN A.data_label = 'vacant gang/homeless=false' THEN A.cnt END), 0)       AS gid_vacant_gang_false,
			COALESCE(MAX(CASE WHEN A.data_label = 'vacant gang/homeless=true' THEN A.cnt END), 0)       AS gid_vacant_gang_true,
			
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'alley gang/homeless=false' THEN C.cnt END) AS INT), 0)       AS neigh_lights_ally_homeless_false,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'alley gang/homeless=true' THEN C.cnt END) AS INT), 0)       AS neigh_lights_ally_homeless_true,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'building_violations' THEN C.cnt END) AS INT), 0)       AS neigh_building_violations,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'crimes theft=non-theft' THEN C.cnt END) AS INT), 0)       AS neigh_crime_non_theft,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'crimes theft=theft' THEN C.cnt END) AS INT), 0)       AS neigh_crime_theft,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'food inspections results=Fail' THEN C.cnt END) AS INT), 0)       AS neigh_food_fail,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'food inspections results=Pass' THEN C.cnt END) AS INT), 0)       AS neigh_food_pass,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'food inspections results=Pass w/ Conditions' THEN C.cnt END) AS INT), 0)       AS neigh_food_pass_w_conditions,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'graffiti' THEN C.cnt END) AS INT), 0)       AS neigh_graffitti,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'sanitation requests' THEN C.cnt END) AS INT), 0)       AS neigh_sanitation_requests,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'vacant gang/homeless=false' THEN C.cnt END) AS INT), 0)       AS neigh_vacant_gang_false,
			COALESCE(CAST(AVG(CASE WHEN C.data_label = 'vacant gang/homeless=true' THEN C.cnt END) AS INT), 0)       AS neigh_vacant_gang_true,
			
			COALESCE(MAX(CASE WHEN D.data_label = 'tweets=bad' THEN D.cnt END), 0)       AS gid_tweets_bad,
			COALESCE(MAX(CASE WHEN D.data_label = 'tweets=good' THEN D.cnt END), 0)       AS gid_tweets_good,
			COALESCE(MAX(CASE WHEN D.data_label = 'liquor_licenses' THEN D.cnt END), 0)       AS gid_liquor_licenses,
			COALESCE(MAX(CASE WHEN D.data_label = 'red light tickets' THEN D.cnt END), 0)       AS gid_red_light_tickets,
			
			COALESCE(CAST(AVG(CASE WHEN D.data_label = 'tweets=bad' THEN C.cnt END) AS INT), 0)       AS neigh_tweets_bad,
			COALESCE(CAST(AVG(CASE WHEN D.data_label = 'tweets=good' THEN C.cnt END) AS INT), 0)       AS neigh_tweets_good,
			COALESCE(CAST(AVG(CASE WHEN D.data_label = 'liquor_licenses' THEN C.cnt END) AS INT), 0)       AS neigh_liquor_licenses,
			COALESCE(CAST(AVG(CASE WHEN D.data_label = 'red light tickets' THEN C.cnt END) AS INT), 0)       AS neigh_red_light_tickets
		FROM dt_data_w_geo A
			INNER JOIN shapes.{0}_neighbors B ON B.gid_2 = A.gid
			INNER JOIN dt_data_w_geo C ON C.gid = B.gid_1 AND C.dt = A.dt
			LEFT OUTER JOIN constants_w_geo D ON D.gid = A.gid
		GROUP BY 1, 2
		""".format(table)
		# print query
		self.p.execute(query)

if __name__ == '__main__':
	
	c = CreateFinalData()
	tables = ['congressional_districts',
			'neighborhoods',
			'police_beats',
			'police_districts',
			'state_senate_districts',
			'tax_increment_financing_districts',
			'ward_precincts',
			'wards',
			'zip_codes']
	for table in tables:
		print table, datetime.now()
		c.p.drop_table(table, schema='final_data')
		c.create_table(table)
		
