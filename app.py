from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'
df = pd.read_csv('data/dashboard_data/youtube_data_dashboard.csv')


external_stylesheets = [dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css"]


# NAVBAR = dbc.Navbar(
#     children=[
#         # Use row and col to control vertical alignment of logo / brand
#         dbc.Row(
#             [
#                 dbc.Col(html.Img(src=YOUTUBE_LOGO, height="60px")),
#                 dbc.Col("Dashboad"),
#                 dbc.Col("Repository")
#             ],
#             align="center"
#         )
#     ],
#     color="gray",
#     dark=True,
#     sticky="top",
# )


FILTER_CARD =[
    # dbc.CardHeader(html.H4("Filters", className="card-title")),
    dbc.CardBody(
        [
        #dbc.Row(
           # [
            #dbc.Col(
             #   [
                    html.Div(dcc.Store(id='master-data',data= df.to_dict('records'))),
                    # html.Div(dcc.Store(id='state-data', data= {'State': 1})),
                    html.Div(dcc.Store(id='state-data')),
                    # html.Button("Reset Selection", id='reset-button', n_clicks=0),
                    html.H4("Filters", className='mb-4'),
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
              #  ]
           # )
           # ]
        #)
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
                        #    FILTER_CARD
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
                                                    dbc.Col(html.I(className="bi-camera-video")),  # Icon column
                                                    dbc.Col(html.H2("10,499", className="card-text fw-bold"))   # Number column
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
                                                    dbc.Col(html.I(className="bi bi-eye-fill")),  # Icon column
                                                    dbc.Col(html.H2("10,499", className="card-text fw-bold"))   # Number column
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
                                                    dbc.Col(html.I(className="bi bi-chat-left-text-fill")),  # Icon column
                                                    dbc.Col(html.H2("10,499", className="card-text fw-bold"))   # Number column
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
                                                    dbc.Col(html.I(className="bi bi-hand-thumbs-up-fill")),  # Icon column
                                                    dbc.Col(html.H2("10,499", className="card-text fw-bold"))   # Number column
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
                    # dbc.Row(
                    #     [
                    #         dbc.Col(dcc.Graph(id='chart-1',config={"displayModeBar": False}),className='shadow-sm border rounded-3 mx-2 mb-4'  ),
                    #         dbc.Col(dcc.Graph(id='chart-2',config={"displayModeBar": False}), className='shadow-sm border rounded-3 mx-2 mb-4')
                    #         # dbc.Col(dcc.Graph(id='chart-3',config={"displayModeBar": False}),width=3, className='border border-secondary rounded-3 mx-3'  ),
                    #         # dbc.Col(dcc.Graph(id='chart-4',config={"displayModeBar": False}),width=3, className='border border-secondary rounded-3 mx-3' )
                    #         ],
                    #         # className= ''
                    #          ),
                    # dbc.Row(
                    #     [
                    #         # dbc.Col(dcc.Graph(id='chart-1',config={"displayModeBar": False}),width=3, className='border border-secondary rounded-3 mx-3' ),
                    #         # dbc.Col(dcc.Graph(id='chart-2',config={"displayModeBar": False}),width=3, className='border border-secondary rounded-3 mx-3'  ),
                    #         dbc.Col(dcc.Graph(id='chart-3',config={"displayModeBar": False}), className='shadow-sm border  rounded-3  mx-2 mb-4'  ),
                    #         dbc.Col(dcc.Graph(id='chart-4',config={"displayModeBar": False}), className='shadow-sm border  rounded-3  mx-2 mb-4' )
                    #         ],
                    #         # className= 'row-cols-2 mb-4'
                    #          ),
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
                                    columns=[{'name': i, 'id': i} for i in ['TITLE', 'VIEWCOUNT', 'LIKECOUNT', 'COMMENTCOUNT', 'PUBLISHED_PERIOD', 'DAY_OF_WEEK_NAME', 'CATEGORY_TITLE']],
                                    page_size=50,
                                    filter_action= 'native',
                                    sort_action= 'native',
                                    style_data= {
                                        'whiteSpace':'normal',
                                        'height': 'auto'
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
                # className= 'my-5'
            )
        ],

        #  style={"marginTop": 30}
        className='mx-3'
    ),
   
    # dbc.Row(
    #     dbc.Col(
    #         html.Div(
    #         dash_table.DataTable(
    #             id='table-data',
    #             columns=[{'name': i, 'id': i} for i in ['TITLE', 'VIEWCOUNT', 'LIKECOUNT', 'COMMENTCOUNT', 'PUBLISHED_PERIOD', 'DAY_OF_WEEK_NAME', 'CATEGORY_TITLE']],
    #             page_size=50,
    #             filter_action= 'native',
    #             sort_action= 'native'

    #             )
    #         )
    #     )
        
    # )

    ],fluid=True,
     className= "bg-light"

)




app = Dash(__name__, external_stylesheets= external_stylesheets)

# app.layout = html.Div(children=[NAVBAR, BODY])
app.layout = html.Div(children=[BODY])


