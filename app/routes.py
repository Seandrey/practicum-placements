# Routes for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051)

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


@app.route('/')
def home():
    return render_template('home/home.html')

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
