# -*- coding: utf-8 -*-
"""
routing page for the application
"""

from flask import current_app as app
from flask import render_template, Blueprint

bp = Blueprint('main', __name__)

@bp.route('/about')
def main_page():
    return render_template('base.html', 
                           title='The About Page')

@bp.route('/api')
def dashboard_page():
    return render_template('base.html',
                           title='The API Page')

@bp.route('/faq')
def faq_page():
    return render_template('base.html',
                           title='The FAQ Page')