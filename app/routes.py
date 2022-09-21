# Routes for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051), David Norris (22690264)

import os
from typing import Any, Optional
import flask
from flask import Flask, Response, redirect, render_template, request, jsonify, url_for
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import func
from app import app, db, qualtrics_import
from datetime import datetime
from app.login import signuprender, loginrender, logoutredirect
from flask_login import login_required, current_user
import json
from datetime import date, timedelta
from app.reports import *
from app.models import Activity, ActivityLog, Domain, Location, Supervisor, User
from app.queries import *


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/edit')
@login_required
def edit():
    return render_template('edit.html')


@app.route('/library')
@login_required
def library():
    students = studentRep()
    return render_template('library.html', students=students)

@app.route('/reports/student')
# @login_required
def reportStudents():
    return render_template('reports/student_search.html')


@app.route('/reports/student/<studentid>')
# @login_required
def reportStudent(studentid):
    # DEBUG
    teardown_db()
    # this fill db starts at 22000000, for testing navigate to /reports/student/22000000 as we only populate one
    fill_db_multiple_students(1)

    data = get_student_info(studentid)
    return render_template('reports/student.html', data=data)

@app.route('/reports/staff')
@login_required
def reportStaff():
    return render_template('reports/staff.html')


@app.route('/reports/location')
# @login_required
def reportLocations():
    # DEBUG
    teardown_db()
    # this fill db starts at 22000000, for testing navigate to /reports/student/22000000 as we only populate one
    fill_db_multiple_students(10)

    # hardcoded location for now: whatever "1" is
    location_id = 1
    # TODO: also filter based on year/semester if relevant
    data = get_location_info(location_id)

    return render_template('reports/location.html', data=data)


@app.route('/reports/cohort')
@login_required
def reportCohorts():
    # DEBUG
    teardown_db()
    # this fill db starts at 22000000, for testing navigate to /reports/student/22000000 as we only populate one
    fill_db_multiple_students(10)

    # hardcoded cohort for now: 2022
    year = date.today().year
    data = get_cohort_info(year)
    return render_template('reports/cohort.html', data=data)

# login.py routes


@app.route('/signup', methods=['GET', 'POST'])
def signuproute():
    return signuprender()


@app.route('/login', methods=['GET', 'POST'])
def loginroute():
    # check if url contains next query, and if so, pass it through
    next_page = request.args.get("next")
    return loginrender(next_page)


@app.route('/logout')
def logoutroute():
    return logoutredirect()

def update_db_qualtrics():
    """TODO: move to another .py file. Updates DB from Qualtrics"""
    # api key, data centre, and survey ID for Joel test survey
    api_key = "3g99BHNjmZBe03puBM8gwx2WqptsJNfiTXyJW3Aa"
    data_centre = "ca1"
    survey_id = "SV_9XIDg01qrekuOWi"

    format = qualtrics_import.get_survey_format(survey_id, api_key, data_centre)
    label_lookup = qualtrics_import.get_label_lookup(format)

    qualtrics_import.download_zip(survey_id, api_key, data_centre)

    json_path = "MyQualtricsDownload/Computer Science - Exercise Science Logbook TRIAL - Copy 2.json"
    assert os.path.isfile(json_path), "failed to find downloaded .json"
    json = qualtrics_import.load_json(json_path)
    qualtrics_import.test_parse_json(json, label_lookup, format)

    # remove generated files
    os.remove(json_path)
    os.rmdir("MyQualtricsDownload")

@app.route('/update', methods=['GET', 'POST'])
def updateroute():
    """Temporary route: to manually update DB from Qualtrics. Remove GET later as not idempotent"""
    update_db_qualtrics()

    # DEBUG
    print(ActivityLog.query.all())

    # allow redirection: designed to be used to reload page on AJAX POST
    redirect_to = request.args.get("next")
    if redirect_to is None:
        redirect_to = "home"

    return redirect(url_for(redirect_to))
