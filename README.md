# upload-to-zenodo

A simple, stupid, quick and dirty script to batch upload papers to [Zenodo](http://zenodo.org).

## What is Zenodo?
[Zenodo](http://zenodo.org) is a free, open-source research repository, containing papers, but also data sets and software.

## Quick start for CCG

_You don't want to accidentally flood your real Zenodo account with dummy submissions. We don't want that either. That's why by default the script `upload_to_zenodo.py` uses the sandbox of Zenodo. When you are done with experimenting, just replace `sandbox.zenodo.org` with `zenodo.org` in that script._

<a href="https://github.com/darvasd/upload-to-zenodo/blob/master/docs/overview.png" title="Overview"><img src="https://github.com/darvasd/upload-to-zenodo/blob/master/docs/overview.png" width="800" /></a>

1. Get a _Personal access token_ at https://zenodo.org/account/settings/applications/. The `deposit:write` is enough: to be on the safe side, the script does not publish the uploaded papers, the _Publish_ button has to be pushed manually. (Once a document is published on Zenodo, the attached files cannot be modified.)
1. Paste your personal token into a file called `.token` and place in your working directory (or paste into `run.bat` file)
1. Place `Starter Kit - List of Countries.xlsx` in the root folder
1. Place `authors.xlsx` in the root folder
1. Place subfolders of csv files in the `data` folder. Subfolder names should match country names in `Starter Kit - List of Countries.xlsx`
1. You may wish to update certain fields in `data/template.txt` such as publication date. This is used as a template for each of the metadata files generated in the next step.
1. Run `run.sh` (Linux or OSX) or `run.bat` (Windows). This scripts should first create a file `data/data.csv` which contains all of the countries info. Then, individual `<country>.json` Zenodo metadata files are created. Finally, the folders are uploaded to Zenodo.

## Customising the uploads

1. Create a template JSON describing your submissions. Check the [documentation](https://zenodo.org/dev#restapi-rep) (Representations > Deposition metadata) for details about it.
   - Use `{key-name}` for parts that are different for each submission.
   - An example template and some example deposition metadata files can be found in the example folder.
   - The JSON description of any submitted document can be checked by clicking on the JSON link in the Export panel (or by checking the `https://zenodo.org/record/{ID}/export/json` URL.)
1. Create a CSV file that describes the parts that are different for each submission.
   - The `{key-name}` strings of the template will be replaced by the values from the column having `key-name` as header in the CSV file.
   - The CSV file should contain a `FILENAME` column, describing the name of the file created by substituting the values from the given row to the template.
1. Place the CSV datafile and template into the `data` folder.
1. Execute the script `fill_template.py` to generate the descriptors (deposition metadata) for each submission.
	- Usage: `fill_template.py <template_filename> <data_filename>`, where `<template_filename>` is the name (path) of the template file, and `<data_filename>` is the name (path) of the CSV data file.

1. Place subfolders of CSV files into the `data` folder
1. Execute the script `upload_to_zenodo.py` to upload your submissions.
   - Usage: `upload_to_zenodo.py <token> <directory>`, where `<token>` is your personal access token, and `<directory>` is the directory that contains the JSON and PDF files to be uploaded.
1. Go to the [Upload page](https://zenodo.org/deposit), check and publish your submissions.

# Policy Briefs

1. Create a custom policy brief template

## List of policy briefs received

2. Use the Excel sheet to list policy briefs, authors and other metadata.
3. Run `create_author_lists.py` to generate the `data.csv` file.
3. Run `fill_template.py` to fill out the templates to create the JSON metadata files for upload to Zenodo
4. Run `upload_to_zenodo.py` to upload the pdf of the policy briefs to Zenodo (updates JSON with DOI number)
5. Run the `get_doi.py` script to add DOIs to policy briefs in Excel

## New policy briefs received with updated metadata

1. Update the JSON templates using the DOIs listed in the Excel file
4. Upload the pdf of the policy briefs to Zenodo
