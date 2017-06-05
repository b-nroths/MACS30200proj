SELECT 
	'alley lights out', 
	MIN(dt), 
	MAX(dt), 
	COUNT(*)
FROM datasets.alley_lights_out_311
GROUP BY 1

UNION ALL

SELECT
	'building_violations',
	MIN(dt), 
	MAX(dt), 
	COUNT(*)
FROM datasets.building_violations
GROUP BY 1

UNION ALL

SELECT
	'crimes theft=' || CASE WHEN json_data::json->>'primary_type' IN ('THEFT', 'BURGLARY', 'ROBBERY', 'MOTOR VEHICLE THEFT') THEN 'theft' ELSE 'non-theft' END,
	MIN(dt), 
	MAX(dt), 
	COUNT(*)
FROM datasets.crimes
GROUP BY 1

UNION ALL

SELECT
	'food inspections results=' || CAST(json_data::json->>'results' AS text),
	MIN(dt), 
	MAX(dt), 
	COUNT(*)
FROM datasets.food_inspections
WHERE
	json_data::json->>'results' IN ('Pass', 'Fail', 'Pass w/ Conditions')
GROUP BY 1

UNION ALL

SELECT
	'graffiti',
	MIN(dt), 
	MAX(dt), 
	COUNT(*)
FROM datasets.graffiti_311
GROUP BY 1

UNION ALL

SELECT
	'liquor_licenses',
	MIN(dt),
	MAX(dt),
	COUNT(*)
FROM datasets.liquor_licenses
GROUP BY 1

UNION ALL

SELECT
	'red light tickets',
	MIN(dt),
	MAX(dt),
	COUNT(*)
FROM datasets.redlight_tickets
GROUP BY 1

UNION ALL

SELECT
	'sanitation requests',
	MIN(dt),
	MAX(dt),
	COUNT(*)
FROM datasets.sanitation_311
GROUP BY 1

UNION ALL

SELECT 
	'vacant gang/homeless=' || COALESCE(json_data::json->>'any_people_using_property_homeless_childen_gangs', 'false'), 
	MIN(dt), 
	MAX(dt), 
	COUNT(*)
FROM datasets.vacant_311
GROUP BY 1
	
UNION ALL

SELECT
	'tweets=' || CASE WHEN CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) <= 0.25 THEN 'bad' WHEN CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) >= 0.25 THEN 'good' END,
	MIN(dt),
	MAX(dt),
	COUNT(*) 
FROM datasets.tweets
	WHERE
		CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) <= 0.25 OR 
		CAST(json_data::json->>'s_score' AS float) * CAST(json_data::json->>'s_magnitude' AS float) >= 0.25	
GROUP BY 1