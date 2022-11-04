from genericpath import isfile
import json
import requests
import os
import sys
import codecs

BASE_URL = "https://zenodo.org" # TODO: once you are sure about what you are doing, remove the "sandbox." part
TOKEN = os.getenv('TOKEN')
print(TOKEN)

def upload(metadata, directory):
    if not _is_valid_json(metadata):
        return

    headers = {"Content-Type": "application/json"}
    params = {'access_token': TOKEN}

    metadata_json = json.loads(metadata)
    if metadata_json['metadata']['prereserve_doi'] == 'true':

        print(f"Creating a new submission for {directory}")
        # Create new submission
        url = "{base_url}/api/deposit/depositions".format(base_url=BASE_URL)

        response = requests.post(url, params=params, json={}, headers=headers)
        #print(response.text)
        if response.status_code > 210:
            print("Error happened during submission, status code: " + str(response.status_code))
            return

        # Get the submission ID
        submission_id = response.json()["id"]

    else:
        submission_id = metadata_json['id']
        print(f"Using existing record {submission_id}")

        url = f"{BASE_URL}/api/deposit/depositions/{submission_id}"
        response = requests.get(url, params=params, json={}, headers=headers)

    bucket_url = response.json()["links"]["bucket"]

    # Add metadata
    url = '{base_url}/api/deposit/depositions/{id}'.format(base_url=BASE_URL, id=submission_id)
    response = requests.put(url,
                            params=params,
                            data=metadata,
                            headers=headers)
    if response.status_code > 210:
        print("Error happened during metadata upload, status code: " + str(response.status_code))
        print(response.json())
        return

    if directory:
        # for csv_file in os.listdir(directory):
        #     filepath = os.path.join(directory, csv_file)
        with open(directory, "rb") as fp:
            response = requests.put(
                                    "%s/%s" % (bucket_url, directory),
                                    data=fp,
                                    params=params,
                                )

    # Upload the file
    if response.status_code > 210:
        print("Error happened during file upload, status code: " + str(response.status_code))
        return

    print(f"{directory} submitted with submission ID = {submission_id} (DOI: 10.5281/zenodo.{submission_id}")
    # The submission needs an additional "Publish" step.
    # This can also be done from a script, but to be on the safe side, it is not included.
    # (The attached file cannot be changed after publication.)
    return submission_id

def batch_upload(directory):
    for metadata_file in os.listdir(directory):
        metadata_file = os.path.join(directory, metadata_file)
        if metadata_file.endswith(".json"):
            filename = metadata_file.replace(".json","")
            print("Uploading %s & %s" % (metadata_file, filename))
            with codecs.open(metadata_file, 'r', 'utf-8') as f:
                metadata = f.read()
                # Re-encoding in order to support UTF-8 inputs
                metadata_json = json.loads(metadata)
                metadata = json.dumps(metadata_json, ensure_ascii=True)
            if os.path.isfile(filename):
                id = upload(metadata, filename)
            else:
                print("The file %s might be a submission metadata file, but %s does not exist." % (metadata_file, filename))
                id = upload(metadata, '')
            if id:
                metadata_json['id'] = id
                metadata_json['metadata']['doi'] = f"10.5281/zenodo.{id}"
                metadata_json['metadata']['prereserve_doi'] = "false"
                with codecs.open(metadata_file, 'w', 'utf-8') as f:
                    f.write(json.dumps(metadata_json, ensure_ascii=True))


def _is_valid_json(text):
    try:
        json.loads(text)
        return True
    except ValueError as e:
        print('Invalid json: %s' % e)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python upload_to_zenodo.py <token> <directory>")
        print("  The directory contains .json metadata descriptors and .pdf files.")
        exit()

    TOKEN = sys.argv[1]
    directory = sys.argv[2]
    if not os.path.isdir(directory):
        print("Invalid directory.")
        exit()

    batch_upload(directory)