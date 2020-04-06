"""
WELCOME: ajax business logic - starsight/app/main/views_ajax.py
These are methods that handle AJAX request and don't return a rendered template
AJAX ==> Asyncronous Javascript And XML
"""
from flask import render_template, redirect, flash, url_for, session, request, current_app, jsonify
from flask_security.forms import RegisterForm
from flask_security import login_required, roles_required, current_user, roles_accepted
from flask_mail import Message as FlaskMessage
from slugify import slugify
from datetime import datetime

from ..extensions import db, uploaded_images, mail, moment
from . import star as app

@app.route('/whattimeisit')
def what_time_is_it():
    return jsonify({'timestamp': moment.create(datetime.utcnow()).format('LLLL')})

@app.route('/togglesidebar', methods=['POST'])
def toggle_sidebar():
    if not 'toggled' in session.keys():
        session['toggled'] = True
    else:
        session['toggled'] = not session['toggled']
    return jsonify({'success' : 'toggle now %r' % session['toggled']})
