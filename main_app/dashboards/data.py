# -*- coding: utf-8 -*-
"""
helper functions to load in the data
"""
import json
import os
import requests

def load_unique_vals():
    folder = os.path.dirname(os.path.abspath(__file__)) + '/data'
    file   = os.path.join(folder, 'unique_vals.json')

    with open(file, 'r') as json_data:
        unique_vals = json.load(json_data)

    return unique_vals

def add_search_inputs(params, search_args):
    if not search_args:
        return params

    if len(search_args) == 1 and type(search_args[0]) == str:
       params['reason_for_search'] = search_args
       return params
    elif len(search_args) == 1 and type(search_args[0]) == list:
       params['reason_for_search'] = search_args[0]
       return params
    elif len(search_args) == 2 and type(search_args[1]) == bool:
       if type(search_args[0]) == str:
           params['reason_for_search'] = [search_args[0]]
           params['contraband_found'] = search_args[1]
           return params
       elif type(search_args[0]) == list:
           params['reason_for_search'] = search_args[0]
           params['contraband_found'] = search_args[1]
           return params
    elif search_args == [None]:
        params['reason_for_search'] = []
        return params

def make_api_call(end_point_type, params):
    if os.environ.get('FLASK_ENV') == 'development':
        username = os.environ['SIGNIN']
        password = os.environ['PASSWORD']
        base_url = 'http://www.police-project-test.xyz/api/v1/'
        api_url  = f'{base_url}{end_point_type}'
        request  = requests.get(api_url, params=params, auth=(username, password))
        return request.json()
    elif os.environ.get('FLASK_ENV') == 'production':
        base_url = 'http://www.policexray.com/api/v1/'
        api_url  = f'{base_url}{end_point_type}'
        request  = requests.get(api_url, params=params)
        return request.json()
