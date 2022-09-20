# Routes for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051), David Norris (22690264)

from typing import Any, Optional
import flask
from flask import Flask, Response, redirect, render_template, request, jsonify, url_for
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import func
from app import app, db
from datetime import datetime
from app.login import signuprender, loginrender, logoutredirect
from flask_login import login_required, current_user
import json
from datetime import date, timedelta
from app.reports import *

from app.models import Activity, ActivityLog, Domain, Location, Supervisor


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
    return render_template('library.html')


@app.route('/reports/student')
# @login_required
def reportStudents():
    # DEBUG
    teardown_db()
    # this fill db starts at 22000000, for testing navigate to /reports/student/22000000 as we only populate one
    fill_db_multiple_students(1)

    data = get_student_info(22000000)
    return render_template('reports/student.html', data=data)


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
