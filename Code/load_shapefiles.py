## this script loads all the shapefiles into postgres


import pysal as ps
import numpy as np
from postgres import Postgres

import matplotlib.pyplot as plt
from pylab import figure, scatter, show, savefig
import shapefile as shp
from datasets import shapefiles

p = Postgres()

for shapefile in shapefiles.keys():
	print shapefile
	### p.import_shapefile(shapefile)
	### p.execute("DROP TABLE IF EXISTS shapes.%s_neighbors" % shapefile)
	### p.execute("""CREATE TABLE shapes.%s_neighbors (
	### 	gid_1 int, gid_2 int
	### )""" % shapefile)
	# try:
	# print shapefile
	shp_path 	= 'shapefiles/%s/sql_statement.shp' % shapefile
	# bds 		= shp.bounds
	dataframe 	= ps.pdio.read_files(shp_path)
	sf 			= shp.Reader(shp_path)
	fig = figure(figsize=(18,18), dpi=225)
	for shape in sf.shapeRecords():
		# print shape.record
		x = [i[0] for i in shape.shape.points[:]]
		y = [i[1] for i in shape.shape.points[:]]
		if shapefiles[shapefile]['name_index']:
			plt.text(sum(x)/len(x), sum(y)/len(y), "%s" % (shape.record[shapefiles[shapefile]['name_index']]))
		plt.plot(x, y)
	# centroids 	= np.array([list(poly.centroid) for poly in dataframe.geometry])

	# plt.plot(centroids[:,0], centroids[:,1],'.')
	wq = ps.queen_from_shapefile(shp_path)
	# print(wq)
	# exit(0)
	# plt.plot(centroids[:,0], centroids[:,1],'.')
	# for k,neighs in wq.neighbors.items():
	# 	origin = centroids[k]
	# 	for neigh in neighs:
	# 		# print k, neigh
	# 		# print shapefile, k+1, neigh+1
	# 		# p.insert_neighbor(shapefile, k+1, neigh+1)
	# 		segment = centroids[[k,neigh]]

	# 		plt.plot(segment[:,0], segment[:,1], '-')
	# exit(0)
	plt.title('%s' % shapefiles[shapefile]['title'], fontsize=50)
	plt.axis('off')
	plt.savefig('images/no/%s.png' % shapefile, bbox_inches='tight', pad_inches = 0)
	# except Exception as e:
	# 	print e
	# 	print "error"