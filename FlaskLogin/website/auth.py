from flask import Blueprint, request, flash, redirect, url_for, jsonify
from flask_cors import cross_origin
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'POST':
        fields = request.get_json()
        email = fields['email']
        password = fields['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                
                login_user(user, remember=True)
                return jsonify({
                    'message': 'success'
                }), 200 # do something else here
            else:
                return jsonify({
                    'message': 'failure',
                    'error': 'password_incorrect'
                })
        else:
            return jsonify({
                'message': 'failure',
                'error': 'no_such_email'
            })


@auth.route('/logout')
@cross_origin(supports_credentials=True)
def logout():
    logout_user()
    # replace with response that leads to redirect
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    if request.method == 'POST':
        fields = request.get_json()
        email = fields['email']
        name = fields['name']
        password1 = fields['password']
        password2 = fields['confirm']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return jsonify({
                'message': 'success'
            })
    return jsonify({}) # may add some call to always perform