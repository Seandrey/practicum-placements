# Routes for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051), David Norris (22690264)

from typing import Optional
from flask import Flask, Response, redirect, render_template, request, jsonify, url_for
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import func
from app import app
from datetime import datetime
from app.login import signuprender, loginrender, logoutredirect
from flask_login import login_required, current_user
import json
from datetime import date, timedelta

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
    data = [
    {
        'title': 'Testing 1',
        'id': 'test1',
        'yMax': '0',
        'domains': ('Cardiovascular', 'Musculosceletal', 'Metabolic'),
        'hours': [
            ('Referrals, Screening or Assessmnts', (3, 8, 12)),
            ('Excercise Prescription', (9, 9, 9)),
            ('Excercise Delivery', (0, 2, 4)),
            ('Other', (3, 8, 9)),
        ]
    },
    {
        'title': 'Testing 2',
        'id': 'test2',
        'yMax': '200',
        'domains': ('Cardiovascular', 'Musculosceletal', 'Metabolic'),
        'hours': [
            ('Referrals, Screening or Assessmnts', (32, 8, 12)),
            ('Excercise Prescription', (9, 19, 49)),
            ('Excercise Delivery', (10, 2, 24)),
            ('Other', (13, 28, 9)),
        ]
    },
    ]
    return render_template('reports/student.html', data=data)

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
