from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, datetime, timedelta
import os 
from components.layout import create_layout
from components.callbacks import register_callbacks
from components.helpers import load_data

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css"]
YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'

data = load_data(os.path.join(BASE_DIR, 'youtube_project','data', 'data_processed','youtube_data_dashboard.csv'))

app = Dash(__name__, external_stylesheets= EXTERNAL_STYLESHEETS)
app.title = "YouTube Dashboard"

app.layout = create_layout(data, YOUTUBE_LOGO)  ## dokoncz to 

register_callbacks(app)

