"""App setup and starter"""
from dash_extensions.enrich import MultiplexerTransform, DashProxy
from dash_bootstrap_components.themes import DARKLY
from strava_viewer import Layout, StravaData, get_callbacks

app = DashProxy(__name__,
                title='Strava Viewer',
                external_stylesheets=[DARKLY],
                transforms=[MultiplexerTransform()],
                prevent_initial_callbacks=True)

# for deployment
server = app.server

# data hook
data = StravaData(data='redis')

# definition of app layout, instance is callable
app.layout = Layout(data=data)()

# import callbacks
get_callbacks(app=app, data=data)

if __name__ == '__main__':
    app.run_server(debug=True)
