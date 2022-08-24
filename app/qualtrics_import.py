# Python code to import survey data from Qualtrics
# Author: Joel Phillips (22967051)

import io
import json
import os
import re
import sys
import zipfile
import requests


def download_zip(survey_id: str, api_token: str, data_centre: str):
    """
    Code based on Qualtrics API example: https://api.qualtrics.com/ZG9jOjg3NzY3Nw-new-survey-response-export-guide
    Downloads a CSV file. This is not intended behaviour
    """

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
        "format": "json", # JSON seems more difficult to use. See if can parse CSV adequately
        #"seenUnansweredRecode": 2, # converts questions that weren't answered to "2", can't be used for JSON
        "startDate": "2019-04-30T07:31:43Z", # only export after given date, inclusive
        #"useLabels": True # shows text shown to user instead of internal numbers. can't use for JSON
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
    zipfile.ZipFile(io.BytesIO(request_download.content)).extractall("MyQualtricsDownload")
    print("complete")

def load_json(filename: str) -> dict[str, list[dict]]:
    """Loads JSON file to python dictionary"""
    with open(filename) as file:
        data: dict[str, list[dict]] = json.load(file)
        
        # sanity checks
        assert isinstance(data, dict), "json not dict!"
        assert "responses" in data, "no responses in data!"
        assert isinstance(data["responses"], list), "responses not list!"
        assert len(data["responses"]) == 0 or isinstance(data["responses"][0], dict), "individual response not dict!"

        return data
    # TODO: delete JSON file

class DummyLogModel:
    """Temporary class to act as model for log book main - has some fields required"""

    def __init__(self, student: str, supervisor: str, location: str, activity: str, domain: str, min_spent: int):
        self.student = student
        self.supervisor = supervisor
        self.location = location
        self.activity = activity
        self.domain = domain
        self.min_spent = min_spent
    
    def __repr__(self) -> str:
        return f"<{self.student}, {self.supervisor}, {self.location}, {self.activity}, {self.domain}, {self.min_spent}>"

class LabelLookup:
    """Class to lookup labels in more intelligent way"""

    def __init__(self, dict: dict[str, str]):
        """TODO: make this generate from scratch eventually"""
        self.dict = dict

    def __repr__(self) -> str:
        return repr(self.dict)
    
    def __getitem__(self, key: str) -> str:
        """Overload [] operator for accesses"""
        return self.dict[key]
    
    def get_text(self, key: str) -> str:
        """Based on JSON having '_TEXT' suffix for text"""
        return f'{self[key]}_TEXT'

def get_answer_label(json_response: dict[str, dict[str, str]], key: str) -> str:
    """Gets answer label for given question name key"""
    print("DEBUG: looking up in labels: ", key)
    return json_response["labels"][key]

def lookup_embedded_text(response_val: dict[str, str], label_lookup: LabelLookup, label_name: str) -> str:
    """Lookup text embedded in JSON (with _TEXT suffix)"""
    return response_val[label_lookup.get_text(label_name)]

def test_parse_json(json_file: dict[str, list[dict]], label_lookup: LabelLookup) -> list[DummyLogModel]:
    """Try to parse JSON representation of dict? Assumed format below"""

    rows: list[DummyLogModel] = []

    for response in json_file["responses"]:
        response_val = response["values"]
        
        """unsure what field names are. Qualtrics docs seem to mention there is an "export mapper" that remaps field names to readable 
        ones. Excel spreadsheet definitely doesn't match the camelCase examples here, so presuming that this has happened. As such,
        trying to use names from there. Or possibly the Excel just uses the 'labels' section? In which case, could just edit 
        json to replace unreadable names with labels ones.
        
        Actually, labels are the data labels, not the question number labels. Question number labels must be something else.""" 

        # I believe these should all have constant question IDs. If not, could allow a "mapping" thing like Sean suggested
        student_name = lookup_embedded_text(response_val, label_lookup, "Student Name")
        service_date = lookup_embedded_text(response_val, label_lookup, "Journal Date (date of service)")
        placement_loc = get_answer_label(response, label_lookup["Placement Location"])
        supervisor = get_answer_label(response, label_lookup["Primary Supervisor:"]) # possibly issue here as seem to be able to do multiple?
        num_logs = lookup_embedded_text(response_val, label_lookup, "How many activity logs will you be adding today?\n\nThis is the number of separate logs to a maximum of 10 per shift/day.") # TODO: issue with whitespace?

        # TODO: alternatively, could just start with "1" and keep going if finds more
        for i in range(1, num_logs + 1):
            # would likely have to look these up by label

            # note inconsistent spacing of "- " vs " - "
            category = get_answer_label(response, f"{i}_{label_lookup['Category']}")
            domain = get_answer_label(response, f"{i}_{label_lookup['Domain']}")
            minutes = response_val[f"{i}_{label_lookup.get_text('Minutes spent on activity:[eg. 1.5 hours = entered as 90]')}"]
            
            # make a student record now
            model = DummyLogModel(student_name, supervisor, placement_loc, category, domain, minutes)
            rows.append(model)

    return rows

def get_survey_format(survey_id: str, api_token: str, data_centre: str) -> dict[str, dict]:
    """Gets format of survey (question name mapping, etc.). Adapted from https://api.qualtrics.com/ZG9jOjg3NzY3Mw-managing-surveys"""
    # also see some more docs on JSON schema here: https://api.qualtrics.com/73d7e07ec68b2-get-survey

    base_url = f"https://{data_centre}.qualtrics.com/API/v3/surveys/{survey_id}"
    headers = {"x-api-token": api_token}

    response = requests.get(base_url, headers=headers)
    print("DEBUG: response start---")
    print(response.text)
    print("DEBUG: response end---")

    # should have a json form, with "result" field. Under "result", has exportColumnMap
    return response.json()

def get_label_lookup_old(survey_format_json: dict[str, dict]) -> dict[str, str]:
    """Gets label lookup map from less useful Qualtrics form.
    NOTE: this implementation abandoned. exportColumnMap seems to have less useful data than I thought - 
    does not have textual column description. Instead trying another way"""

    bad_map = survey_format_json["result"]["exportColumnMap"]

    print("DEBUG: export column map---")
    print(bad_map)
    print("DEBUG: end export column map---")

    print(type(bad_map["Q1"]))
    print(type(bad_map["Q1"]["question"]))
    
    # now, extract a str-str dictionary from that
    label_lookup: dict[str, str] = {key: value["question"] for (key, value) in bad_map.items()}
    return label_lookup

def get_label_lookup(survey_format_json: dict[str, dict]) -> LabelLookup:
    """Gets label lookup map in form: {"Student Name": "QID1"}"""
    questions_map = survey_format_json["result"]["questions"]

    print("DEBUG: export questions map---")
    print(questions_map)
    print("DEBUG: end questions column map---")

    # now, extract a str-str dictionary from that
    label_lookup: dict[str, str] = {value["questionText"]: key for (key, value) in questions_map.items()}

    # FIXME: why are HTML things in there in the first place?
    label_lookup = {re.sub("<div>|</div>|<br>", "", key): value for (key, value) in label_lookup.items()}

    return LabelLookup(label_lookup)


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
