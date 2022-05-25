
from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from layouts import app_layout

app = Dash(__name__,
           title='Strava Viewer',
           external_stylesheets=[DARKLY],
           prevent_initial_callbacks=True)

app.layout = app_layout


if __name__ == '__main__':
    app.run_server(debug=True)
