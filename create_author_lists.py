"""
Creates a `data.csv` file

The `data.csv` file contains all of the information needed to populate
the deposition metadata templates

"""
import pandas as pd
from typing import List, Dict
import sys
import re
from csv import DictWriter
import json
import os

def get_authors(contributors: List[int], data: pd.DataFrame) -> List:
    """Extract authors from dataframe

    Arguments
    ---------
    contributors : list
    data : pandas.DataFrame

    Returns
    -------
    list
        A list of authors
    """

    authors = []

    for author in contributors:
        try:
            row = data.loc[int(author)]
        except KeyError:
            print(f"Unable to find author with id {author} in contributors")
            row = None
        except ValueError:
            print(f"Unable to find author with id {author} in contributors")
            row = None

        if row is None:
            raise ValueError(f"No authors found {row}")
        else:
            row_data = {
                "name": row['lastname'] + ", " + row['firstname']
            }
            if row['institution'] != '':
                row_data["affiliation"] = row['institution']
            if row['orcid'] != '':
                row_data["orcid"] = row['orcid']
            authors.append(row_data)

    return authors


def main(file_path: str):
    """

    Arguments
    ---------
    file_path : str
        Path to an Excel file with sheets ``papers``, ``contributors``
    """

    columns = ['filename', 'title', 'author_list', 'abstract',
               'keyword_list', 'publication_date', 'series', 'acknowledgements', 'doi']

    df = pd.read_excel(file_path, sheet_name='papers', usecols=columns,
                    engine='openpyxl', keep_default_na=False).dropna()

    lookup = df.set_index('filename').to_dict(orient='index')

    data = pd.read_excel(file_path, sheet_name='contributors', engine='openpyxl',
                        usecols=['id', 'firstname', 'lastname', 'orcid', 'institution'], na_filter=False)
    data['lookup'] = data['firstname'] + " " + data['lastname']
    data = data.set_index('id')

    csv_file_contents = []

    for filename, value in lookup.items():
        try:
            contributors = value['author_list'].split(",")
        except TypeError as ex:
            raise ex
        except AttributeError:
            contributors = [value['author_list']]

        authors = get_authors(contributors, data)

        titlename = value['title'].strip().replace('\n','')
        abstract = value['abstract'].strip().replace('\n','')
        acknowledgements = value['acknowledgements'].strip().replace('\n', '')

        try:
            keywords = [x.strip() for x in value['keyword_list'].split(",")]
        except AttributeError as err:
            raise AttributeError(err)

        contents = {
            'FILENAME': f"{filename.strip()}.pdf.json",
            'TITLE': f"{titlename}",
            'ABSTRACT': f"{abstract}",
            'AUTHORS': json.dumps(authors),
            'KEYWORDS': json.dumps(keywords),
            'DATE': f"{value.get('publication_date','01-01-2023')}",
            'NOTE': f"{acknowledgements}",
            'DOI': f"{value.get('doi', '')}",
            'ID': value.get('doi', '').replace('10.5281/zenodo.', '')
        }
        csv_file_contents.append(contents)

    return csv_file_contents

def write_out_list(author_list: List[Dict], filepath: str):

    fieldnames = ["FILENAME","TITLE","ABSTRACT","AUTHORS","KEYWORDS",'DATE','NOTE','DOI', 'ID']

    with open(filepath, 'w') as csvfile:
        write = DictWriter(csvfile, fieldnames=fieldnames, lineterminator = "\n")
        write.writeheader()
        write.writerows(author_list)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python create_author_lists.py <deposits.xlsx>")
        exit()

    filename = sys.argv[1] # e.g. "tranche_1.xlsx"
    if os.path.isfile(filename):
        author_list = main(filename)
        write_out_list(author_list, os.path.join('data', 'data.csv'))
