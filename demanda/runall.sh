for f in result_*.json
do
	python zonemap.py $f "$f.csv"
done