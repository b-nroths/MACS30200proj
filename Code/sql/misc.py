CREATE TABLE congressional_districts_data AS
(
WITH groups AS (
	SELECT 
		--CAST(date AS DATE),
		gid,
		COUNT(CASE WHEN primary_type IN ('THEFT', 'BURGLARY', 'ROBBERY', 'MOTOR VEHICLE THEFT') THEN 1 END) AS thefts,
		COUNT(CASE WHEN primary_type NOT IN ('THEFT', 'BURGLARY', 'ROBBERY', 'MOTOR VEHICLE THEFT') THEN 1 END) AS non_thefts
	FROM crimes, congressional_districts
	WHERE 
		st_within (ST_MakePoint(crimes.longitude, crimes.latitude), congressional_districts.geom)
	GROUP BY 1--, 2
)

SELECT 
	groups.gid AS gid,
	MAX(groups.thefts) AS gid_thefts,
	MAX(groups.non_thefts) AS gid_non_thefts,
	AVG(C.thefts) AS avg_neighbor_thefts,
	AVG(C.non_thefts) AS avg_neighbor_non_thefts
FROM groups 
	INNER JOIN congressional_districts_neighbors B ON B.gid_2 = groups.gid
	INNER JOIN groups C ON C.gid = B.gid_1
GROUP BY 1)