from dash import Dash, callback, Output, Input, ctx, State, no_update
# import plotly.express as px
# import dash_bootstrap_components as dbc
import pandas as pd
# from datetime import date, datetime, timedelta
# import os 
from src.dashboard.utilities import data_filter, build_charts, kpis


def register_callbacks(app_name):

    @app_name.callback(
        Output('chart-1', 'figure'),
        Output('chart-2', 'figure'),
        Output('chart-3', 'figure'),
        Output('chart-4', 'figure'),
        Output('table-data', 'data'),
        Output('slider-filter', 'value'),
        Output('state-data', 'data'),
        Output('dropdown-filter', 'value'),
        Output('number-of-videos', 'children'),
        Output('avg-number-of-views', 'children'),
        Output('avg-number-of-comments', 'children'),
        Output('avg-number-of-likes', 'children'),

        Input('chart-1', 'clickData'),
        Input('chart-3', 'clickData'),
        Input('chart-4', 'clickData'),
        Input('master-data', 'data'),
        Input('slider-filter', 'value'),
        Input('dropdown-filter', 'value'),
        Input('state-data', 'data'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),

        State('slider-filter', 'value'),
        State('dropdown-filter', 'value'),
        State('chart-1', 'clickData'),
        State('chart-3', 'clickData'),
        State('chart-4', 'clickData'),
    )

    def update_all(chart1_data, chart3_data, chart4_data, master_data, slider_filter, dropdown_filter, state_data, date_picker_start, date_picker_end, slider_filter_state, dropdown_filter_state, chart1_state, chart3_state, chart4_state ):

        triggered_id = ctx.triggered_id
        dff = pd.DataFrame(master_data)
        dff, state_data = data_filter(dff, chart1_state, chart3_state, chart4_state, triggered_id, slider_filter_state, dropdown_filter_state, state_data, date_picker_start, date_picker_end,   True)
        figg1, figg2, figg3, figg4 = build_charts(dff)
        filter_value = no_update
        filter2_value = no_update
        number_of_videos, avg_number_of_views, avg_number_of_comments, avg_number_of_likes  = kpis(dff)
        dff =  dff.to_dict('records')
        
        return figg1, figg2, figg3, figg4, dff, filter_value, state_data, filter2_value, number_of_videos, avg_number_of_views, avg_number_of_comments, avg_number_of_likes
