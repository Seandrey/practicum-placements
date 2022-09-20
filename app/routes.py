# Routes for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051), David Norris (22690264)

from ssl import SSLSession
from typing import Optional
from app.qualtrics_import import MINUTES_SPENT
from flask import Flask, Response, redirect, render_template, request, jsonify, url_for
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import func
from app import app, db
from datetime import datetime
from app.login import signuprender, loginrender, logoutredirect
from flask_login import login_required, current_user
import json
from datetime import date, timedelta
from app.models import User, ActivityLog, Activity, Domain, Location
# from models import Location as Loc
from app.queries import *

#import User, Student, Location , Supervisor, Activity, ActivityLog, Domain

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
@login_required
def reportStudents():
    result = createReport(1, 90) 
    createDomainAct(1)
        
    data = {
    'domains': (
        'Cardiovascular',
        'Musculoskeletal',
        'Metabolic',
        'Mental Health',
        'Cancer',
        'Kidney',
        'Neurological',
        'Respiratory/Pulmonary',
        'Other'
    ), ## list of available domains
    'charts': [
    {
        'title': 'Core Domains',
        'id': 'test1',
        'yMax': '200',
        'style': 'core',
        'domains': (1, 1, 1, 0, 0, 0, 0, 0, 0), ## if the index is one, the domain will be shown
        'hours': [
            ('Referrals, Screening or Assessmnts', (32, 8, 12)), ## three tuple as we are showing three domains
            ('Excercise Prescription', (9, 19, 49)),
            ('Excercise Delivery', (10, 2, 24)),
            ('Other', (13, 28, 9)),
        ]
    },
    {
        'title': 'Additional Domains',
        'id': 'test2',
        'yMax': '70',
        'domains': (0, 0, 0, 1, 1, 1, 1, 1, 1),
        'hours': [
            ('Referrals, Screening or Assessmnts', (3, 8, 12, 6, 6, 12)),
            ('Excercise Prescription', (3, 8, 1, 6, 6, 12)),
            ('Excercise Delivery', (5, 3, 1, 6, 6, 12)),
            ('Other', (3, 8, 12, 5, 3, 1)),
        ]
    }]
    }


    return render_template('reports/student.html', data=data, result=result, location=result['location'], domainAct=result['domainAct'])

@app.route('/reports/staff')
@login_required
def reportStaff():
    return render_template('reports/staff.html')

@app.route('/reports/location')
@login_required
def reportLocations():
    return render_template('reports/location.html')

@app.route('/reports/cohort')
@login_required
def reportCohorts():
    return render_template('reports/cohort.html')

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
