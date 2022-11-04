#!/bin/bash

DATA_FOLDER=./data

python scripts/create_author_lists.py <xlsx>
python scripts/fill_template.py $DATA_FOLDER/template_update.txt $DATA_FOLDER/data.csv

echo "Copy any extra files to the folder of .json files, then press enter"
read

TOKEN=YOUR_TOKEN_COMES_HERE
python scripts/upload_to_zenodo.py $TOKEN $DATA_FOLDER
