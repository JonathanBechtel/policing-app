
"""
Helper functions for API page
"""
import os
import pickle
import json

def str2bool(val):
    return val.lower() == 'true'

def load_reason_for_stop():
    folder = os.path.dirname(os.path.abspath(__file__))
    file   = os.path.join(folder, 'unique_vals.json')

    with open(file, 'r') as json_data:
        unique_vals = json.load(json_data)

    return unique_vals['reason_for_stop']

def assign_stop_value_to_alias(value_list: list, list_of_reason_dicts: list) -> str:
    print(f"List of reasons: {list_of_reason_dicts}")
    reason_vals = [reason['value'] for reason in list_of_reason_dicts]
    for idx, value in enumerate(value_list):
        if value in reason_vals:
            print(value)
            for reason in list_of_reason_dicts:
                if reason['value'] == value:
                    value_list[idx] = reason['label']
            break
    return value_list


def load_model_pipelines():
    folder = os.path.dirname(os.path.abspath(__file__)) + '/models/pipelines'
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

    return stop_search_mod, stop_arrest_mod, arrest_pipe_w_outcome, arrest_pipe_no_outcome

def load_explainers():
    folder = os.path.dirname(os.path.abspath(__file__)) + '/models/explainers'

    stop_search_file  = os.path.join(folder, 'explainer_stop_search.pkl')
    stop_arrest_file  = os.path.join(folder, 'explainer_stop_arrest.pkl')
    arrest_w_outcome_file = os.path.join(folder, 'explainer_arrest_w_outcome.pkl')
    arrest_no_outcome_file = os.path.join(folder, 'explainer_arrest_no_outcome.pkl')

    with open(stop_search_file, 'rb') as search_explainer:
        stop_search_explainer = pickle.load(search_explainer)

    with open(stop_arrest_file, 'rb') as arrest_explainer:
        stop_arrest_explainer = pickle.load(arrest_explainer)

    with open(arrest_w_outcome_file, 'rb') as external_arrest_explainer1:
        arrest_explainer_w_outcome = pickle.load(external_arrest_explainer1)

    with open(arrest_no_outcome_file, 'rb') as external_arrest_explainer2:
        arrest_explainer_no_outcome = pickle.load(external_arrest_explainer2)

    return stop_search_explainer, stop_arrest_explainer, arrest_explainer_w_outcome, arrest_explainer_no_outcome

def generate_shap_chart_data(sample, pipeline, explainer, search_val=False, search_outcome=False):

    day_mapping = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
    }

    reasons_for_stop = load_reason_for_stop()

    search_cols = ['Observation of Suspected Contraband', 'Informant Tip', 'Suspicious Movement',\
                    'Witness Observation', 'Erratic/Suspicious Behavior', 'Other Official Information']

    vals             = sample.to_dict('records')[0]
    transformed_vals = pipeline[-2].transform(sample)
    print(f"Transformed vals: {transformed_vals.values}")
    print(transformed_vals.info())
    print(transformed_vals.shape)
    print(transformed_vals.columns.tolist())
    print(explainer.data[0])
    shap_values      = explainer(transformed_vals)
    chart_vals       = {col: shap_val for col, shap_val in zip(transformed_vals.columns, shap_values.values[0])}
    sex_val          = sum(value for key, value in chart_vals.items() if 'sex' in key)
    race_val         = sum(value for key, value in chart_vals.items() if 'race' in key)
    keys_to_drop     = [key for key in chart_vals.keys() if 'race' in key or 'sex' in key]

    for key in keys_to_drop:
        del chart_vals[key]

    chart_vals['subject_race'] = race_val
    chart_vals['subject_sex']  = sex_val

    sample['dayofweek'] = day_mapping[sample['dayofweek'].values[0]]
    new_sample = sample.append(chart_vals, ignore_index=True)

    if search_val:
        cols_to_drop      = []
        false_search_vals = 0
        num_false_cols    = 0
        for col in search_cols:
            # if the number is one
            if vals[col]:
                new_sample.rename({col: f'Reason for Search: {col}'}, axis=1, inplace=True)
            else:
                false_search_vals += chart_vals[col]
                num_false_cols    += 1
                cols_to_drop.append(col)
        new_sample.drop(cols_to_drop, axis=1, inplace=True)
        new_sample['Omitted Search Reasons'] = false_search_vals

    if not search_val and not search_outcome:
        new_sample.columns = ['City', 'Age', 'Race', 'Sex', 'Reason For Stop', 'Hour', 'Day', 'Quarter']

    if search_val:
        search_cols = [col for col in new_sample.columns if 'Search' in col and col != 'Omitted Search Reasons']
        if not search_outcome:
            new_sample.columns = ['City', 'Age', 'Race', 'Sex', 'Reason For Stop'] + search_cols + ['Hour', 'Day', 'Quarter', 'Omitted Search Reasons']
        else:
            new_sample.columns = ['City', 'Age', 'Race', 'Sex', 'Contraband Found', 'Reason For Stop'] + search_cols + ['Hour', 'Day', 'Quarter', 'Omitted Search Reasons']

    col_vals = new_sample.values[0].tolist()
    col_vals = assign_stop_value_to_alias(col_vals, reasons_for_stop)
    col_vals = [val.title() if type(val) == str else int(val) for val in col_vals]

    # done to replace the reason for stop with its alias


    new_sample.columns = [f"{col}: {value}" if  col not in search_cols and col != 'Omitted Search Reasons'
                          else col for col, value in zip(new_sample.columns, col_vals)]
    if search_outcome:
        contraband_col  = new_sample.columns.values[4]
        first_col_part  = contraband_col[:-1]
        second_col_part = str(bool(int(contraband_col[-1])))
        contraband_col  = first_col_part + second_col_part
        new_sample.columns.values[4] = contraband_col
    new_sample = new_sample.T
    del new_sample[0]
    new_sample.sort_values(by=1, inplace=True)
    new_sample['Positive']  = new_sample[1] > 0
    new_sample['Positive']  = new_sample['Positive'].astype(int)
    chart_data = new_sample[1].to_dict()
    chart_data['base_value'] = shap_values.base_values[0]
    return chart_data