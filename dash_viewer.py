"""App starter and callbacks definitions"""
from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from dash import Input, Output, State
from layouts import app_layout, METRIC_OPTIONS, get_chart
from strava_data import request_access_token, get_activities, dump_acts_to_file
from activities import get_acts_from_file, get_types, get_options, get_years

app = Dash(__name__,
           title='Strava Viewer',
           external_stylesheets=[DARKLY],
           prevent_initial_callbacks=True)
# for heroku
server = app.server

app.layout = app_layout


@app.callback([Output('loading', 'children'),
               Output('metrics-input', 'options'),
               Output('metrics-input', 'value'),
               Output('activity-input', 'options'),
               Output('activity-input', 'value')],
              Input('load-data', 'n_clicks'),
              prevent_initial_call=True)
def load_data(n_clicks):
    """Callback when clicking 'Load or refresh data' button. Updates <activities.json> file and then metrics and activities to choose from."""
    if n_clicks > 0:
        token = request_access_token()
        activities = get_activities(token)
        dump_acts_to_file(activities)

        df = get_acts_from_file()
        activity_types = get_types(df)
        activity_options = get_options(activity_types)
        metrics_options = METRIC_OPTIONS
        years_all = get_years(df)
        metrics_value = 'distance'

        return '', metrics_options, metrics_value, activity_options, activity_types


@app.callback(Output('bar-chart', 'figure'),
              [Input('metrics-input', 'value'),
               Input('activity-input', 'value'),
               Input('years-input', 'value')],
              prevent_initial_call=True)
def show_bar_chart(metrics, activity, year):
    """Callback updates barchart when changes to metrics or activities are made."""
    df = get_acts_from_file()
    if year != 'All':
        df = df[df['year'] == int(year)]
    df = df[df['type'].isin(activity)]
    barchart = get_chart(df, metrics, activity, year)
    return barchart


if __name__ == '__main__':
    app.run_server(debug=True)
