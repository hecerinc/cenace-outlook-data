import json
import numpy as np
import pandas as pd

nodos = pd.read_csv('geoNodes.csv')

result = {'type': 'FeatureCollection', 'features': []}

features = []
for index,node in nodos.iterrows():
	props = {
		'clave': node['clave'],
		'estado': node['estado'],
		'localidad': node['localidad'],
		'region': node['region']
	}

	temp = {
		'type': 'Feature', 
		'properties': props, 
		'geometry': {
			'type': 'Point', 
			'coordinates': [node['location.long'], node['location.lat']]
		}
	}
	features.append(temp)

result['features'] = features

with open('result.geojson.json', 'w', encoding='utf8') as f:
	f.write(json.dumps(result))

