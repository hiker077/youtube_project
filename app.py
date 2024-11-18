from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, datetime, timedelta

YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'
EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css"]


#Load and process data 
def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df['TITLE'] = [f'[{title}]({link})' for title, link in zip(df['TITLE'], ('https://www.youtube.com/watch?v=' + df['VIDEOID']))]
    return df 

df = load_data('data/dashboard_data/youtube_data_dashboard.csv')

#Helper functions
def data_filter(dff, chart1_state, chart3_state, chart4_state , trigger_id, slider_filter_state, dropdown_filter_state, state_data,date_picker_start, date_picker_end, is_month = False):
    """Filter our all neceserry data base on callback Input and State conditions."""

    dff['PUBLISHEDAT'] = pd.to_datetime(dff['PUBLISHEDAT'])
    date_picker_start = datetime.strptime(date_picker_start, '%Y-%m-%d').date()
    date_picker_end = datetime.strptime(date_picker_end, '%Y-%m-%d').date()
    dff = dff.loc[(dff['PUBLISHEDAT'].dt.date>= date_picker_start ) & (dff['PUBLISHEDAT'].dt.date<= date_picker_end)]
    dff = dff[(dff['VIDEO_TIME']>= slider_filter_state[0]) & (dff['VIDEO_TIME']<= slider_filter_state[1])]
    dff = dff[dff['CATEGORY_TITLE'].isin(dropdown_filter_state)]
    
    state_data = state_data if state_data is not None else {}

    if trigger_id is not None:

        if trigger_id in state_data:
            state_data.pop(trigger_id)      
        else:
            state_data[trigger_id] = 0

        if chart1_state is not None and 'chart-1' in state_data:
            chart1_state = chart1_state['points'][0]['x']
            month = pd.to_datetime(chart1_state).strftime('%Y-%m')
            dff = dff[dff['YEAR_MONTH']==month]
        
        if chart3_state is not None and 'chart-3' in state_data:
            chart3_state = chart3_state['points'][0]['x']
            dff = dff[dff['DAY_OF_WEEK_NAME']==chart3_state]

        if chart4_state is not None and 'chart-4' in state_data:
            chart4_state = chart4_state['points'][0]['x']
            dff = dff[dff['CATEGORY_TITLE']==chart4_state]
    else:
        state_data = {}
 
    return dff, state_data


def kpis(df):
    """Count KPI's results which are displayed on main dashboard page."""

    count = len(df)
    views_mean = round(df['VIEWCOUNT'].mean(),0)
    comment_mean= round(df['COMMENTCOUNT'].mean(),0)
    like_mean = round(df['LIKECOUNT'].mean(),0)

    return count, views_mean, comment_mean, like_mean


def build_charts(data: pd.DataFrame):
    """Generate 4 charts dispaly in dashboard."""

    ## Chart 1 
    df1 = data.groupby('YEAR_MONTH')['YEAR_MONTH'].count().reset_index(name='count').sort_values(by="YEAR_MONTH", ascending=True)
    fig1 = px.line(df1, x= 'YEAR_MONTH', y= 'count', markers=True, text= 'count', template= 'plotly_white')
    fig1.update_traces(textposition="top right", line=dict(color='firebrick', width=3), line_shape='spline')
    fig1.update_layout(title='Number of published videos',
                   xaxis_title='Month',
                   yaxis_title='Number of movies',
                   barmode='group', 
                   xaxis_tickangle=-45)
    #Chart 2 
    df2 = data.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": 'mean',"LIKECOUNT": ['mean', 'count']}).reset_index()
    df2.columns = ['_'.join(col).strip('_') for col in df2.columns]
    df2.columns = ['Category', 'Average of views', 'Average of likes','Number of movies']
    sizeref = 2.*(df2['Number of movies'].max())/(100**2)    
    fig2 = px.scatter(df2, x = 'Average of views', y= 'Average of likes',size= 'Number of movies', color='Category', template= 'plotly_white')
    fig2.update_traces(marker=dict(sizemode='area', sizeref=sizeref, line_width=2))
    fig2.update_layout(title='Category statistics',
                   xaxis_title='Avg. number of views',
                   yaxis_title='Avg. number of likes')
    #Chart 3 
    df3 = data.groupby(['DAY_OF_WEEK_NAME','PUBLISHED_PERIOD','DAY_OF_WEEK_NUMBER']).size().reset_index(name='COUNT').sort_values(by= 'DAY_OF_WEEK_NUMBER')
    fig3 = px.bar(df3, x='DAY_OF_WEEK_NAME', y='COUNT', color='PUBLISHED_PERIOD', template= 'plotly_white')
    fig3.update_layout(title='Day of video publication',
                        xaxis_title='Day of week',
                        yaxis_title='Number of movies'
                       )
    #Chart 4
    fig4 = px.box(data, x='CATEGORY_TITLE', y='VIDEO_TIME', template='plotly_white',  color='CATEGORY_TITLE')
    # fig4.update_traces( boxpoints='all', jitter=0.5,)
    fig4.update_layout(title='Statistics of video time',
                        xaxis_title='Category',
                        yaxis_title='Video time',
                        showlegend = False
                       )
    
    return fig1, fig2, fig3, fig4


FILTER_CARD =[

    dbc.CardBody(
        [
                    html.Div(dcc.Store(id='master-data',data= df.to_dict('records'))),
                    html.Div(dcc.Store(id='state-data')),
                    html.H4("Filters", className='mb-4'),
                    html.Div([
                        html.H6('Date', className='mb-3'),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            month_format='DD/MM/YYYY',
                            end_date_placeholder_text='DD/MM/YYYY',
                            start_date= pd.to_datetime(df['PUBLISHEDAT']).dt.date.min(), #date.today() - timedelta(days=90),
                            end_date=  pd.to_datetime(df['PUBLISHEDAT']).dt.date.max()
                        ),
                        ],
                        className='mb-3'),
                    html.Div([
                        html.H6("Duration of video (minutes)"),
                        dcc.RangeSlider(
                        min=df['VIDEO_TIME'].min(),
                        max=df['VIDEO_TIME'].max(),
                        # step=1,
                        tooltip={"placement": "bottom", "always_visible": True},
                        allowCross=False,
                        marks=None, 
                        id='slider-filter',
                        value=[df['VIDEO_TIME'].min(), df['VIDEO_TIME'].max()],
                        )],
                        className='mb-3'
                        ),
                    html.Div([
                        html.H6("Categories"),
                        dcc.Dropdown(
                        options= df['CATEGORY_TITLE'].unique(),
                        value= df['CATEGORY_TITLE'].unique(),
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
                        html.Div(html.Img(src=YOUTUBE_LOGO, height="40px")),
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




app = Dash(__name__, external_stylesheets= EXTERNAL_STYLESHEETS)

app.layout = html.Div(children=[BODY])








@app.callback(
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)





