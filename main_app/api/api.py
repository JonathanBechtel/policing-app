# -*- coding: utf-8 -*-
"""
Primary file for the API endpoints to deliver model data
"""

from flask import Blueprint, request, jsonify
import pandas as pd

from .extra import str2bool, load_model_pipelines, load_explainers, generate_shap_chart_data

bp = Blueprint('api', __name__, url_prefix='/api')

try:
    stop_search_pipe, stop_arrest_pipe, arrest_pipe_w_outcome, arrest_pipe_no_outcome = load_model_pipelines()
    print("Successfully loaded models")
except Exception as e:
    print(f"Could not load models, because: {e}")

try:
    stop_search_explainer, stop_arrest_explainer, arrest_explainer_w_outcome, arrest_explainer_no_outcome = load_explainers()
    print("Successfully loaded explainers")
except Exception as e:
    print(f"Could not load explainers because: {e}")

@bp.route('/v1/search', methods=['GET'])
def search_prediction():
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
    info_dict['proba'] = float(stop_search_pipe.predict_proba(sample)[0][1])
    info_dict['outcome'] = 'search'
    
    print("Building the SHAP values")
    chart_data = generate_shap_chart_data(sample, stop_search_pipe, stop_search_explainer)
    info_dict['outcome_vals'] = chart_data

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
        try:
            search_reasons = request.args.to_dict(flat=False)['reason_for_search']
        except Exception as e:
            print(e)
            search_reasons = []
        for col in search_cols:
            if col in search_reasons:
                info_dict[col] = True
            else:
                info_dict[col] = False
        try:
            sample = pd.DataFrame(info_dict, index=[0])
        except Exception as e:
            print(e)
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
        info_dict['proba'] = float(stop_arrest_pipe.predict_proba(sample)[0][1])
        
    info_dict['outcome'] = 'arrest'
    
    if str2bool(request.args['searched']):
        if request.args['search_outcome'] == 'known':
            chart_data = generate_shap_chart_data(sample, arrest_pipe_w_outcome,
                                                      arrest_explainer_w_outcome, 
                                                      search_val=True, 
                                                      search_outcome=True)
        else:
            chart_data = generate_shap_chart_data(sample, arrest_pipe_no_outcome, 
                                                      arrest_explainer_no_outcome,
                                                      search_val=True)
    else:
        chart_data = generate_shap_chart_data(sample, stop_arrest_pipe, stop_arrest_explainer)
        
    info_dict['outcome_vals'] = chart_data
   
    return jsonify(info_dict)
            

        