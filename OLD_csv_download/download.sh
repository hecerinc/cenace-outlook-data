while read p; do
	arrIN=($p)
	echo "Downloading ${arrIN[0]}.csv"
	curl -o ${arrIN[0]}.csv ${arrIN[1]}
	echo ""
done < $1 
echo -e "\a"
