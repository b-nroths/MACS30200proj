datasets = {
	'crimes': {
		'done': True,
		'dataset_name': 'crimes_2001_to_present',
		'columns': ['id', 'date', 'latitude', 'longitude']
	},
	'graffiti_311': {
		'done': True,
		'dataset_name': '311_service_requests_graffiti_removal',
		'columns': ['service_request_number', 'creation_date', 'latitude', 'longitude']
	},
	'vacant_311': {
		'done': True,
		'dataset_name': '311_service_requests_vacant_and_abandoned_building',
		'columns': ['service_request_number', 'date_service_request_was_received', 'latitude', 'longitude']
		# any_people_using_property_homeless_childen_gangs
	},
	'alley_lights_out_311': {
		'done': False,
		'dataset_name': '311_service_requests_alley_lights_out',
		'columns': ['service_request_number', 'creation_date', 'latitude', 'longitude']
	},
	'sanitation_311': {
		'done': True,
		'dataset_name': '311_service_requests_sanitation_code_complaints',
		'columns': [None, 'creation_date', 'latitude', 'longitude']
	},
	'redlight_tickets': {
		'done': True,
		'dataset_name': 'chicago_redlight_tickets_csv',
		'columns': [None, 'issue_time', 'latitude', 'longitude'],
	},
	'food_inspections': {
		'done': True,
		'dataset_name': 'food_inspections',
		'columns': ['inspection_id', 'inspection_date', 'latitude', 'longitude'],
	},
	'liquor_licenses': {
		'done': True,
		'dataset_name': 'business_licenses_current_liquor_and_public_places',
		'columns': ['license_id', 'license_term_start_date', 'latitude', 'longitude'],
	},
	'building_violations': {
		'done': True,
		'dataset_name': 'building_violations',
		'columns': ['id', 'violation_date', 'latitude', 'longitude']
	},
	'tweets': {
		'done': True,
		'dataset_name': 'tweets',
		'columns': ['id', 'created_at', 'lat', 'lng']
	}
}

shapefiles = {
	'congressional_districts': {
		'name_index': 3, #
		'font_size': 12,
		'title': 'Congressional Districts'
		},
	'neighborhoods': {
		'name_index': 1, #
		'font_size': 12,
		'title': 'Neighborhoods'
		},
	'police_beats': {
		'name_index': None,
		'font_size': 12,
		'title': 'Police Beats'
		},
	'police_districts': {
		'name_index': 0, #
		'font_size': 12,
		'title': 'Police Districts'
		},
	'state_senate_districts': {
		'name_index': 0, #
		'font_size': 12,
		'title': 'State Senate Districts'
		},
	'tax_increment_financing_districts': {
		'name_index': None, #
		'font_size': 12,
		'title': 'Tax Increment Financing Districts'
		},
	'ward_precincts': {
		'name_index': None, #
		'font_size': 12,
		'title': 'Ward Precincts'
		},
	'wards': {
		'name_index': 0, #
		'font_size': 12,
		'title': 'Wards'
		},
	'zip_codes': { 
		'name_index': 2, #
		'font_size': 12,
		'title': 'Zip Codes'
		}
}


