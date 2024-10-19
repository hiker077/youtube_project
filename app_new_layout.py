from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL, State, no_update
import plotly.express as px
# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'
df = pd.read_csv('data/dashboard_data/youtube_data_dashboard.csv')


external_stylesheets = [dbc.themes.COSMO]



NAVBAR = dbc.Navbar(
    children=[
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(html.Img(src=YOUTUBE_LOGO, height="60px")),
                dbc.Col("Dashboad"),
                dbc.Col("Repository")
            ],
            align="center"
        )
    ],
    color="gray",
    dark=True,
    sticky="top",
)


FILTER_CARD =[
    dbc.CardHeader(html.H5("Filters", className="display-6 card-title")),
    dbc.CardBody(
        [
        dbc.Row(
            [
            dbc.Col(
                [
                    html.Div(dcc.Store(id='output-data',data= df.to_dict('records'))),
                    # html.Div(dcc.Store(id='state-data', data= {'State': 1})),
                    html.Div(dcc.Store(id='state-data')),
                    html.Button("Reset Selection", id='reset-button', n_clicks=0),
                    html.Div("Duration of video (minutes)"),
                    html.Div(
                        dcc.RangeSlider(
                        min=df['VIDEO_TIME'].min(),
                        max=df['VIDEO_TIME'].max(),
                        step=50,
                        id='filter-minutes-slider',
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
            dbc.Col(dbc.Card(FILTER_CARD, color='light') , md=2),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='chart-1',config={"displayModeBar": False}), md=6),
                            dbc.Col(dcc.Graph(id='chart-2',config={"displayModeBar": False}), md=6)
                        ]
                            ),
                    dbc.Row(
                            [
                            dbc.Col(dcc.Graph(id='chart-3',config={"displayModeBar": False}), md=6),
                            dbc.Col(dcc.Graph(id='chart-4',config={"displayModeBar": False}), md=6)
                            ]
                             )
                ],
                md=10
            )
        ],
         style={"marginTop": 30}
    ),
    dbc.Row(
        html.Div(
            dash_table.DataTable(
                id='table-data',
                # columns=[{'name': i, 'id': i} for i in df.columns],
                columns=[{'name': i, 'id': i} for i in ['TITLE', 'VIEWCOUNT', 'LIKECOUNT', 'COMMENTCOUNT', 'PUBLISHED_PERIOD', 'DAY_OF_WEEK_NAME', 'CATEGORY_TITLE']],
                page_size=50
                # data=df.to_dict('records')
                )
        )
    )

    ],fluid=True

)



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[NAVBAR, BODY])



def chart_funtion(dff):
    ## Chart 1 
    # df1 = dff.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
    df1 = dff.groupby('YEAR_MONTH')['YEAR_MONTH'].count().reset_index(name='count').sort_values(by="YEAR_MONTH", ascending=True)
    fig1 = px.line(df1, x= 'YEAR_MONTH', y= 'count', markers=True)

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


def filters_data(df, minutes_filter): #, dropdown_filter):
    
    dff = df
    if minutes_filter:
        dff = dff[(dff['VIDEO_TIME']>= minutes_filter[0]) & (dff['VIDEO_TIME']<= minutes_filter[1])]
    # elif dropdown_filter:
    #     dff = 
    else: 
        dff = df

    return dff





def chart_filter(df, chart1_state, chart3_state, chart4_state , trigger_id, filter_1, state_data, is_month = False):
    

    dff = df
    dff = dff[(dff['VIDEO_TIME']>= filter_1[0]) & (dff['VIDEO_TIME']<= filter_1[1])]
    state_data = state_data if state_data is not None else {}

    if trigger_id is not None and trigger_id != 'reset-button':
        state_data[trigger_id] = True

        if chart1_state is not None and state_data.get('chart-1'):
            chart1_state = chart1_state['points'][0]['x']
            month = pd.to_datetime(chart1_state).strftime('%Y-%m')
            dff = dff[dff['YEAR_MONTH']==month]
        
        if chart3_state is not None and state_data.get('chart-3'):
            chart3_state = chart3_state['points'][0]['x']
            dff = dff[dff['DAY_OF_WEEK_NAME']==chart3_state]

        if chart4_state is not None and state_data.get('chart-4'):
            chart4_state = chart4_state['points'][0]['x']
            dff = dff[dff['CATEGORY_TITLE']==chart4_state]
    else:
        state_data = {}


    print(state_data)
    
    # if is_month:
    #     month = pd.to_datetime(chart_clickdata).strftime('%Y-%m')

    # if trigger_id=='chart-1':
    #     dff = dff[dff['YEAR_MONTH']==month]
    # elif trigger_id=='chart-3':
    #     dff = dff[dff['DAY_OF_WEEK_NAME']==chart_clickdata]
    # elif trigger_id=='chart-4':
    #     dff = dff[dff['CATEGORY_TITLE']==chart_clickdata]
    # else: 
        # dff

    # figg1, figg2, figg3, figg4 = chart_funtion(dff)
 
    return dff, state_data



