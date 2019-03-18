import json
import pandas as pd
import numpy as np
import sys
import csv
from concurrent import futures


if len(sys.argv) < 2:
	print("Usage: python cleanJSON.py <result.json>")
	sys.exit()

# The json is an array of calls to the API.
# Each element is one call.
# For each call, an array of 20 nodes is returned
# Each element of this array is a JSON object that represents the reads for the entire week for a single node


with open(sys.argv[1], 'r', encoding='utf-8') as f:
	parsed = json.load(f)


def worker(nodelist):
	# tlen2 = len(nodelist)
	result = [] 
	for nodeinfo in nodelist:
		# print("..{}/{}".format(ind2+1, tlen2))
		clave = nodeinfo['clv_nodo']
		if len(nodeinfo['Valores']) == 0:
			continue
		df = pd.DataFrame(nodeinfo['Valores'])
		df.rename(columns={'pml_cng': 'congestion', 'pml_ene': 'energia', 'pml_per': 'perdidas'}, inplace=True)
		cols = ['pml', 'congestion', 'energia', 'perdidas']
		try:
            # Split into a list of data frames, one per fecha
			tt = [v for k, v in df.groupby('fecha')]
		except Exception as e:
			print(nodeinfo)
			print(df)
			print(df.columns)
			raise RuntimeError('Something went wrong')
		for fechadf in tt:
			fechadf.reset_index(drop = True, inplace = True)
			fechadf[cols] = fechadf[cols].apply(lambda x: x.astype('float64'))
			fecha = fechadf.fecha[0]
			precios = fechadf[cols].to_dict(orient='list')
			precios_str = json.dumps(precios)
			result.append(pd.DataFrame({'fecha': [fecha], 'node_id': [clave], 'precios': [precios_str]}))
	return pd.concat(result, ignore_index = True)


def main():
	# result = pd.DataFrame()
	# tlen = len(parsed)
	# print(tlen)
	intermresult = []
	print(len(parsed))
	index = 0
	with futures.ProcessPoolExecutor() as pool:
		for nodedf in pool.map(worker, parsed):
			# print("Processing {}/{}".format(ind+1, tlen))
			intermresult.append(nodedf)
			index = index + 1
			print(index)
	result = pd.concat(intermresult, ignore_index = True)
	result.to_csv('{}.csv'.format(sys.argv[1]), index = False, quoting = csv.QUOTE_NONNUMERIC, header = False)


if __name__ == '__main__':
	main()

