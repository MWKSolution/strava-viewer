"""Layouts definition for strava-viewer dash app"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from activities import acts_file_present, get_acts_from_file, get_types, get_options

# Options list as a parameter for dash dbc.RadioItems options. Doesn't change so it is const.
METRIC_OPTIONS = [
        {'label': 'Distance [km]', 'value': 'distance'},
        {'label': 'Time [h]', 'value': 'time'},
        {'label': 'Elevation gain [m]', 'value': 'gain'}]
# {'label': 'Quantity', 'value': 'quan'}] ... for further development


def get_chart(df, metrics, activity):
    """Get plotly bar chart for given parameters

    """
    # start from empty Figure
    barchart = go.Figure()
    # stacked activities - one colour for one activity
    for i in activity:
        dfa = df[df['type'] == i]
        barchart.add_trace(go.Bar(
                          x=dfa['year'],
                          y=dfa[metrics],
                          name=i,
                          showlegend=True))
    barchart.update_layout(barmode='stack')
    # add total sum for given metrics
    dfs = df.groupby(['year'], as_index=False).sum()
    barchart.add_trace(
        go.Scatter(
            x=dfs['year'],
            y=dfs[metrics],
            text=dfs[metrics],
            mode='text',
            textposition='top center',
            texttemplate='%{text:.3s}',
            showlegend=False))
    return barchart


# Initiation some parameters for default view (when you load page for the first time
if acts_file_present():  # check if activities file is present (if it is first run?)
    df = get_acts_from_file()
    activity_types = get_types(df)
    activity_options = get_options(activity_types)
    metrics_options = METRIC_OPTIONS
    metrics_value = 'distance'
    barchart = get_chart(df, metrics_value, activity_types)
else:  # otherwise, prepare empty layout, it will change after clicking button: 'Load or refresh data'
    barchart = {'data': [], 'layout': {}, 'frames': [], }
    activity_options = []
    activity_types = []
    metrics_options = []
    metrics_value = ''

fig = dcc.Graph(figure=barchart,
                config={'displaylogo'           : False,
                        'displayModeBar'        : True,
                        'scrollZoom'            : True,
                        'showAxisDragHandles'   : True,
                        'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'resetScale2d'],
                        'toImageButtonOptions'  : {'format': 'jpeg', 'scale': 2}},
                style={'height': '80vh', 'width': '66vw'},
                id='bar-chart')

load_button = dbc.Button(
    children='Load or refresh data',
    n_clicks=0,
    color='success',
    id='load-data',
    type='submit',
    className='m-4')

load_indicator = dbc.Spinner(html.Div(id='loading'),
                             spinner_style={'width': '20rem', 'height': '20rem'},
                             fullscreen=True,
                             color='danger')

metrics = html.Div([
    dbc.Alert('Choose metrics', color='info', className='m-2'),
    dbc.RadioItems(
        options=metrics_options,
        value=metrics_value,
        id='metrics-input',
        className='m-3')])

activity = html.Div([
    dbc.Alert('Choose activity', color='info', className='m-2'),
    dbc.Checklist(
        options=activity_options,
        value=activity_types,
        id='activity-input',
        className='m-3')])

main_layout = html.Div([
    dbc.Row([dbc.Col([load_button, load_indicator], width=2)], justify='center'),
    dbc.Row([
        dbc.Col([metrics],
                width=2),
        dbc.Col([fig], width=8),
        dbc.Col([activity],
                width=2)], justify='center')])

nav_bar = dbc.NavbarSimple(
    brand='Strava Viewer by MWK Solution',
    color='primary',
    dark=True)

app_layout = html.Div([nav_bar,
                       main_layout])
