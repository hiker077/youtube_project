from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'
df = pd.read_csv('data/dashboard_data/youtube_data_dashboard.csv')


external_stylesheets = [dbc.themes.COSMO]


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
    dbc.CardHeader(html.H5("Filters", className="display-6 card-title")),
    dbc.CardBody(
        [
        dbc.Row(
            [
            dbc.Col(
                [
                    html.Div(dcc.Store(id='master-data',data= df.to_dict('records'))),
                    # html.Div(dcc.Store(id='state-data', data= {'State': 1})),
                    html.Div(dcc.Store(id='state-data')),
                    html.Button("Reset Selection", id='reset-button', n_clicks=0),
                    html.Div("Duration of video (minutes)"),
                    html.Div(
                        dcc.RangeSlider(
                        min=df['VIDEO_TIME'].min(),
                        max=df['VIDEO_TIME'].max(),
                        step=50,
                        id='slider-filter',
                        value=[df['VIDEO_TIME'].min(), df['VIDEO_TIME'].max()],
                        )),
                    html.Div("Categories"),
                    html.Div(
                        dcc.Dropdown(
                        options= df['CATEGORY_TITLE'].unique(),
                        value= df['CATEGORY_TITLE'].unique(),
                        multi=True,
                        id= 'dropdown-filter'
                        )
                    )
                ]
            )]
        )]
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
                        html.Div(html.Img(src=YOUTUBE_LOGO, height="60px"))
                    ),
                    dbc.Row(
                        html.Div('Comment')
                    ),
                    dbc.Row(
                        [
                            dbc.Col('Button'),
                            dbc.Col('Button'),
                            dbc.Col('Button')
                        ]
                    ),
                    dbc.Row( dbc.Card(FILTER_CARD, color='light'))
                ],
                md=2
            ),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col('Stats', className='py-3 mx-3 my-5 w-5 border rounded-3'),
                            dbc.Col('Stats', className='bg-danger'),
                            dbc.Col('Stats', className='bg-danger'),
                            dbc.Col('Stats', className='bg-danger')
                        ],
                        className= 'bg-info  g-2 my-2'
                    
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='chart-1',config={"displayModeBar": False}) ),
                            dbc.Col(dcc.Graph(id='chart-2',config={"displayModeBar": False}) ),
                            dbc.Col(dcc.Graph(id='chart-3',config={"displayModeBar": False}) ),
                            dbc.Col(dcc.Graph(id='chart-4',config={"displayModeBar": False}))
                            ],
                            className= 'g-3 row-cols-2 my-2'
                             ),
                             
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
                md=10, className= 'my-3 border-danger'
            )
        ],
        #  style={"marginTop": 30}
        className='mb-4'
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




app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = html.Div(children=[NAVBAR, BODY])
app.layout = html.Div(children=[BODY])


def chart_bulilder(dff):
    ## Chart 1 
    # df1 = dff.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
    df1 = dff.groupby('YEAR_MONTH')['YEAR_MONTH'].count().reset_index(name='count').sort_values(by="YEAR_MONTH", ascending=True)
    fig1 = px.line(df1, x= 'YEAR_MONTH', y= 'count', markers=True, text= 'count')
    fig1.update_traces(textposition="top right", line=dict(color='firebrick', width=4))

    #Chart 2 
    df2 = dff.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": 'mean',"LIKECOUNT": ['mean', 'count']}).reset_index()
    df2.columns = ['_'.join(col).strip('_') for col in df2.columns]
    fig2 = px.scatter(df2, x = 'VIEWCOUNT_mean', y= 'LIKECOUNT_mean',size= 'LIKECOUNT_count', color='CATEGORY_TITLE')

    #Chart 3 
    df3 = dff.groupby(['DAY_OF_WEEK_NAME','PUBLISHED_PERIOD']).size().reset_index(name='COUNT')
    fig3 = px.bar(df3, x='DAY_OF_WEEK_NAME', y='COUNT', color='PUBLISHED_PERIOD')

    #Chart 4
    fig4 = px.box(dff, x='CATEGORY_TITLE', y='VIDEO_TIME')

    return fig1, fig2, fig3, fig4



def data_filter(dff, chart1_state, chart3_state, chart4_state , trigger_id, slider_filter_state, dropdown_filter_state, state_data, is_month = False):
    
    dff = dff[(dff['VIDEO_TIME']>= slider_filter_state[0]) & (dff['VIDEO_TIME']<= slider_filter_state[1])]
    dff = dff[dff['CATEGORY_TITLE'].isin(dropdown_filter_state)]
    state_data = state_data if state_data is not None else {}

    if trigger_id is not None and trigger_id != 'reset-button':

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
    Input('reset-button', 'n_clicks'),
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


def update_all(chart1_data, chart3_data, chart4_data, rest_button, master_data, slider_filter, dropdown_filter, state_data, slider_filter_state, dropdown_filter_state, chart1_state, chart3_state, chart4_state ):

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
