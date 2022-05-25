from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_json('activities.json', orient='records')

barchart = px.bar(df,
                  x='year',
                  y='distance',
                  color='type')

nav_bar = dbc.NavbarSimple(
    brand='Strava Viewer by MWK Solution',
    color='primary',
    dark=True)

fig = dcc.Graph(figure=barchart,
                config={'displaylogo'           : False,
                        'displayModeBar'        : True,
                        'scrollZoom'            : True,
                        'showAxisDragHandles'   : True,
                        'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'resetScale2d'],
                        'toImageButtonOptions'  : {'format': 'jpeg', 'scale': 2}},
                style={'height': '80vh', 'width': '80vw'},
                id='bar-chart')

load_button = dbc.Button(
    children='Load data',
    n_clicks=0,
    color='success',
    id='load-data',
    type='submit',
    className='ms-4')

main_layout = html.Div([
    dbc.Row([dbc.Col([html.H2('Activities bar chart')], width=3)], justify='center'),
    dbc.Row([
        dbc.Col([load_button],
                width=1),
        dbc.Col([fig]),
        dbc.Col([],
                width=1)])])

app_layout = html.Div([nav_bar,
                       main_layout])
