import requests
import sys

if len(sys.argv) < 2:
	print("Usage: python titles.py <file_with_urls.txt>")
	sys.exit()



headers = {
	'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"'
}
with open(sys.argv[1], 'r', encoding='utf-8') as f:
	index = 1
	for line in f:
		print("Getting " + line)
		req = requests.get(line.strip(), headers=headers)
		if req.status_code != 200:
			print(req.url)
			print(req.text)
			break
		outfile = open("result_{0:02d}.json".format(index), 'w', encoding='utf-8')
		print(req.text, file=outfile)
		outfile.close()
		index = index + 1
print('\a')

