# -*- coding: utf-8 -*-
"""
routing page for the application
"""

from flask import current_app as app
from flask import render_template, Blueprint

bp = Blueprint('main', __name__)

@bp.route('/about')
def main_page():
    return render_template('about.html', 
                           title='Better Understand Problems With Data')

@bp.route('/api')
def dashboard_page():
    return render_template('api.html',
                           title='Connect Directly To Our Model')

@bp.route('/faq')
def faq_page():
    return render_template('faq.html',
                           title='Frequently Asked Questions')