# json2CSV.py
# @desc This file will convert a DEMANDA JSON file into a corresponding CSV file
#	It uses a zones2.csv file which is the database dump for the zones table in the application databsae
#	to merge the zone_id from the actual zone name (which comes in the JSON) to the zone ID (in the database zones table)

import pandas as pd
import numpy as np
import json

import glob

region = 'BAJA CALIFORNIA SUR'
filelist = glob.glob("*.json")

#import sys
#if len(sys.argv) < 3:
#	print("Wrong number of arguments")
#	sys.exit()
# inputname = sys.argv[1]
# outputname = sys.argv[2]

for filename in filelist:

	with open(inputname, 'r', encoding='utf8') as f:
	    c = f.read()
	parsed = json.loads(c)
	parsed = parsed['Resultados']


	res = pd.DataFrame()
	for zone in parsed:
	    tmp = pd.DataFrame(zone['Valores'])
	    tmp['zdc'] = zone['zona_carga']
	    res = res.append(tmp, ignore_index = True)


	res['hora'] = res['hora'].astype('int32')
	res['region'] = region

	zones = pd.read_csv('zones2.csv', names=['id','region', 'zdc'], header=None)
	tmp = pd.merge(res, zones, how="left", left_on=['region', 'zdc'], right_on=['region', 'zdc'])
	tmp = tmp.drop(columns=['zdc','region'])
	tmp.rename(columns={'id': 'zdc_id', 'demanda_mdo_nodales': 'cdm', 'demanda_pml_zonales': 'cim', 'total_cargas': 'eta'}, inplace=True)
	tmp = tmp[['fecha', 'zdc_id', 'hora', 'cdm', 'cim', 'eta']]

	outname = filename.split(".")
	outname = "{}.csv".format(outname[0])
	tmp.to_csv(outname, index=False)