@app.callback(
    Output('chart-1', 'figure'),
    Output('chart-2', 'figure'),
    Output('chart-3', 'figure'),
    Output('chart-4', 'figure'),
    Output('table-data', 'data'),
    Output('filter-minutes-slider', 'value'),
    Output('state-data', 'data'),
    
    Input('chart-1', 'clickData'),
    Input('chart-3', 'clickData'),
    Input('chart-4', 'clickData'),
    Input('reset-button', 'n_clicks'),
    Input('output-data', 'data'),
    Input('filter-minutes-slider', 'value'),
    Input('dropdown-filter', 'value'),
    Input('state-data', 'data'),

    State('filter-minutes-slider', 'value'),
    State('chart-1', 'clickData'),
    State('chart-3', 'clickData'),
    State('chart-4', 'clickData'),
)

def update_all(chart1_data, chart3_data, chart4_data, rest_button, store_data, minutes_filter, dropdown_filter,state_data, state_of_slider, chart1_state, chart3_state, chart4_state ):

    triggered_id = ctx.triggered_id
    dff = pd.DataFrame(store_data)
    # print(chart1_state)
    # print(chart3_state)
    # print(chart4_state)

  



    # if triggered_id=='chart-1':
    #     try:
    #         dff = chart_filter(dff, chart1_data, triggered_id,state_of_slider,  True)
    #         figg1, figg2, figg3, figg4 = chart_funtion(dff)
    #         filter_value = no_update
    #         state_data = {'State': '1' }
    #     except Exception as e:
    #         print(f"Error parsing month: {e}")
    #         dff = chart_filter(dff, chart1_data, triggered_id, state_of_slider, True)
    #         figg1, figg2, figg3, figg4 = chart_funtion(dff)
    #         filter_value = no_update
    #         state_data = no_update
    # elif triggered_id=='chart-3':
    #     dff = chart_filter(dff, chart3_data, triggered_id, state_of_slider)
    #     figg1, figg2, figg3, figg4 = chart_funtion(dff)
    #     filter_value = no_update
    #     state_data = no_update
    # elif triggered_id=='chart-4':
    #     dff = chart_filter(dff, chart4_data, triggered_id, state_of_slider)
    #     figg1, figg2, figg3, figg4 = chart_funtion(dff)
    #     filter_value = no_update
    #     state_data = no_update
    # elif triggered_id=='reset-button':
    #     figg1, figg2, figg3, figg4 = chart_funtion(dff)
    #     filter_value = no_update
    #     state_data = None

    # else:
    #     # dff = df
    #     dff= chart_filter(dff, None ,triggered_id, state_of_slider)
    #     figg1, figg2, figg3, figg4 = chart_funtion(dff)
       
    #     filter_value = no_update
    #     state_data = state_data
    
    dff, state_data = chart_filter(dff, chart1_state, chart3_state, chart4_state, triggered_id, state_of_slider, state_data,   True)
    figg1, figg2, figg3, figg4 = chart_funtion(dff)
    filter_value = no_update
    # state_data = no_update

    dff =  dff.to_dict('records')




    return figg1, figg2, figg3, figg4, dff, filter_value, state_data

























# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



### To do 
# 1) w funkcji chart_filter dodac w parametrach state_data 
# w poszczegolnych pozycjac sprawdzac stany np. State_data.get{}, jezeli rozne od 0 to korzystaj 
# 2) dodac zmiane system state w przypadku restetu! S 
