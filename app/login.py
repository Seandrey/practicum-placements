# Page rendering helpers for account-related pages
# Author: Joel Phillips (22967051)

from typing import Optional
from flask import Flask, redirect, render_template, url_for, flash
from app import app, db
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user, login_user, logout_user

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken, try another')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already in use, try another')

# maybe log in with email or username --------------------------------------

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    rememberMe = BooleanField('remember me?')
    submit = SubmitField('Signup')

def signuprender():
    form = SignupForm()
    if form.validate_on_submit():
        print('<h1>' + str(form.username.data) + ' ' + str(form.email.data) + ' ' + str(form.password.data) + '</h1>')
        newuser = User(email=form.email.data, username=form.username.data)
        newuser.set_password(form.password.data)
        db.session.add(newuser)
        db.session.commit()
        flash('Account created!')
        return redirect(url_for('loginroute'))
    return render_template('login/signup.html',title='Signup', form=form)

def loginrender(next_page: Optional[str] = None):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('loginroute'))
        login_user(user, remember=form.rememberMe.data)

        # redirect to "next page" if specified
        if next_page is None:
            next_page = url_for("home")
        return redirect(next_page)
    return render_template('login/login.html', title='Sign In', form=form)


def logoutredirect():
    logout_user()
    return redirect(url_for('home'))

