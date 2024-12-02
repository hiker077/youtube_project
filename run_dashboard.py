from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
import dash_bootstrap_components as dbc
from src.dashboard.layout import create_layout
from src.dashboard.callbacks import register_callbacks
from src.dashboard.utilities import load_data
from dotenv import dotenv_values

config = dotenv_values(".env")
dashboard_data = config['DASHBOARD_DATA_FILE']


EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css"]
YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'

data = load_data(dashboard_data)

app = Dash(__name__, external_stylesheets= EXTERNAL_STYLESHEETS)
app.title = "YouTube Dashboard"

app.layout = create_layout(data, YOUTUBE_LOGO)  ## dokoncz to 

register_callbacks(app)


if __name__ == '__main__':
     app.run_server(debug=True)