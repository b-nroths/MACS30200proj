SELECT 
	'congressional_districts', 100000 * AVG(ST_Area(geom))
FROM shapes.congressional_districts

UNION ALL

SELECT 
	'neighborhoods', 100000 * AVG(ST_Area(geom))
FROM shapes.neighborhoods

UNION ALL

SELECT 
	'police_beats', 100000 * AVG(ST_Area(geom))
FROM shapes.police_beats

UNION ALL

SELECT 
	'police_districts', 100000 * AVG(ST_Area(geom))
FROM shapes.police_districts

UNION ALL

SELECT 
	'state_senate_districts', 100000 * AVG(ST_Area(geom))
FROM shapes.state_senate_districts

UNION ALL

SELECT 
	'tax_increment_financing_districts', 100000 * AVG(ST_Area(geom))
FROM shapes.tax_increment_financing_districts

UNION ALL

SELECT 
	'wards', 100000 * AVG(ST_Area(geom))
FROM shapes.wards

UNION ALL

SELECT 
	'ward_precincts', 100000 * AVG(ST_Area(geom))
FROM shapes.ward_precincts

UNION ALL

SELECT 
	'zip_codes', 100000 * AVG(ST_Area(geom))
FROM shapes.zip_codes

