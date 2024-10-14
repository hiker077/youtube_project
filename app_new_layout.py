from dash import Dash, html, dcc, callback, Output, Input, ctx, dash_table, MATCH, ALL
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
                    html.Div(dcc.Store(id='output-data', data= df.to_dict('records'))),
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



def filter_data(df, input_value, chart_name, is_month = False):
    
    input_value = input_value['points'][0]['x']

    if is_month:
        month = pd.to_datetime(input_value).strftime('%Y-%m')

    if chart_name=='chart-1':
        dff = df[df['YEAR_MONTH']==month]
    elif chart_name=='chart-3':
        dff = df[df['DAY_OF_WEEK_NAME']==input_value]
    elif chart_name=='chart-4':
        dff = df[df['CATEGORY_TITLE']==input_value]

    figg1, figg2, figg3, figg4 = chart_funtion(dff)
 
    return figg1, figg2, figg3, figg4 



@app.callback(

    Output('chart-1', 'figure'),
    Output('chart-2', 'figure'),
    Output('chart-3', 'figure'),
    Output('chart-4', 'figure'),
    Input('chart-1', 'clickData'),
    Input('chart-3', 'clickData'),
    Input('chart-4', 'clickData'),
    Input('reset-button', 'n_clicks'),
    Input('output-data', 'data')
)

def update_all(chart1_data, chart3_data, chart4_data, rest_button, store_data):

    triggered_id = ctx.triggered_id
    dff = pd.DataFrame(store_data)

    if triggered_id=='chart-1':
        try:
            figg1, figg2, figg3, figg4 = filter_data(dff, chart1_data, triggered_id, True)
        except Exception as e:
            print(f"Error parsing month: {e}")
            figg1, figg2, figg3, figg4 = filter_data(dff, chart1_data, triggered_id, True)
    elif triggered_id=='chart-2':
        figg1, figg2, figg3, figg4 = filter_data(dff, chart3_data, triggered_id)
    elif triggered_id=='chart-4':
        figg1, figg2, figg3, figg4 = filter_data(dff, chart4_data, triggered_id)
    elif triggered_id=='reset-button':
        figg1, figg2, figg3, figg4 = chart_funtion(df)
    else:
        figg1, figg2, figg3, figg4 = chart_funtion(df)
    
    return figg1, figg2, figg3, figg4


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
