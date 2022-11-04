"""
Delete all draft deposits for the signed-in user

"""
from genericpath import isfile
import json
import requests
import os
import sys
import codecs

SIZE = 10  # Number of deposits to retrieve from each request
BASE_URL = "https://zenodo.org" # TODO: once you are sure about what you are doing, remove the "sandbox." part
TOKEN = os.getenv('TOKEN')
print(TOKEN)

def main():

    headers = {"Content-Type": "application/json"}
    params = {'access_token': TOKEN}

    # Get list of draft submissions
    url = f"{BASE_URL}/api/deposit/depositions?status=draft&size={SIZE}"

    response = requests.get(url, params=params, json={}, headers=headers)
    print(response.text)
    if response.status_code > 210:
        print("Error happened during submission, status code: " + str(response.status_code))
        return

    for record in response.json():
        id = record['id']
        url = f"{BASE_URL}/api/deposit/depositions/{id}"
        response = requests.delete(url, params=params, json={}, headers=headers)
        if response.status_code > 210:
            print("Error happened during deletion, status code: " + str(response.status_code))
            return

if __name__ == "__main__":

    main()