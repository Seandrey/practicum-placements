# Script for testing qualtrics import functionality
# Author: Joel Phillips (22967051)

from app import qualtrics_import, db

from sqlalchemy.orm.scoping import scoped_session

from app.models import Activity, ActivityLog, Domain


def run_import():
    """Main function to run the imports"""
    # api key, data centre, and survey ID for Joel test survey
    api_key = "3g99BHNjmZBe03puBM8gwx2WqptsJNfiTXyJW3Aa"
    data_centre = "ca1"
    survey_id = "SV_9XIDg01qrekuOWi"
    # can get IDs from here apparently: https://api.qualtrics.com/ZG9jOjg3NjYzNQ-finding-your-qualtrics-i-ds 

    format = qualtrics_import.get_survey_format(survey_id, api_key, data_centre)
    label_lookup = qualtrics_import.get_label_lookup(format)
    print("Label lookup:")
    print(label_lookup)

    qualtrics_import.add_known_choices(label_lookup, format)

    qualtrics_import.download_zip(survey_id, api_key, data_centre)
    # shows weird format of CSV that doesn't seem to match Excel spreadsheet. Need to access their survey to ensure this matches
    # for numbering of looped questions, you get uniform "1 - Age" (or "1_Q12") in CSV if no numbering specifically applied. So presuming this
    # JSON has numbering of "1_QID7" or "1_QID9_TEXT"

    json = qualtrics_import.load_json("MyQualtricsDownload/Computer Science - Exercise Science Logbook TRIAL - Copy 2.json")
    # TODO: delete MyQualtricsDownload folder, including contents
    rows = qualtrics_import.test_parse_json(json, label_lookup, format)
    print(rows)

    db_rows = ActivityLog.query.all()
    for row in db_rows:
        print(row)
    domain_rows = Domain.query.all()
    for row in domain_rows:
        print(row)
    activity_rows = Activity.query.all()
    for row in activity_rows:
        print(row)

if __name__ == "__main__":
    run_import()
