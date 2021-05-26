# -*- coding: utf-8 -*-
"""
Main application file that will run the application
"""

from main_app import init_app

app = init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
