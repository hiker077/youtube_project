from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL
import plotly.express as px
# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'
df = pd.read_csv('data/dashboard_data/youtube_data_dashboard.csv')
#count po grupie peirod 
# grouped_df = df.groupby(['PUBLISHED_PERIOD']).size().reset_index(name='Count')
# fig = px.bar(grouped_df, x='PUBLISHED_PERIOD', y='Count')


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

# FIRST_CHART = [
#     # dbc.CardHeader(html.H5("First chart", className="display-6 card-title")),
#     # dbc.CardBody(
#     #     [
#             dcc.Graph(id='first-graph')
#     #     ]
#     # )
# ]




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
                            # dbc.Col(dbc.Card(FIRST_CHART)),
                            # dbc.Col(dcc.Graph(id={'type': 'graph', 'index': 'first'},config={"displayModeBar": False}), md=6),
                            # dbc.Col(dcc.Graph(id={'type': 'graph', 'index': 'second'},config={"displayModeBar": False}), md=6)
                            dbc.Col(dcc.Graph(id='graph1',config={"displayModeBar": True}), md=6),
                            dbc.Col(dcc.Graph(id='graph2',config={"displayModeBar": False}), md=6)
                        ]
                            ),
                    dbc.Row(
                            [
                            # dbc.Col(dcc.Graph(id={'type': 'graph', 'index': 'third'},config={"displayModeBar": False}), md=6),
                            # dbc.Col(dcc.Graph(id={'type': 'graph', 'index': 'fourth'},config={"displayModeBar": False}), md=6)
                            dbc.Col(dcc.Graph(id='graph3',config={"displayModeBar": False}), md=6),
                            dbc.Col(dcc.Graph(id='graph4',config={"displayModeBar": False}), md=6)
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
    df1 = dff.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
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




@app.callback(
    # Output({'type': 'graph', 'index': ALL}, 'figure'),
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),

    Input('filter-minutes-slider', 'value'),
    Input('dropdown-filter', 'value'),
    Input('graph1', 'clickData'),
    Input('reset-button', 'n_clicks')
    # Input({'type': 'graph', 'index': ALL}, 'selectedData')
)

def update_all(filter_minutes, filter_dropdown, clickData, n_clicks):
    # dff = filter_data(df, filter_minutes, filter_dropdown, charts_data)
    triggered_id = ctx.triggered_id
    print(triggered_id)

    if triggered_id=='graph1':
        try:
            month = clickData['points'][0]['x']
            month = pd.to_datetime(month).strftime('%Y-%m')
            dff = df[df['YEAR_MONTH'] == month]
            figg1, figg2, figg3, figg4 = chart_funtion(dff)
        except Exception as e:
            print(f"Error parsing month: {e}")
            figg1, figg2, figg3, figg4 = chart_funtion(df)
    elif triggered_id=='reset-button':
        figg1, figg2, figg3, figg4 = chart_funtion(df)
    else:
        figg1, figg2, figg3, figg4 = chart_funtion(df)
    
    return figg1, figg2, figg3, figg4



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
