@SET DATA_FOLDER=./data
python ./fill_template.py $DATA_FOLDER/template.txt $DATA_FOLDER/data.csv

@echo Copy the .pdf files to the folder of .json files.
@pause

@SET TOKEN=YOUR_TOKEN_COMES_HERE
python upload_to_zenodo.py %TOKEN% %DATA_FOLDER%