def chart_bulilder(dff):
    ## Chart 1 
    # df1 = dff.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
    df1 = dff.groupby('YEAR_MONTH')['YEAR_MONTH'].count().reset_index(name='count').sort_values(by="YEAR_MONTH", ascending=True)
    fig1 = px.line(df1, x= 'YEAR_MONTH', y= 'count', markers=True, text= 'count', template= 'plotly_white')
    fig1.update_traces(textposition="top right", line=dict(color='firebrick', width=3), line_shape='spline')
    fig1.update_layout(title='Number of published videos',
                   xaxis_title='Month',
                   yaxis_title='Number of movies',
                   barmode='group', 
                   xaxis_tickangle=-45)
  

    #Chart 2 
    df2 = dff.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": 'mean',"LIKECOUNT": ['mean', 'count']}).reset_index()
    df2.columns = ['_'.join(col).strip('_') for col in df2.columns]
    df2.columns = ['Category', 'Average of views', 'Average of likes','Number of movies']
    ##Text in hover
    # hover_text_chart2 = []
    # for index, row in df2.iterrows():
    #     hover_text_chart2.append(('Category: {category}<br>'+
    #                             'Average of views: {views_mean}<br>'+
    #                             'Average of likes: {likes_mean}<br>'+
    #                             'Number of movies: {movies_number}<br>').format(category = row['CATEGORY_TITLE'],
    #                                                                             views_mean = row['VIEWCOUNT_mean'],
    #                                                                             likes_mean = row['LIKECOUNT_mean'],
    #                                                                             movies_number = row['LIKECOUNT_count']
    #                                                                             ))
    # df2['text'] = hover_text_chart2

    sizeref = 2.*(df2['Number of movies'].max())/(100**2)    
    fig2 = px.scatter(df2, x = 'Average of views', y= 'Average of likes',size= 'Number of movies', color='Category', template= 'plotly_white')
    fig2.update_traces(marker=dict(sizemode='area', sizeref=sizeref, line_width=2))
    fig2.update_layout(title='Category statistics',
                   xaxis_title='Avg. number of views',
                   yaxis_title='Avg. number of likes')
    
 

    #Chart 3 
    df3 = dff.groupby(['DAY_OF_WEEK_NAME','PUBLISHED_PERIOD','DAY_OF_WEEK_NUMBER']).size().reset_index(name='COUNT').sort_values(by= 'DAY_OF_WEEK_NUMBER')
    fig3 = px.bar(df3, x='DAY_OF_WEEK_NAME', y='COUNT', color='PUBLISHED_PERIOD', template= 'plotly_white')
    # fig3.update_traces(marker= dict(cornerradius="30%"))
    fig3.update_layout(title='Day of video publication',
                        xaxis_title='Day of week',
                        yaxis_title='Number of movies'
                       )

    #Chart 4
    fig4 = px.box(dff, x='CATEGORY_TITLE', y='VIDEO_TIME', template='plotly_white' )
    # fig4.update_traces( boxpoints='all', jitter=0.5,)
    fig4.update_layout(title='Statistics of video time',
                        xaxis_title='Category',
                        yaxis_title='Video time'
                       )

    return fig1, fig2, fig3, fig4



def data_filter(dff, chart1_state, chart3_state, chart4_state , trigger_id, slider_filter_state, dropdown_filter_state, state_data, is_month = False):
    
    dff = dff[(dff['VIDEO_TIME']>= slider_filter_state[0]) & (dff['VIDEO_TIME']<= slider_filter_state[1])]
    dff = dff[dff['CATEGORY_TITLE'].isin(dropdown_filter_state)]
    state_data = state_data if state_data is not None else {}

    if trigger_id is not None: #and trigger_id != 'reset-button':

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



@app.callback(
    Output('chart-1', 'figure'),
    Output('chart-2', 'figure'),
    Output('chart-3', 'figure'),
    Output('chart-4', 'figure'),
    Output('table-data', 'data'),
    Output('slider-filter', 'value'),
    Output('state-data', 'data'),
    Output('dropdown-filter', 'value'),
    
    Input('chart-1', 'clickData'),
    Input('chart-3', 'clickData'),
    Input('chart-4', 'clickData'),
    # Input('reset-button', 'n_clicks'),
    Input('master-data', 'data'),
    Input('slider-filter', 'value'),
    Input('dropdown-filter', 'value'),
    Input('state-data', 'data'),

    State('slider-filter', 'value'),
    State('dropdown-filter', 'value'),
    State('chart-1', 'clickData'),
    State('chart-3', 'clickData'),
    State('chart-4', 'clickData'),
)


def update_all(chart1_data, chart3_data, chart4_data, master_data, slider_filter, dropdown_filter, state_data, slider_filter_state, dropdown_filter_state, chart1_state, chart3_state, chart4_state ):

    triggered_id = ctx.triggered_id
    dff = pd.DataFrame(master_data)
    dff, state_data = data_filter(dff, chart1_state, chart3_state, chart4_state, triggered_id, slider_filter_state, dropdown_filter_state, state_data, True)
    figg1, figg2, figg3, figg4 = chart_bulilder(dff)
    filter_value = no_update
    filter2_value = no_update
    dff =  dff.to_dict('records')

    return figg1, figg2, figg3, figg4, dff, filter_value, state_data, filter2_value



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



### To do 
# Dodac 4 kafelki na środku ze stats: średni czas filmu, srednie like, średnie comentarze,  wyswietlenia 
# dodaj w filtrach kalendarz 
# chart1 - poprawić miesiace - żeby były wszysktie 
# zaokreąglone ramki chartów + białe tła wykresów z pojedynczymi paskami 
#charty - wyrazne tytuły lewy góy róg 
#szare tło + białe kafelki 


# 1) w funkcji chart_filter dodac w parametrach state_data 
# w poszczegolnych pozycjac sprawdzac stany np. State_data.get{}, jezeli rozne od 0 to korzystaj 
# 2) dodac zmiane system state w przypadku restetu! S 




#Linki w tablei 
# popraw wykresy 
# DONE -----------------wykres bubble resize jak?
# poprawy miesiace na wykres 1 
# poraw wykres box plot na kropki