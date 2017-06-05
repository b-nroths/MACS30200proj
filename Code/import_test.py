#!/user/bin/python2.7

#script for importing US Census Tract File
#works specifically for subfolder 'shapefiles' with x number of subfolders for each state
#requires pyshp library http://code.google.com/p/pyshp/ and psycopg2 postgresql library


import psycopg2
import shapefile
import glob

#loop through each record in shapefile
def process_shapes(shape_records):
  for record in shape_records:
    insert_shape(record)

#create the shape in the database
def insert_shape(new_record):
  tract_latln = new_record.record[10:]
  tract_number = new_record.record[2]
  cur.execute("INSERT INTO tracts(lat, lng, tract_number) VALUES(%s, %s, %s) RETURNING id", 
      (float(tract_latln[0]), float(tract_latln[1]), tract_number))
  insert_points(new_record, cur.fetchone()[0]) 

#insert corrisponding boundary points for a given shape relation
def insert_points(new_record, id):
  for point in new_record.shape.points:
    cur.execute("INSERT INTO tract_points(lat, lng, tract_id) VALUES(%s, %s, %s)", 
        (float(point[0]), float(point[1]), id))


#connect to postgres db
try:
  conn = psycopg2.connect(dbname="uchicago", 
                    user="bnroths", 
                    password="pw", 
                    host="host", 
                    port="5432",
                    )
except:
  print "Can't connect to database"

cur = conn.cursor()

#loop through each of the subdirectories, open and process each shapefile
for dir in glob.glob('shapefiles/*'):
  file_str = dir[dir.find("/") + 1:]
  print file_str
  sf = shapefile.Reader(dir + "/" + file_str)
  print sf
  # shape_records  = sf.shapeRecords()
  # process_shapes(shape_records)
  # conn.commit()