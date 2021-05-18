#!/bin/bash

DATA_FOLDER=./data

python ./fill_template.py $DATA_FOLDER/template.txt $DATA_FOLDER/data.csv

echo Copy the .pdf files to the folder of .json files.
# read -rs $'Press enter to continue...\n'

TOKEN=`cat .carla`
export TOKEN
python ./upload_to_zenodo.py $TOKEN ./$DATA_FOLDER
