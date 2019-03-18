# Instructions for downloading PRECIOS

There are two files for downloading PRECIOS:

1. `getJSON.py`: This file takes in a node list and the corresponding sistema (the nodes belong to) and generates and downloads the information for a given date range for all the nodes in the API. This script will split the range in 6 day increments and the node list into 20 nodes (these are the limits imposed by the API) and generate a request for each such 20-node, 6-day chunk. The result is a JSON file with a list of JSON objects, each containing 6 day's worth of information for 20 nodes, called `result_${SISTEMA}.json`.
2. `cleanJSON.py`: This file does the actual processing to convert the JSON file into a CSV we can upload to the SQL database. Outputs `outfiledf2.csv`


## Running the files

0. Get the nodes you want to retrieve. Use the node list at CENACE to find out which nodes you're interested in and save it to some file `nodes.in`.

The **list of nodes** should be a file with a single node ID per line. Pass it through `dos2unix` before running `getJSON.py`.

1. Modify the date range.

In `getJSON.py` lines 17 and 18 are the `startDate` and `endDate` that the script will retrieve. Modify accordingly.

2. Run `getJSON.py` to get the data.

```bash
> python3 getJSON.py [BCS | BCA | SIN] <list_of_nodes.txt>
```

This produces `result_${SISTEMA}.json`. An example of the list of nodes is in `bcs.in`


3. Clean the JSON (transform to CSV)

Depending on how much data you've got, you might want to rent a cloud server with some 8 CPUs and at least 16 GBs RAM.

Once you've got it, you can run `cleanJSON.py`:

```bash
> python3 cleanJSON.py <name_of_input_file.json>
```

This will produce an output file called `name_of_input_file.json.csv`.


## Format for CSV

The CSV follows the following format:

```
fecha,node_id,precios
```


- `fecha`: is some date value in the `%Y-%m-%d` format. (Ex. `2018-08-27`)
- `node_id`: is the `node_id` as defined by the CENACE. (Ex. `07COE-115`)
- `precios`: is a JSON string of the format:

```
{ 
	"pml": int[],
	"congestion": int[],
	"perdidas": int[],
	"energia": int[]
}
```

The `cleanJSON.py` file is the one that performs this conversion. However, it will try to do it all at once, so this process could potentially take a **very long time** depending on how much data is to be processed.

## Concurrent version

Because of the amount of data that comes with the precios db, I decided to make a concurrent version of `cleanJSON.py` which lives in the `concurrent/cleanJSON.py`. 

This is a small modification of the file which allows the use of all the CPUs that the computer has (automatically through Python's `futures` package).

This significantly improves the processing time.

