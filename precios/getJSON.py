from datetime import datetime
from datetime import timedelta
import requests
import sys
import json


if len(sys.argv) < 3:
	print('Usage: python getJSON.py <SISTEMA: BCS | BCA | SIN> <list_of_nodes.txt>')
	sys.exit()

if len(sys.argv[1]) != 3:
	raise ValueError("Sistema must be one of BCA, BCS or SIN")
	sys.exit()


startDate = datetime(2018,6,12)
endDate = datetime(2018,12,31)

# En orden: Sistema, Nodelist (separados por coma), startDate (Y/m/d), endDate (Y/m/d)
url = "https://ws01.cenace.gob.mx:8082/SWPML/SIM/{}/MDA/{}/{}/{}/JSON"

# Read list of nodes
nodefile = sys.argv[2]
with open(nodefile, 'r', encoding='utf-8') as f:
	c = f.read()
	nodelist = c.split('\n')

sistema = sys.argv[1]

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]

# For every set of 20 nodes:
slicedlist = list(chunks(nodelist, 20)) # Max # of nodes that the API will allow you to request per call.

result = []

for chunk in slicedlist:
	# Get the info for the full date range
	x = startDate
	while x <= endDate:
		datestr = x.strftime("%Y/%m/%d")
		delta = x + timedelta(days = 6)
		deltastr = delta.strftime("%Y/%m/%d")
		nodeliststr = ','.join(chunk)
		finalurl = url.format(sistema, nodeliststr, datestr, deltastr)

		req = requests.get(finalurl)
		if req.status_code != 200:
			print('ERR: The request for {} failed'.format(finalurl))

		parsed = req.json()
		result.append(parsed['Resultados'])
		x = delta + timedelta(days=1) # x = x + 7 days

with open('result_{}.json'.format(sistema), 'w', encoding = 'utf-8') as f:
	print(json.dumps(result), file=f)

print('\a')





