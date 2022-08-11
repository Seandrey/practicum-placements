# Python code to import survey data from Qualtrics
# Author: Joel Phillips (22967051)

import io
import json
import os
import sys
import zipfile
import requests


def download_zip():
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
        "format": "json",
        "seenUnansweredRecode": 2, # converts questions that weren't answered to "2", can't be used for JSON
        "startDate": "2019-04-30T07:31:43Z", # only export after given date, inclusive
        "useLabels": True # shows text shown to user instead of internal numbers
        #"compress": False # can not make it a zip file
    }

    download_req_response = requests.request("POST", url, json=data, headers=headers)
    print(download_req_response.json())

    try:
        progress_id = download_req_response.json()["result"]["progressId"]
    except KeyError:
        print(download_req_response.json())
        sys.exit(2)
    assert progress_id is not None, "progress_id is none!"
    
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

def load_json(filename: str):
    """Loads JSON file to python dictionary"""
    with open(filename) as file:
        data: dict[str, list[dict]] = json.load(file)
        
        # sanity checks
        assert isinstance(data, dict), "json not dict!"
        assert "responses" in data, "no responses in data!"
        assert isinstance(data["responses"], list), "responses not list!"
        assert len(data["responses"]) == 0 or isinstance(data["responses"][0], dict), "individual response not dict!"

        return data

class DummyLogModel:
    """Temporary class to act as model for log book main - has some fields required"""

    def __init__(self, student: str, supervisor: str, location: str, activity: str, domain: str, min_spent: int):
        self.student = student
        self.supervisor = supervisor
        self.location = location
        self.activity = activity
        self.domain = domain
        self.min_spent = min_spent

def test_parse_json(json_file: dict[str, list[dict]]) -> list[DummyLogModel]:
    """Try to parse JSON representation of dict? Assumed format below"""

    rows: list[DummyLogModel] = []

    for response in json_file["responses"]:
        
        """unsure what field names are. Qualtrics docs seem to mention there is an "export mapper" that remaps field names to readable 
        ones. Excel spreadsheet definitely doesn't match the camelCase examples here, so presuming that this has happened. As such,
        trying to use names from there. Or possibly the Excel just uses the 'labels' section? In which case, could just edit 
        json to replace unreadable names with labels ones.
        
        Actually, labels are the data labels, not the question number labels. Question number labels must be something else.""" 

        # I believe these should all have constant question IDs. If not, could allow a "mapping" thing like Sean suggested
        student_name = response["Student Name"]
        service_date = response["Journal Date (date of service)"]
        placement_loc = response["Placement Location"]
        supervisor = response["Primary Supervisor:"] # possibly issue here as seem to be able to do multiple?
        num_logs = response["How many activity logs will you be adding today?\n\nThis is the number of separate logs to a maximum of 10 per shift/day."] # TODO: issue with whitespace?

        # TODO: alternatively, could just start with "1" and keep going if finds more
        for i in range(1, num_logs + 1):
            # would likely have to look these up by label

            # note inconsistent spacing of "- " vs " - "
            category = response[f"{i} - Category"]
            domain = response[f"{i}- Domain"]
            minutes = response[f"{i} - Minutes spent on activity:[eg. 1.5 hours = entered as 90]"]
            
            # make a student record now
            model = DummyLogModel(student_name, supervisor, placement_loc, category, domain, minutes)
            rows.append(model)

    return rows

def get_survey_format():
    """Gets format of survey (question name mapping, etc.). Adapted from https://api.qualtrics.com/ZG9jOjg3NzY3Mw-managing-surveys"""
    # also see some more docs on JSON schema here: https://api.qualtrics.com/73d7e07ec68b2-get-survey

    # set user params
    api_token = os.environ["Q_API_TOKEN"]
    data_centre = os.environ["Q_DATA_CENTER"]

    survey_id = "soemthing"

    base_url = f"https://{data_centre}.qualtrics.com/API/v3/surveys/{survey_id}"
    headers = {"x-api-token": api_token}

    response = requests.get(base_url, headers=headers)
    print(response.text)

    # should have a json form, with "result" field. Under "result", has exportColumnMap
    return response.json()

def get_label_lookup(survey_format_json: dict[str, dict]) -> dict[str, str]:
    """Gets label lookup map from less useful Qualtrics form."""

    bad_map = survey_format_json["result"]["exportColumnMap"]
    
    # now, extract a str-str dictionary from that
    label_lookup: dict[str, str] = {key: value["question"] for (key, value) in bad_map}
    return label_lookup

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
