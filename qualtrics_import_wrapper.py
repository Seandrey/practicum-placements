# Script for testing qualtrics import functionality
# Author: Joel Phillips (22967051)

from app import qualtrics_import


def run_import():
    """Main function to run the imports"""
    # api key, data centre, and survey ID for Joel test survey
    api_key = "3g99BHNjmZBe03puBM8gwx2WqptsJNfiTXyJW3Aa"
    data_centre = "ca1"
    survey_id = "SV_3pXN7wR1BG74Mrs"
    # can get IDs from here apparently: https://api.qualtrics.com/ZG9jOjg3NjYzNQ-finding-your-qualtrics-i-ds 

    format = qualtrics_import.get_survey_format(survey_id, api_key, data_centre)
    label_lookup = qualtrics_import.get_label_lookup(format)
    print("Label lookup:")
    print(label_lookup)

    qualtrics_import.download_zip(survey_id, api_key, data_centre)
    # shows weird format of CSV that doesn't seem to match Excel spreadsheet. Need to access their survey to ensure this matches
    # for numbering of looped questions, you get uniform "1 - Age" (or "1_Q12") in CSV if no numbering specifically applied. So presuming this
    # JSON has numbering of "1_QID7" or "1_QID9_TEXT"

    json = qualtrics_import.load_json("MyQualtricsDownload/Test survey CITS3200.json")
    # TODO: delete MyQualtricsDownload folder, including contents
    rows = qualtrics_import.test_parse_json(json, label_lookup)
    print(rows)

if __name__ == "__main__":
    run_import()