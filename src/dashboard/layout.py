from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, datetime, timedelta
import os 
from helpers import get_filters_parameters
YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'

# picker_range_start_date
# picker_range_end_date
# range_sider_video_time_min
# range_sider_video_time_max
# drop_down_category
# LOGO

def create_layout(data, youtube_logo):

    raw_data, picker_range_start_date, picker_range_end_date, range_sider_video_time_min, range_sider_video_time_max, drop_down_category = get_filters_parameters(data)

    FILTER_CARD =[

        dbc.CardBody(
            [
                        html.Div(dcc.Store(id='master-data',data= raw_data)),  #df.to_dict('records')
                        html.Div(dcc.Store(id='state-data')),
                        html.H4("Filters", className='mb-4'),
                        html.Div([
                            html.H6('Date', className='mb-3'),
                            dcc.DatePickerRange(
                                id='date-picker-range',
                                month_format='DD/MM/YYYY',
                                end_date_placeholder_text='DD/MM/YYYY',
                                start_date= picker_range_start_date, # pd.to_datetime(df['PUBLISHEDAT']).dt.date.min(), 
                                end_date= picker_range_end_date #  pd.to_datetime(df['PUBLISHEDAT']).dt.date.max()
                            ),
                            ],
                            className='mb-3'),
                        html.Div([
                            html.H6("Duration of video (minutes)"),
                            dcc.RangeSlider(
                            min= range_sider_video_time_min, #df['VIDEO_TIME'].min(),
                            max= range_sider_video_time_max, #df['VIDEO_TIME'].max(),
                            # step=1,
                            tooltip={"placement": "bottom", "always_visible": True},
                            allowCross=False,
                            marks=None, 
                            id='slider-filter',
                            value= [range_sider_video_time_min, range_sider_video_time_max]  #[df['VIDEO_TIME'].min(), df['VIDEO_TIME'].max()],
                            )],
                            className='mb-3'
                            ),
                        html.Div([
                            html.H6("Categories"),
                            dcc.Dropdown(
                            options= drop_down_category, # df['CATEGORY_TITLE'].unique(),
                            value= drop_down_category, # df['CATEGORY_TITLE'].unique(),
                            multi=True,
                            id= 'dropdown-filter'
                            )],
                            className='mb-3'
                        )

            ],
            className='mb-1'
            
        )
    ]


    BODY = dbc.Container(
        [
        ##Filter
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            html.Div(html.Img(src=youtube_logo, height="40px")),
                            className='my-3'
                        ),
                        dbc.Row(
                            html.Div('Analyse your favourite channel statistics'),
                            className= 'fst-italic fs-4 my-4'
                        ),
                        
                        dbc.Row(
                            dbc.Card(FILTER_CARD, color='light')
                            )
                    
                    ],
                    md=2
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H6("Number of videos", className="card-title text-muted"),
                                                # html.H2("$10,499.93", className="card-text fw-bold"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.I(className="bi-camera-video"), style={"color": "red"}),  # Icon column
                                                        dbc.Col(html.H2(id='number-of-videos', className="card-text fw-bold"))   # Number column
                                                    ],
                                                    className="align-items-center"  # Vertically align icon and number
                                                ),
                                            ]),
                                            className="shadow-sm my-2"
                                        ),
                                        width=3,
                                    
                                        ),
                                dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H6("Average number of views", className="card-title text-muted"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.I(className="bi bi-eye-fill", style={"color": "red"})),  # Icon column
                                                        dbc.Col(html.H2(id='avg-number-of-views', className="card-text fw-bold"))   # Number column
                                                    ],
                                                    className="align-items-center"  # Vertically align icon and number
                                                ),
                                            ]),
                                            className="shadow-sm my-2"
                                        ),
                                        width=3,
                                    
                                        ),
                                dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H6("Average number of comments", className="card-title text-muted"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.I(className="bi bi-chat-left-text-fill"), style={"color": "red"}),  # Icon column
                                                        dbc.Col(html.H2(id='avg-number-of-comments', className="card-text fw-bold"))   # Number column
                                                    ],
                                                    className="align-items-center"  # Vertically align icon and number  
                                                ),
                                            ]),
                                            className="shadow-sm my-2"
                                        ),
                                        width=3,
                                    
                                        ),
                                dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H6("Average number of likes", className="card-title text-muted"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.I(className="bi bi-hand-thumbs-up-fill", style={"color": "red"})),  # Icon column
                                                        dbc.Col(html.H2(id='avg-number-of-likes', className="card-text fw-bold"))   
                                                    ],
                                                    className="align-items-center"  # Vertically align icon and number
                                                ),
                                            ]),
                                            className="shadow-sm my-2"
                                        ),
                                        width=3,
                                    
                                        )
                                    
                            ],
                            className= 'my-4'
                        
                        ),
                    
                        dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(id='chart-1', config={"displayModeBar": False}), className='shadow-sm border rounded-3'),
                                    dbc.Col(dcc.Graph(id='chart-2', config={"displayModeBar": False}), className='shadow-sm border rounded-3'),
                                    dbc.Col(dcc.Graph(id='chart-3', config={"displayModeBar": False}), className='shadow-sm border rounded-3'),
                                    dbc.Col(dcc.Graph(id='chart-4', config={"displayModeBar": False}), className='shadow-sm border rounded-3')
                                ],
                                className='row row-cols-1 row-cols-md-2 row-cols-lg-2 my-4 g-3 '),
                                
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    dash_table.DataTable(
                                        id='table-data',
                                        columns=[ #{'name': 'TITLE', 'id': 'TITLE', 'presentation': 'markdown'},
                                            {'name': 'Video title', 'id': 'TITLE', 'presentation': 'markdown'},
                                            {'name': 'Youtube category', 'id': 'CATEGORY_TITLE'},
                                            {'name': 'Viws', 'id': 'VIEWCOUNT'},
                                            {'name': 'Likes', 'id': 'LIKECOUNT'},
                                            {'name': 'Comments', 'id': 'COMMENTCOUNT'},
                                            {'name': 'Publishing time', 'id': 'PUBLISHED_PERIOD'},
                                            {'name': 'Week day publishing', 'id': 'DAY_OF_WEEK_NAME'},

                                            # {'name': i, 'id': i} for i in ['VIEWCOUNT', 'LIKECOUNT', 'COMMENTCOUNT', 'PUBLISHED_PERIOD', 'DAY_OF_WEEK_NAME', 'CATEGORY_TITLE']
                                            ],
                                        page_size=50,
                                        filter_action= 'native',
                                        sort_action= 'native',
                                        style_data= {
                                            'whiteSpace':'normal',
                                            'height': 'auto'
                                        },
                                        style_header = {
                                            'fontWeight': 'bold'
                                        },
                                        sort_by=[{"column_id": "VIEWCOUNT", "direction": "desc"}]
                                        # fixed_rows={'headers': True, 'data':0}

                                        )
                                    ),
                                className='justify-content-center my-2'
                                ),
                        )
                    ],
                    md=10, 
        
                )
            ],


            className='mx-3'
        ),
        ],fluid=True,
        className= "bg-light"
    )
    return html.Div(children=[BODY])