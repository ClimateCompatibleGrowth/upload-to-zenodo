import pandas as pd
import re
from csv import DictWriter
import json
import os

columns = ['Name of the Country', 'Author List (draft, to be checked)']

df = pd.read_excel('Starter Kit - List of Countries.xlsx', usecols=columns,
                   engine='openpyxl').dropna()
df = df.rename(columns={'Name of the Country': 'country',
                        'Author List (draft, to be checked)': 'authors'})
lookup = df.set_index('country').to_dict()['authors']

data = pd.read_excel('authors.xlsx', engine='openpyxl',
                     usecols=['firstname', 'lastname', 'orcid', 'institution'], na_filter=False)
data['lookup'] = data['firstname'] + " " + data['lastname']
data = data.set_index('lookup')

regex = r"\[.{1,3}\]"

csv_file_contents = []

for country, author_list in lookup.items():
    try:
        remove_brackets = re.sub(regex, "", author_list).split(",")
        remove_whitespace = [x.strip() for x in remove_brackets]
    except TypeError as ex:
        print(author_list)
        raise ex

    authors = []
    for author in remove_whitespace:
        row = data.loc[author]

        rowdata = {
            "name": row['lastname'] + ", " + row['firstname']
        }
        if row['institution'] != '':

            rowdata["affiliation"] = row['institution']
        if row['orcid'] != '':
            rowdata["orcid"] = row['orcid']

        authors.append(rowdata)

    countryname = country.strip().title()
    contents = {
        'FILENAME': "{}.json".format(countryname),
        'TITLE': "CCG Starter Data Kit: {}".format(countryname),
        'ABSTRACT': "<p>A starter data kit for {}</p>".format(countryname),
        'AUTHORS': json.dumps(authors),
        'KEYWORDS': json.dumps(['energy', 'OSeMOSYS', '#CCG', 'clicSAND',
                                'energy system modelling',
                                'GNUMathProg', 'GLPK', 'linear programming', "{}".format(countryname)])
    }
    csv_file_contents.append(contents)
    with open(os.path.join(data, 'data.csv'), 'w') as csvfile:
        write = DictWriter(csvfile, fieldnames=["FILENAME","TITLE","ABSTRACT","AUTHORS","KEYWORDS"])
        write.writeheader()
        write.writerows(csv_file_contents)
