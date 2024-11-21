from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, datetime, timedelta
import os 
from components.helpers import get_filters_parameters
from test import app


if __name__ == '__main__':
     app.run_server(debug=True)