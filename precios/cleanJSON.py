import json
import pandas as pd
import numpy as np
import sys
import csv

# {"pml":[1264.34,1229.98,1179.42,1167.83,1174.07,1179.25,1207.85,1263.55,1508.29,1383.1,1473.99,1370.87,1474.64,1416.58,1263.11,1268.5,1275.38,1248.68,1247.32,1313.86,1304.29,1274.89,1221.64,1202.88],"energia":[1231.31,1199.49,1151.09,1140.32,1146.39,1151.12,1178.62,1230.96,1464.01,1340.22,1426.64,1327.7,1426.33,1370.16,1221.57,1226.95,1233.44,1208.42,1207.1,1269.75,1262.2,1235.97,1186.54,1170.79],"perdidas":[33.04,30.49,28.34,27.51,27.68,28.13,29.23,32.59,44.28,42.88,47.35,43.16,48.31,46.43,41.53,41.55,41.94,40.26,40.22,44.11,42.1,38.92,35.1,32.08],"congestion":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}


if len(sys.argv) < 2:
	print("Usage: python cleanJSON.py <result.json>")
	sys.exit()

# The json is an array of calls to the API.
# Each element is one call.
# For each call, an array of 20 nodes is returned
# Each element of this array is a JSON object that represents the reads for the entire week for a single node


with open(sys.argv[1], 'r', encoding='utf-8') as f:
	parsed = json.load(f)


def main():
	result = pd.DataFrame()
	for nodelist in parsed:
		for nodeinfo in nodelist:
			clave = nodeinfo['clv_nodo']
			if len(nodeinfo['Valores']) == 0:
				continue
            # This returns a data frame with all the columns, but fecha is repeated several times.
			df = pd.DataFrame(nodeinfo['Valores'])

			df.rename(columns={'pml_cng': 'congestion', 'pml_ene': 'energia', 'pml_per': 'perdidas'}, inplace=True)
			cols = ['pml', 'congestion', 'energia', 'perdidas']
			try:
                # Split the resulting df by fecha (this produces a list of data frames)
                # One for each fecha
				tt = [v for k, v in df.groupby('fecha')]
			except Exception as e:
				print(nodeinfo)
				print(df)
				print(df.columns)
				raise RuntimeError('Something went wrong')
            # For eac
			for fechadf in tt:
				fechadf.reset_index(drop = True, inplace = True)
                # Convert all the cols in cols to float64 (numeric) types
				fechadf[cols] = fechadf[cols].apply(lambda x: x.astype('float64'))
                # Get the actual date (we get the first since all of the rows contain the same value)
				fecha = fechadf.fecha[0]
				precios = fechadf[cols].to_dict(orient='list')
				precios_str = json.dumps(precios)
				result = result.append(pd.DataFrame({'fecha': [fecha], 'node_id': [clave], 'precios': [precios_str]}), ignore_index = True)
	result.to_csv('outfiledf2.csv', index = False, quoting = csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
	main()
