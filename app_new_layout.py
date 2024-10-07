from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
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
                            dbc.Col(dcc.Graph(id='first-graph'), md=6),
                            dbc.Col(dcc.Graph(id='second-graph'), md=6)
                        ]
                            ),
                    dbc.Row(
                            [
                            dbc.Col(dcc.Graph(id='third-graph'), md=6),
                            dbc.Col(dcc.Graph(id='fourth-graph'), md=6)
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



##First Graph 
@app.callback(
    Output('first-graph', 'figure'),
    Input('filter-minutes-slider', 'value'),
    Input('dropdown-filter', 'value')
)
def update_graf1(filter_minutes, filter_dropdown):
    df1 = filter_data(df, filter_minutes, filter_dropdown)
    df1 = df.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
    fig1 = px.line(df1, x= 'YEAR_MONTH', y= 'count', markers=True)
    return fig1


##Second Graph


@callback(
   Output('second-graph', 'figure'),
   Input('filter-minutes-slider', 'value'),
   Input('dropdown-filter', 'value')
)
def update_graf2(filter_minutes, filter_dropdown):
    # dff = df[(df['VIDEO_TIME']>= filter_minutes[0]) & (df['VIDEO_TIME']<= filter_minutes[1])]
    df2 = filter_data(df, filter_minutes, filter_dropdown)
    df2 = df2.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": 'mean',"LIKECOUNT": ['mean', 'count']}).reset_index()
    df2.columns = ['_'.join(col).strip('_') for col in df2.columns]
    fig2 = px.scatter(df2, x = 'VIEWCOUNT_mean', y= 'LIKECOUNT_mean',size= 'LIKECOUNT_count', color='CATEGORY_TITLE')
    
    return fig2


##Third Graph 


@callback(
    Output('third-graph', 'figure'),
    Input('filter-minutes-slider', 'value'),
    Input('dropdown-filter', 'value')
)

def update_graf3(filter_minutes, filter_dropdown):
    df3 = filter_data(df, filter_minutes, filter_dropdown)
    df3 = df3.groupby(['DAY_OF_WEEK_NAME','PUBLISHED_PERIOD']).size().reset_index(name='COUNT')
    fig3 = px.bar(df3, x='DAY_OF_WEEK_NAME', y='COUNT', color='PUBLISHED_PERIOD')

    return fig3

#fourth chart
@callback(
    Output('fourth-graph', 'figure'),
    Input('filter-minutes-slider', 'value'),
    Input('dropdown-filter', 'value')
)

def update_graf4(filter_minutes, filter_dropdown):
    df4 = filter_data(df, filter_minutes, filter_dropdown)
    fig4 = px.box(df4, x='CATEGORY_TITLE', y='VIDEO_TIME')
    return fig4


#table data 
@callback(
    Output('table-data', 'data'),
    Input('filter-minutes-slider', 'value'),
    Input('dropdown-filter', 'value')
)

def update_table(filter_minutes, filter_dropdown):
    df_table = filter_data(df, filter_minutes, filter_dropdown)
    df_table=df_table.to_dict('records')
    return df_table






def filter_data(df, filter1, filter2, *charts_data):
    if filter1[0] or filter1[1]:
        df = df[(df['VIDEO_TIME']>= filter1[0]) & (df['VIDEO_TIME']<= filter1[1])]

    if filter2:
        df = df[df['CATEGORY_TITLE'].isin(filter2)]
    
    return df



#  if filter_dropdown== 'Avg. number of views':
#         dff2 = dff.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": 'mean'}).reset_index().sort_values(by="VIEWCOUNT", ascending=False)
#         ##box plot 
#         fig2 = px.bar(dff2,x= 'CATEGORY_TITLE', y= 'VIEWCOUNT')
#     elif filter_dropdown== 'Avg. number of likes':
#         ##boxplot 
#         dff2 = dff.groupby(["CATEGORY_TITLE"]).aggregate({"LIKECOUNT": 'mean'}).reset_index().sort_values(by="LIKECOUNT", ascending=False)
#         fig2 = px.bar(dff2,x= 'CATEGORY_TITLE', y= 'LIKECOUNT')
#     elif filter_dropdown== 'Number of movies':
#         dff2 = dff.groupby(['CATEGORY_TITLE'])['CATEGORY_TITLE'].describe()['count'].reset_index().sort_values(by="count", ascending=False)
#         fig2 = px.bar(dff2,x= 'CATEGORY_TITLE', y= 'count')


#Third Graph


#     dff3 = dff.groupby(['DAY_OF_WEEK_NAME','PUBLISHED_PERIOD']).size().reset_index(name='COUNT')
#     fig3 = px.bar(dff3, x='DAY_OF_WEEK_NAME', y='COUNT', color='PUBLISHED_PERIOD')




# app.layout = dbc.Container([
#     dcc.Store(id ='memory-output', data= [], storage_type='memory'),
#     dbc.Row([
#         html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
#     ]),
#     dbc.Row([
#         dbc.Col([
#             html.Div("One of three columns"),
#             html.Div(
#                 dcc.RangeSlider(
#                 min=df['VIDEO_TIME'].min(),
#                 max=df['VIDEO_TIME'].max(),
#                 step=None,
#                 id='filter-minutes-slider',
#                 value=[df['VIDEO_TIME'].min(), df['VIDEO_TIME'].max()],
#                 # marks={str(year): str(year) for year in df['VIDEO_TIME'].unique()}
#                 )
#             ),
#             html.Div(id='my-first-graph', children=[])
#             # dcc.Graph(id='my-first-graph')
#         ], width=6),
#         dbc.Col([ 
#             html.Div("The second of three columns", className="text-center my-3"),
#             html.Div(
#                 dcc.Dropdown(
#                     options=["Avg. number of views", "Avg. number of likes", "Number of movies"],
#                     value ="Number of movies",
#                     id = "filter-dropdown"
#                 )
#             ),
#             html.Div(id='my-second-graph', children=[])
#         ], width=6)
#     ]),
#     dbc.Row([
#         dbc.Col([
#             html.Div('3 Chart'),
#             html.Div(id='my-third-graph', children=[])
#         ],width=6),
#         dbc.Col([
#             html.Div('4 Chart'),
#             html.Div(id='my-fourth-graph', children=[])
#         ],width=6)
#     ]),
#     dbc.Row(
#         html.Div(
#             dash_table.DataTable(
#                 id='table-row-data',
#                 columns=[{'name': i, 'id': i} for i in df.columns],
#                 data=df.to_dict('records')
#                 )
#         )
#     )

# ], fluid=True)




# @callback(
#         Output('memory-output','data'),
#         Input('filter-minutes-slider', 'value'),

# )

# def filter_minutes(filter_minutes):
#      dff = df[(df['VIDEO_TIME']>= filter_minutes[0]) & (df['VIDEO_TIME']<= filter_minutes[1])]
#      return dff.to_dict('records')




# ##First chart
# @callback(
#     Output('my-first-graph', 'children'),
#     Output('my-second-graph', 'children'),
#     Output('my-third-graph', 'children'),
#     Output('my-fourth-graph', 'children'),
#     Output('table-row-data', 'data'),
    
#     Input('memory-output','data'),
#     Input('filter-dropdown', 'value')
# )
# def update_graf(data, filter_dropdown):
#     dff = pd.DataFrame(data)

#     ##First chart 
#     dff1 = dff.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
#     fig1 = px.line(dff1, x= 'YEAR_MONTH', y= 'count', markers=True)

#     ##Second chart 
#     if filter_dropdown== 'Avg. number of views':
#         dff2 = dff.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": 'mean'}).reset_index().sort_values(by="VIEWCOUNT", ascending=False)
#         ##box plot 
#         fig2 = px.bar(dff2,x= 'CATEGORY_TITLE', y= 'VIEWCOUNT')
#     elif filter_dropdown== 'Avg. number of likes':
#         ##boxplot 
#         dff2 = dff.groupby(["CATEGORY_TITLE"]).aggregate({"LIKECOUNT": 'mean'}).reset_index().sort_values(by="LIKECOUNT", ascending=False)
#         fig2 = px.bar(dff2,x= 'CATEGORY_TITLE', y= 'LIKECOUNT')
#     elif filter_dropdown== 'Number of movies':
#         dff2 = dff.groupby(['CATEGORY_TITLE'])['CATEGORY_TITLE'].describe()['count'].reset_index().sort_values(by="count", ascending=False)
#         fig2 = px.bar(dff2,x= 'CATEGORY_TITLE', y= 'count')
#     ##Third chart

#     dff3 = dff.groupby(['DAY_OF_WEEK_NAME','PUBLISHED_PERIOD']).size().reset_index(name='COUNT')
#     fig3 = px.bar(dff3, x='DAY_OF_WEEK_NAME', y='COUNT', color='PUBLISHED_PERIOD')

#     ##Forth chart was impelemnted 
#     fig4 = px.box(dff, x='CATEGORY_TITLE', y='VIDEO_TIME')


#     return dcc.Graph(figure= fig1), dcc.Graph(figure= fig2), dcc.Graph(figure= fig3), dcc.Graph(figure= fig4), dff.to_dict('records')













##https://dash-example-index.herokuapp.com/

# insporacja: 
# https://mahmoud2227.pythonanywhere.com/

### Next time 
# @callback(
#     Output(component_id='my-first-graph-final', component_property='figure'),
#     Input(component_id='radio-buttons-final', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#     return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
