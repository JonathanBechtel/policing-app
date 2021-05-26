# -*- coding: utf-8 -*-
"""
Primary file for the API endpoints to deliver model data
"""

from flask import Blueprint, request, jsonify
import pandas as pd
import pickle
import os

from .extra import str2bool

bp = Blueprint('api', __name__, url_prefix='/api')

folder = os.path.dirname(os.path.abspath(__file__)) + '/models'
stop_search_file  = os.path.join(folder, 'stop_search_pipe.pkl')
stop_arrest_file  = os.path.join(folder, 'stop_arrest_pipe.pkl')
arrest_w_outcome_file = os.path.join(folder, 'arrest_pipe_w_outcome.pkl')
arrest_no_outcome_file = os.path.join(folder, 'arrest_pipe_no_outcome.pkl')

with open(stop_search_file, 'rb') as mod_pipe:
    stop_search_mod = pickle.load(mod_pipe)
    
with open(stop_arrest_file, 'rb') as stop_arrest_pipe:
    stop_arrest_mod = pickle.load(stop_arrest_pipe)
    
with open(arrest_w_outcome_file, 'rb') as external_arrest_pipe1:
    arrest_pipe_w_outcome = pickle.load(external_arrest_pipe1)
    
with open(arrest_no_outcome_file, 'rb') as external_arrest_pipe2:
    arrest_pipe_no_outcome = pickle.load(external_arrest_pipe2)


@bp.route('/v1/search', methods=['GET'])
def search_prediction():
    print(request.args)
    info_dict = dict(
        city = request.args['city'],
        subject_age = int(request.args['subject_age']),
        subject_race = request.args['subject_race'],
        subject_sex = request.args['subject_sex'],
        reason_for_stop = request.args['reason_for_stop'],
        hour = int(request.args['hour']),
        dayofweek = int(request.args['dayofweek']),
        quarter = int(request.args['quarter'])
    )
    
    sample = pd.DataFrame(info_dict, index=[0])
    info_dict['proba'] = float(stop_search_mod.predict_proba(sample)[0][1])
    info_dict['outcome'] = 'search'
   
    
    return jsonify(info_dict)

@bp.route('/v1/arrest', methods=['GET'])
def arrest_prediction():

    search_cols = ['Observation of Suspected Contraband', 'Informant Tip', 'Suspicious Movement', 'Witness Observation', 'Erratic/Suspicious Behavior', 'Other Official Information']
    
    info_dict = dict(
        city = request.args['city'],
        subject_age = int(request.args['subject_age']),
        subject_race = request.args['subject_race'],
        subject_sex = request.args['subject_sex'],
        reason_for_stop = request.args['reason_for_stop'],
        hour = int(request.args['hour']),
        dayofweek = int(request.args['dayofweek']),
        quarter = int(request.args['quarter']))
        
    if str2bool(request.args['searched']):
        search_reasons = request.args.to_dict(flat=False)['reason_for_search']
        info_dict['reason_for_search'] = search_reasons
        for col in search_cols:
            if col in search_reasons:
                info_dict[col] = True
            else:
                info_dict[col] = False
        sample = pd.DataFrame(info_dict, index=[0])
        if request.args['search_outcome'] == 'known':
            sample['contraband_found'] = str2bool(request.args['contraband_found'])
            info_dict['contraband_found'] = str2bool(request.args['contraband_found'])
            sample = sample[['city', 'subject_age', 'subject_race', 'subject_sex',\
                             'contraband_found','reason_for_stop', 'Observation of Suspected Contraband',\
                            'Informant Tip', 'Suspicious Movement', 'Witness Observation',\
                            'Erratic/Suspicious Behavior', 'Other Official Information',\
                            'hour', 'dayofweek', 'quarter']]
            info_dict['proba'] = float(arrest_pipe_w_outcome.predict_proba(sample)[0][1])
        else:
            sample = sample[['city', 'subject_age', 'subject_race', 'subject_sex',\
                             'reason_for_stop', 'Observation of Suspected Contraband',\
                            'Informant Tip', 'Suspicious Movement', 'Witness Observation',\
                            'Erratic/Suspicious Behavior', 'Other Official Information',\
                            'hour', 'dayofweek', 'quarter']]
            info_dict['proba'] = float(arrest_pipe_no_outcome.predict_proba(sample)[0][1])
    else:
        sample = pd.DataFrame(info_dict, index=[0])
        info_dict['proba'] = float(stop_arrest_mod.predict_proba(sample)[0][1])
        
    info_dict['outcome'] = 'arrest'
   
    
    return jsonify(info_dict)

