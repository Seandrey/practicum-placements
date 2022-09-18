# Routes for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051), David Norris (22690264)

from typing import Optional
from flask import Flask, Response, redirect, render_template, request, jsonify, url_for
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import func
from app import app, db
from datetime import datetime
from app.login import signuprender, loginrender, logoutredirect
from flask_login import login_required, current_user
import json
from datetime import date, timedelta

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
@login_required
def reportStudents():
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
        ),  # list of available domains
        'charts': [
            {
                'title': 'Core Domains',
                'id': 'test1',
                'yMax': '200',
                'style': 'core',
                # if the index is one, the domain will be shown
                'domains': (1, 1, 1, 0, 0, 0, 0, 0, 0),
                'hours': [
                    # three tuple as we are showing three domains
                    ('Referrals, Screening or Assessmnts', (32, 8, 12)),
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

    return render_template('reports/student.html', data=data)


@app.route('/reports/staff')
@login_required
def reportStaff():
    return render_template('reports/staff.html')


def get_domain_col(activity: Optional[str], flist: list):
    """Gets the single AEP domain/activity type table column specified as a partial query"""
    session: scoped_session = db.session

    boilerplate = session.query(
        ActivityLog, Activity).join(Activity).filter(*flist)
    # if no activity, don't include in subquery (assume any activity)
    col_activity_subq = boilerplate.filter(Activity.activity == activity).subquery(
    ) if activity is not None else boilerplate.subquery()
    cols = session.query(Domain.domainid, Domain.domain, (func.coalesce(func.sum(col_activity_subq.c.minutes_spent), 0) / 60.0).label(
        "hours")).join(col_activity_subq, col_activity_subq.c.domainid == Domain.domainid, isouter=True).group_by(Domain.domainid).subquery()

    return cols


def get_domain_table(flist: Optional[list]):
    """Gets AEP domain/activity type table"""
    session: scoped_session = db.session
    if flist is None:
        flist = []

    # find activity-domain table based on hardcoded activity types. due to how group by works, probably have to do this piecewise

    assessments = get_domain_col("Exercise Assessment", flist)
    prescriptions = get_domain_col("Exercise Prescription", flist)
    deliveries = get_domain_col("Exercise Delivery", flist)
    others = get_domain_col("Other", flist)
    total = get_domain_col(None, flist)

    table = session.query(total.c.domain.label("domain"), assessments.c.hours.label("assessment"), prescriptions.c.hours.label("prescription"), deliveries.c.hours.label("delivery"), others.c.hours.label("other"), total.c.hours.label("total")).join(
        assessments, assessments.c.domainid == total.c.domainid).join(prescriptions, prescriptions.c.domainid == total.c.domainid).join(deliveries, deliveries.c.domainid == total.c.domainid).join(others, others.c.domainid == total.c.domainid).all()
    return table


@app.route('/reports/location')
@login_required
def reportLocations():
    # hardcoded location for now: whatever "1" is
    location_id = 1

    # TODO: also filter based on year/semester if relevant

    session: scoped_session = db.session

    # DEBUG find everything in DB with that location
    loc_data = session.query(ActivityLog, Domain, Activity, Supervisor, Location).join(
        Domain).join(Activity).join(Supervisor).join(Location).all()
    print(loc_data)

    # find location name
    loc_name = Location.query.filter_by(locationid=location_id).one().location
    print(loc_name)

    # find hours by supervisor for that location
    loc_hours: list = session.query(Supervisor.name.label("supervisor"), (func.sum(ActivityLog.minutes_spent) / 60.0).label(
        "hours")).join(ActivityLog).filter_by(locationid=location_id).group_by(ActivityLog.supervisorid).all()
    print(loc_hours)

    domains: list[dict] = get_domain_table([ActivityLog.locationid == location_id])

    data = {
        "location": loc_name,
        "date_generated": date.today().isoformat(),
        "loc_hours": loc_hours,
        "domains": domains
    }

    # list of domain names
    domain_names: list[str] = []
    # "hours" data
    domains_hours: dict[str, list[int]] = {
        "Exercise Assessment": [],
        "Exercise Prescription": [],
        "Exercise Delivery": [],
        "Other": []
    }
    # bitset of domains used
    domains_used: list[int] = []
    for domain in domains:
        domain_names.append(domain.domain)
        if domain.total == 0:
            domains_used.append(0)
            continue
        domains_used.append(1)
        domains_hours["Exercise Assessment"].append(domain.assessment)
        domains_hours["Exercise Prescription"].append(domain.prescription)
        domains_hours["Exercise Delivery"].append(domain.delivery)
        domains_hours["Other"].append(domain.other)
    print(domains_hours)

    chart_data = {
        "domains": tuple(domain_names),
        """'domains': (
            'Cardiovascular',
            'Musculoskeletal',
            'Metabolic',
            'Mental Health',
            'Cancer',
            'Kidney',
            'Neurological',
            'Respiratory/Pulmonary',
            'Other'
        ),  # list of available domains"""
        'charts': [
            {
                'title': 'Core Domains',
                'id': 'core_domains_test',
                'yMax': '200',
                'style': 'core',
                # if the index is one, the domain will be shown
                #'domains': (1, 1, 1, 0, 0, 0, 0, 0, 0),
                "domains": tuple(domains_used),
                """'hours': [
                    # three tuple as we are showing three domains
                    ('Referrals, Screening or Assessmnts', (32, 8, 12)),
                    ('Excercise Prescription', (9, 19, 49)),
                    ('Excercise Delivery', (10, 2, 24)),
                    ('Other', (13, 28, 9)),
                ]"""
                "hours": [(key, tuple(value)) for key, value in domains_hours.items()]
            },
            {
                'title': 'Additional Domains',
                'id': 'additional_domains_test',
                'yMax': '70',
                'domains': tuple(domains_used),
                """'hours': [
                    ('Referrals, Screening or Assessmnts', (3, 8, 12, 6, 6, 12)),
                    ('Excercise Prescription', (3, 8, 1, 6, 6, 12)),
                    ('Excercise Delivery', (5, 3, 1, 6, 6, 12)),
                    ('Other', (3, 8, 12, 5, 3, 1)),
                ]"""
                "hours": [(key, tuple(value)) for key, value in domains_hours.items()]
            }
        ]
    }

    return render_template('reports/location.html', data=data, chart_data=chart_data)


@app.route('/reports/cohort')
@login_required
def reportCohorts():
    # hardcoded cohort for now: 2022
    domains = get_domain_table([ActivityLog.record_date.between(
        date.today().replace(month=1, day=1), date.today().replace(month=12, day=31))])

    data = {
        "year": date.today().year,
        "domains": domains
    }

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
