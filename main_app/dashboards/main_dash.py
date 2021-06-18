# -*- coding: utf-8 -*-
"""
Page for Plotly Dashboard
"""

import dash
import dash_html_components as html
from .html_layout import html_layout
import dash_core_components as dcc
from dash.dependencies import Input, Output, ALL, State
from .data import load_unique_vals, add_search_inputs
import requests
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pandas import DataFrame



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
                    ]),
                html.Hr(),
                dbc.Row(
                dbc.Button('Run Analysis', id="submit-button"), style={'padding': '20px', 'padding-top': '10px'})
                ]

    # Create Dash Layout
    dash_app.layout = html.Div(id='main-div', children=[
        dbc.Container([
            html.Br(),
            html.Br(),
            ### Begin Row With Card of Information On It
            dbc.Row([
                dbc.Col([dbc.Card(id='input-card', children=card_content)
                         ], lg=4),
                dbc.Col([
                    dcc.Loading(
                        html.Div(id='output-div'))
                    ], lg=8)
            ]),
            html.Hr()
            ]),
        ])

    return dash_app.server


def register_callbacks(app):
    @app.callback(
        Output('output-div', 'children'),
        Input('submit-button', 'n_clicks'),
        [State('scenario-radio', 'value'),
         State('city-dropdown', 'value'),
         State('race-dropdown', 'value'),
         State('sex-dropdown', 'value'),
         State('reason-dropdown', 'value'),
         State('age-input', 'value'),
         State('hour-input', 'value'),
         State('season-input', 'value'),
         State('day-dropdown', 'value'),
         State('outcome-radio', 'value'),
         State({'type': 'input', 'index': ALL}, 'value')])
    def dump_data(*args):
        params = {
            'city': args[2],
            'subject_age':  args[6],
            'subject_race': args[3],
            'subject_sex': args[4],
            'reason_for_stop': args[5],
            'hour': args[7],
            'dayofweek': args[9],
            'quarter': args[8],
            }

        if args[0] == 0:
            return html.H1("Please Fill Out the Form to the Left and Hit 'Run Analysis' To See Your Chances of Being Arrested or Searched")

        if args[1] in 'You have been searched':
            params['search_outcome'] = 'unknown'
            params['searched'] = True
        elif args[1] == 'Your search has been completed':
            params['search_outcome'] = 'known'
            params['searched'] = True
        elif args[1] == 'You are pulled over':
            params['search_outcome'] = 'unknown'
            params['searched'] = False

        params = add_search_inputs(params, args[11])
        request = requests.get(url=f"http://police-project-test.xyz/api/v1/{args[10]}", params=params).json()
        chart_data = request.pop('outcome_vals')
        base_value = chart_data.pop('base_value')
        new_sample = DataFrame(chart_data, index=[0]).T
        new_sample.sort_values(by=0, inplace=True)
        new_sample['Positive']  = new_sample[0] > 0
        new_sample['Positive']  = new_sample['Positive'].astype(int)
        try:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=new_sample[0], y=new_sample.index, text=new_sample[0], orientation='h', marker={'color': new_sample['Positive'], 'colorscale': 'spectral'}))
            fig.update_traces(texttemplate='%{text:.0%}', textposition='auto')
            fig.update_layout(uniformtext_minsize = 8,
                      uniformtext_mode = 'hide',
                      xaxis = {'tickformat' : '%'},
                      xaxis_title = f"Base Value: {base_value:.2%}",
                      title={'text': "What Contributes to the Outcome: ",
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                      margin={'r': 0})
            fig.update_yaxes(
                tickangle = -45)
            return [html.H1(f"Chance of {args[10]}: {request['proba']:.1%}", style={'textAlign': 'center'}),
                    dcc.Graph(id='explainer-graph', figure=fig)]

        except Exception as e:
            print(f"Error: {e}")
            return html.H3("Uh-oh!  Something did not work right.  Please try looking over your values to make sure they are\
                           correct.  If they are, please try again later as something is not right.")

    @app.callback(Output('search-row', 'children'),
                   Input('scenario-radio', 'value'),
                   State({'type': 'input', 'index': ALL}, 'value'))
    def display_search_row(scenario_val, search_vals):
        if not search_vals:
            dropdown_val = None
        else:
            dropdown_val = search_vals[0]

        print(f"Value of search_vals: {search_vals}")
        print(f"Value of dropdown_val: {dropdown_val}")

        unique_vals = load_unique_vals()
        if scenario_val == 'You are pulled over':
            return []
        elif scenario_val == 'You have been searched':
            return dbc.Col([
                        dbc.Label("Reason For Search (Choose All That Apply)", html_for={'type': 'input', 'index': 0}),
                        dcc.Dropdown(
                            id={'type': 'input',
                                'index': 0},
                            options = [
                                {'label': i, 'value': i} for i in unique_vals['reason_for_search']
                            ],
                            clearable = False,
                            multi = True,
                            value = dropdown_val)
                        ])

        elif scenario_val == 'Your search has been completed':
            return [
                    dbc.Col([
                        dbc.Label("Reason For Search (choose all that apply, Leave blank if no search conducted)", html_for={'type': 'input', 'index': 0}),
                        dcc.Dropdown(
                            id={'type': 'input',
                                'index': 0},
                            options = [
                                {'label': i, 'value': i} for i in unique_vals['reason_for_search']
                            ],
                            clearable = False,
                            multi = True,
                            value = dropdown_val)
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
