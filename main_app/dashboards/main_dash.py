# -*- coding: utf-8 -*-
"""
Page for Plotly Dashboard
"""

import dash
import dash_html_components as html
from .html_layout import html_layout
import dash_core_components as dcc
from dash.dependencies import Input, Output, ALL
from .data import load_unique_vals, add_search_inputs
import json
import requests
import dash_bootstrap_components as dbc



def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server = server,
        routes_pathname_prefix = '/home/',
        external_stylesheets = [
            dbc.themes.JOURNAL,
        ]
    )

    dash_app.index_string = html_layout
    unique_vals = load_unique_vals()
    register_callbacks(dash_app)
    
    
    card_content = [
                dbc.CardHeader("Enter Your Information Here"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Your Scenario", html_for="scenario-radio"),
                            dbc.RadioItems(
                                id='scenario-radio',
                                options=[
                                    {'label': 'You\'re pulled over', 'value': 'You are pulled over'},
                                    {'label': 'You\'re being searched', 'value': 'You have been searched'},
                                    {'label': 'Your search has been completed', 'value': 'Your search has been completed'}
                                    ],
                                value='You are pulled over',
                                 labelStyle = {'display': 'block'},
                                 style={}
                                )]
                            ),
                        dbc.Col([
                            dbc.Label("Outcome To Analyze", html_for="outcome-radio"),
                            dbc.RadioItems(
                                id='outcome-radio',
                                labelStyle = {'display': 'block'})
                            ])
                        ]),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Your Race", html_for="race-dropdown"),
                            dcc.Dropdown(
                                id = 'race-dropdown',
                                options = [
                                    {'label': i, 'value': i} for i in unique_vals['subject_race']
                                ],
                                clearable = False,
                                value='white'),
                            ]),
                        dbc.Col([
                            dbc.Label("Your Gender", html_for="sex-dropdown"),
                            dcc.Dropdown(
                                id='sex-dropdown',
                                options=[
                                    {'label': i, 'value': i} for i in unique_vals['subject_sex']    
                                ],
                                clearable=False,
                                value='female')
                            ]),
                        dbc.Col([
                            dbc.Label("Your Age", html_for="age-input"),
                            html.Br(),
                            dbc.Input(
                                id='age-input',
                                type='number',
                                min=12, max=100, step=1, value=40,
                                required=True
                                ),
                            ]),
                        ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Hour", html_for="hour-input"),
                        html.Br(),
                        dbc.Input(
                           id='hour-input',
                           type='number',
                           min=0, max=24, step=1, value=12,
                           required=True)
                        ]),
                    dbc.Col([
                        dbc.Label("Day", html_for="day-dropdown"),
                        dcc.Dropdown(
                            id='day-dropdown',
                            options = [
                                {'label': 'Monday', 'value': 0},
                                {'label': 'Tuesday', 'value': 1},
                                {'label': 'Wednesday', 'value': 2},
                                {'label': 'Thursday', 'value': 3},
                                {'label': 'Friday', 'value': 4},
                                {'label': 'Saturday', 'value': 5},
                                {'label': 'Sunday', 'value': 6}
                                ],
                            value=0,
                            clearable=False
                        )
                        ]),
                    dbc.Col([
                        dbc.Label("Season", html_for="season-input"),
                        dcc.Dropdown(
                            id='season-input',
                            options = [
                                {'label': 'Summer', 'value': 3},
                                {'label': 'Spring', 'value': 2},
                                {'label': 'Winter', 'value': 1},
                                {'label': 'Fall', 'value': 4}
                                ],
                            value=2,
                            clearable=False)
                        ])
                    ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("City", html_for="city-dropdown"),
                        dcc.Dropdown(
                            id='city-dropdown',
                            options=[
                            {'label': i, 'value': i} for i in unique_vals['city']
                            ],
                            clearable = False,
                            value='Charlotte')
                        ], width=4),
                    dbc.Col([
                        dbc.Label("Reason For Stop", html_for="reason-dropdown"),
                        dcc.Dropdown(
                            id='reason-dropdown',
                            options = [
                                {'label': i, 'value': i } for i in unique_vals['reason_for_stop']
                                ],
                            value='Safe Movement Violation',
                            clearable=False)
                            ], width=8)
                        ]),
                html.Hr(),
                dbc.Row(id = 'search-row'),
                    ])
                ]
    
    # Create Dash Layout
    dash_app.layout = html.Div(id='main-div', children=[
        dbc.Container([
            html.Br(),
            html.Br(),
            ### Begin Row With Card of Information On It
            dbc.Row([
                dbc.Col([dbc.Card(id='input-card', children=card_content)
                         ], width=4),
                dbc.Col([
                    html.Div(id='output-div')
                    ], width=8)
            ]),
            html.Hr()
            ]),
        ])

    return dash_app.server


