# -*- coding: utf-8 -*-
"""
Main file that initializes the primary app
"""

from flask import Flask

def init_app():
    
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    with app.app_context():
        
        # register blueprints from different sections of the application
        from . import main
        
        app.register_blueprint(main.bp)
        
        from .api import api
        
        app.register_blueprint(api.bp)
        
        # Import Plotly Dashboard
        from .dashboards.main_dash import init_dashboard
        
        app = init_dashboard(app)
        
        return app