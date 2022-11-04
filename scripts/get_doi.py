"""Extracts DOIs from the metadata files and pastes them into a spreadsheet
"""
import pandas as pd
from typing import List
import sys
import re
from csv import DictWriter
import json
import os

def main(file_path, data_folder):

    columns = ['filename', 'title', 'author_list', 'abstract',
               'keyword_list', 'publication_date', 'series', 'acknowledgements']

    papers = pd.read_excel(file_path, sheet_name='papers', usecols=columns,
                           engine='openpyxl', keep_default_na=False).dropna().set_index('filename')

    df = papers.to_dict(orient='index')

    for filename, record in df.items():
        metadata_path = os.path.join(data_folder, filename + ".json")
        with open(metadata_path, 'r') as json_file:
            metadata = json.load(json_file)['metadata']
            doi = metadata['doi']
        papers.loc[filename, 'doi'] = doi


    with pd.ExcelWriter(file_path, mode='a') as writer:
        papers.to_excel(writer, sheet_name='papers_doi', engine='openpyxl')



if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python get_doi.py tranch.xlsx data_folder")
        exit()

    file_path = sys.argv[1] # e.g. "tranche_1.xlsx"
    data_folder = sys.argv[2]
    if os.path.isfile(file_path) and os.path.isdir(data_folder):
        main(file_path, data_folder)