def register_callbacks(app):
    @app.callback(
        Output('output-div', 'children'),
        [Input('scenario-radio', 'value'),
         Input('city-dropdown', 'value'),
         Input('race-dropdown', 'value'),
         Input('sex-dropdown', 'value'),
         Input('reason-dropdown', 'value'),
         Input('age-input', 'value'),
         Input('hour-input', 'value'),
         Input('season-input', 'value'),
         Input('day-dropdown', 'value'),
         Input('outcome-radio', 'value'),
         Input({'type': 'input', 'index': ALL}, 'value')])
    def dump_data(*args):
        params = {
            'city': args[1],
            'subject_age':  args[5],
            'subject_race': args[2],
            'subject_sex': args[3],
            'reason_for_stop': args[4],
            'hour': args[6],
            'dayofweek': args[8],
            'quarter': args[7],
            }
        
        if args[0] in 'You have been searched':
            params['search_outcome'] = 'unknown'
            params['searched'] = True
        elif args[0] == 'Your search has been completed':
            params['search_outcome'] = 'known'
            params['searched'] = True
        elif args[0] == 'You are pulled over':
            params['search_outcome'] = 'unknown'
            params['searched'] = False
        
        params = add_search_inputs(params, args[10])
        
        try:
            request = requests.get(url=f"http://localhost:5000/api/v1/{args[9]}", params=params).json()
            return html.H1(f"Chance of {args[9]}: {request['proba']:.2%}")
        except Exception as e:
            print(e)
            return json.dumps(args)
        
    @app.callback(Output('search-row', 'children'),
                  Input('scenario-radio', 'value'))
    def display_search_row(scenario_val):
        unique_vals = load_unique_vals()
        if scenario_val == 'You are pulled over':
            return []
        elif scenario_val == 'You have been searched':
            return dbc.Col([
                        dbc.Label("Reason For Search", html_for={'type': 'input', 'index': 0}),
                        dcc.Dropdown(
                            id={'type': 'input',
                                'index': 0},
                            options=[
                            {'label': i, 'value': i} for i in unique_vals['reason_for_search']
                            ],
                            clearable = False,
                            multi = True,
                            value='Erratic/Suspicious Behavior')
                        ])
        
        elif scenario_val == 'Your search has been completed':
            return [
                    dbc.Col([
                        dbc.Label("Reason For Search", html_for={'type': 'input', 'index': 0}),
                        dcc.Dropdown(
                            id={'type': 'input',
                                'index': 0},
                            options=[
                            {'label': i, 'value': i} for i in unique_vals['reason_for_search']
                            ],
                            clearable = False,
                            multi = True,
                            value='Erratic/Suspicious Behavior')
                        ], width=6),
                    dbc.Col([
                        dbc.Label("Result of Search", html_for={'type': 'input', 'index': 1}),
                        dcc.Dropdown(
                            id={'type': 'input', 
                                'index': 1},
                            options = [
                                {'label': 'Contraband Found', 'value': True },
                                {'label': 'Contraband Not Found', 'value': False}
                                ],
                            value=False,
                            clearable=False)
                            ], width=6)
                    ]
        
    @app.callback([Output('outcome-radio', 'value'),
                   Output('outcome-radio', 'options')],
                  Input('scenario-radio', 'value'))
    def return_scenario_radio_buttons(scenario_val):
        if scenario_val == 'You are pulled over':
            return 'arrest',  [
                                    {'label': 'Whether You Are Arrested', 'value': 'arrest'},
                                    {'label': 'Whether You Are Searched', 'value': 'search'},
                                ]
        else:
            return 'arrest', [
                                    {'label': 'Whether You Are Arrested', 'value': 'arrest'},
                                    {'label': 'Whether You Are Searched', 'value': 'search', 'disabled': True},
                                ]
