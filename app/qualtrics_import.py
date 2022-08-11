# Python code to import survey data from Qualtrics
# Author: Joel Phillips (22967051)

import io
import os
import sys
import zipfile
import requests


def get_something():
    """
    Code based on Qualtrics API example: https://api.qualtrics.com/ZG9jOjg3NzY3Nw-new-survey-response-export-guide
    Downloads a CSV file. This is not intended behaviour
    """

    # set user params
    try:
        api_token = os.environ["APIKEY"]
    except KeyError:
        print("set environment variable APIKEY")
        sys.exit(2)
    
    survey_id = "Sv_someweirdhexurlthing"
    data_centre = "co1" # unsure what this is
    # can get IDs from here apparently: https://api.qualtrics.com/ZG9jOjg3NjYzNQ-finding-your-qualtrics-i-ds 

    # set static params
    request_check_progress = 0.0
    progress_status = "inProgress"
    url = f"https://{data_centre}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses/"
    headers = {
        "content-type": "application/json",
        "x-api-token": api_token
    }

    # 1: create data export
    data = {
        "format": "csv",
        "seenUnansweredRecode": 2, # converts questions that weren't answered to "2", can't be used for JSON
        "startDate": "2019-04-30T07:31:43Z",
        "useLabels": True # shows text shown to user instead of internal numbers
    }

    download_req_response = requests.request("POST", url, json=data, headers=headers)
    print(download_req_response.json())

    try:
        progress_id = download_req_response.json()["result"]["progressId"]
    except KeyError:
        print(download_req_response.json())
        sys.exit(2)
    
    isFile = None

    # 2: check on data export progress and wait until export ready
    while progress_status != "complete" and progress_status != "failed" and isFile is None:
        if isFile is None:
            print("file not ready")
        else:
            print("progress_status=", progress_status)
        request_check_url = url + progress_id
        request_check_response = requests.request("GET", request_check_url, headers=headers)
        try:
            isFile = request_check_response.json()["result"]["fileId"]
        except KeyError:
            1 == 1
        print(request_check_response.json())
        request_check_progress = request_check_response.json()["result"]["percentComplete"]
        print("Download is " + str(request_check_progress) + " complete")
        progress_status = request_check_response.json()["result"]["status"]
    
    # check for error
    if progress_status == "failed":
        raise Exception("export failed")

    file_id = request_check_response.json()["result"]["fileId"]

    # 3: download file
    request_download_url = url + file_id + "/file"
    request_download = requests.request("GET", request_download_url, headers=headers, stream=True)

    # 4: unzip file
    zipfile.ZipFile(io.BytesIo(request_download.content)).extractall("MyQualtricsDownload")
    print("complete")

# JSON format (apparently):
"""
{
    "responses": [{
        "responseId": "horrible_hex_number",
        "values": {
            "startDate": "2019-05-02T14:06:49Z",
            "endDate": "2019-05-02T14:06:58Z",
            "status": 0,
            "ipAddress": "24.197.127.176",
            "progress": 100,
            "duration": 9,
            "finished": 1,
            "recordedDate": "2019-05-02T14:06:59.208Z",
            "_recordId": "R_1Cx8FIukucgqM94",
            "locationLatitude": "34.8307952880859375",
            "locationLongitude": "-82.35070037841796875",
            "distributionChannel": "anonymous",
            "userLanguage": "EN", 
            "QID2": 2,
            "QID3": 2
        },
        "labels": {
            "status": "IP Address",
            "finished": "True",
            "QID2": "fair",
            "QID3": "maybe"
        },
        "displayedFields": ["QID1", "QID3", "QID2"],
        "displayedValues: {
            "QID1": [1, 2],
            "QID3": [1, 2, 3],
            "QID2": [1, 2, 3]
        }
    }]
}

"""
