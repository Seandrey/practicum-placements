# Routes for app
# Author: David Norris (22690264), Joel Phillips (22967051), Sean Ledesma (22752771), Lara Posel (22972221)

import os
from typing import Any, Optional
import flask
from flask import Flask, Response, redirect, render_template, request, make_response, jsonify, url_for
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
import pdfkit

@app.route('/')
def redirects():
    return redirect(url_for('home'))

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
    #students = studentRep()
    return render_template('library.html', students=[])

@app.route('/reports/student')
@login_required
def reportStudents():
    students = db.session.query(Student.student_number.label('id'), Student.name).all()
    return render_template('reports/student_search.html', students=students)


@app.route('/reports/logs/<int:student_number>')
@login_required
def studentLogs(student_number):
    s: Student = Student.query.filter_by(student_number=student_number).one()
    studentid = s.studentid
    logs = ActivityLog.query.filter_by(studentid=studentid).all()

    #Get Queries   
    units: list[Unit] = Unit.query.order_by(
        Unit.unitid).all()
    locations: list[Location] = Location.query.order_by(
        Location.locationid).all()
    supervisors: list[Supervisor] = Supervisor.query.order_by(
        Supervisor.supervisorid).all()
    domains: list[Domain] = Domain.query.order_by(
        Domain.domainid).all()
    activities: list[Activity] = Activity.query.order_by(
        Activity.activityid).all()

    subst_data = {
        "student_db_id": studentid
    }

    data = {
        "student": s,
        "locations": locations,
        "supervisors": supervisors,
        "domains": domains,
        "units": units,
        "activities": activities
    }

    return render_template('reports/logs.html', logs=logs, subst_data=subst_data, data=data)

@app.route("/reports/submit_edit", methods=['POST'])
@login_required
def submit_edit():
    """Send Post Request to that page, on the client has JSON file. Extracts json file from body"""
    data = request.get_json()

    print(data)
    
    #Update Row with new Data
    new_log: ActivityLog = ActivityLog.query.filter_by(logid=data['logid']).one()
    assert new_log.studentid == data["studentid"], f"DB has edit request for {data['logid']} with student {new_log.studentid}, while request has {data['studentid']}"
    new_log.locationid = data["locationid"]
    new_log.supervisorid = data["supervisorid"]
    new_log.activityid = data["activityid"]
    new_log.domainid =  data["domainid"]
    new_log.minutes_spent = data["minutes_spent"]
    # new_log.record_date = data["record_date"]
    new_log.unitid = data["unitid"]

    service_date_datetime: datetime = 0
    try:
        #service_date_datetime = datetime.strptime(data["record_date"], "%Y-%m-%d")
        # strip weird "Z" character
        processed_date = data["record_date"].replace("Z", "")
        service_date_datetime = datetime.fromisoformat(processed_date)
        service_date_date = service_date_datetime.date()
        new_log.record_date = service_date_date
    except ValueError:
        print(f"failed to parse '{data['record_date']}' to datetime (record date). ignoring any changes")

    session: scoped_session = db.session
    session.commit()

    # TODO: do more stuff
    return jsonify({"success": True})


@app.route('/reports/student/<int:studentid>')
@login_required
def reportStudent(studentid):
    data = get_student_info(studentid)
    return render_template('reports/student.html', data=data)

@app.route('/reports/student/pdf/<int:studentid>')
@login_required
def reportStudentPdf(studentid):
    data = get_student_info(studentid)

    return render_template('reports/student_pdf.jinja', data=data)


@app.route('/reports/staff')
@login_required
def reportStaff():
    return render_template('reports/staff.html')


@app.route('/reports/location')
@login_required
def reportLocationsSearch():
    locations = db.session.query(Location.locationid.label('id'), Location.location).all()
    return render_template('reports/location_search.html', locations=locations)

@app.route('/reports/location/<int:locationid>')
@login_required
def reportLocations(locationid):
    # TODO: also filter based on year/semester if relevant
    data = get_location_info(locationid)

    return render_template('reports/location.html', data=data)

@app.route('/reports/location/pdf/<int:locationid>')
@login_required
def reportLocationPdf(locationid):
    # TODO: also filter based on year/semester if relevant
    data = get_location_info(locationid)

    return render_template('reports/location_pdf.jinja', data=data)


@app.route('/reports/cohort')
@login_required
def reportCohortsSearch():
    #years = db.session.query(func.year(ActivityLog.record_date)).group_by(func.year(ActivityLog.record_date)).all()
    cohorts = db.session.query(ActivityLog.year, ActivityLog.unitid, Unit.unit).join(Unit).group_by(ActivityLog.year, ActivityLog.unitid).all()
    return render_template('reports/cohort_search.html', cohorts=cohorts)

@app.route('/reports/cohort/<int:cohort_unit>/<int:cohort_year>')
@login_required
def reportCohorts(cohort_unit, cohort_year):
    data = get_cohort_info(cohort_unit, cohort_year)
    return render_template('reports/cohort.html', data=data)

@app.route('/reports/cohort/pdf/<int:cohort_unit>/<int:cohort_year>')
@login_required
def reportCohortPdf(cohort_unit, cohort_year):
    data = get_cohort_info(cohort_unit, cohort_year)
    return render_template('reports/cohort_pdf.jinja', data=data)


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

    qualtrics_import.add_known_choices(label_lookup, format)

    qualtrics_import.download_zip(survey_id, api_key, data_centre)

    json_path = "MyQualtricsDownload/Computer Science - Exercise Science Logbook TRIAL - Copy 2.json"
    assert os.path.isfile(json_path), "failed to find downloaded .json"
    json = qualtrics_import.load_json(json_path)
    qualtrics_import.test_parse_json(json, label_lookup, format)

    # remove generated files
    os.remove(json_path)
    os.rmdir("MyQualtricsDownload")

@app.route('/update', methods=['POST'])
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

@app.route('/makepdf', methods=['POST'])
def makePDF():
    if request.method == 'POST':
        html = request.data.decode('utf-8')

        # PDF options
        options = {
            "orientation": "portrait",
            "page-size": "A4",
            "encoding": "UTF-8",
            "enable-local-file-access":""
        }
        css = ['skeleton.css', 'normalize.css', 'style.css', 'reports.css', 'pdf.css']
        css = [os.path.join(app.root_path, 'static\\css\\' + c) for c in css]
        config = pdfkit.configuration(wkhtmltopdf=app.config['WKHTML_EXE'])
        # Build PDF from HTML
        pdf = pdfkit.from_string(html, False, options=options, configuration=config, css=css)
        response=make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename-output.pdf'

        return response
