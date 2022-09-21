"""App starter and callbacks definitions"""
from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from dash import Input, Output
from strava_viewer import Layout
from strava_viewer import StravaData

app = Dash(__name__,
           title='Strava Viewer',
           external_stylesheets=[DARKLY],
           prevent_initial_callbacks=True)

# for deployment
server = app.server

# data hook
data = StravaData(data='local')

# definition of app layout, instance is callable
app.layout = Layout(data)()


# callbacks
@app.callback([Output('loading', 'children'),
               Output('metrics-input', 'options'),
               Output('metrics-input', 'value'),
               Output('activity-input', 'options'),
               Output('activity-input', 'value'),
               Output('years-input', 'options'),
               Output('years-input', 'value')],
              Input('load-data', 'n_clicks'),
              prevent_initial_call=True)
def load_data(n_clicks):
    """Callback when clicking 'Reload all data' button."""
    if n_clicks > 0:
        data.reload_all_dataAPI()
        metrics, activities, year = data.get_optionsDATA()
        return '', metrics.options, metrics.value, activities.options, activities.types, year.options, year.value


@app.callback(Output('bar-chart', 'figure'),
              [Input('metrics-input', 'value'),
               Input('activity-input', 'value'),
               Input('years-input', 'value')],
              prevent_initial_call=True)
def show_bar_chart(metrics, activity, year):
    """Callback updates barchart when changes to metrics or activities or year are made."""
    barchart = data.get_chartDATA(metrics, activity, year)
    return barchart


if __name__ == '__main__':
    app.run_server(debug=True)
