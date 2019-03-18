# json2CSVForSIN.py
# @desc This is the json2CSV file with a few modifications to account for a few special cases that the SIN zone requires.
#		It also uses a zones3.csv file to map the zone DB ID to the name.

import pandas as pd
import numpy as np
import json

import glob

region = 'BAJA CALIFORNIA'
filelist = glob.glob("*.json")

for filename in filelist[:2]:
	print("Reading {}".format(filename))
	with open(filename, 'r', encoding='utf8') as f:
	    c = f.read()
	parsed = json.loads(c)
	parsed = parsed['Resultados']


	res = pd.DataFrame()
	for zone in parsed:
		if zone['zona_carga'] == "CENTRO SUR":
			continue
		tmp = pd.DataFrame(zone['Valores'])
		tmp['zdc'] = zone['zona_carga']
		res = res.append(tmp, ignore_index = True)


	res['hora'] = res['hora'].astype('int32')
	
	# res['region'] = region

	zones = pd.read_csv('zones3.csv', names=['id','region', 'zdc'], header=None)
	tmp = pd.merge(res, zones, how="left", left_on=['zdc'], right_on=['zdc'])
	tmp = tmp.drop(columns=['zdc'])
	tmp.rename(columns={'id': 'zdc_id', 'demanda_mdo_nodales': 'cdm', 'demanda_pml_zonales': 'cim', 'total_cargas': 'eta'}, inplace=True)
	tmp = tmp[['fecha', 'zdc_id', 'hora', 'cdm', 'cim', 'eta']]

	outname = filename.split(".")
	outname = "{}.csv".format(outname[0])
	tmp.to_csv(outname, index=False, header=False)

