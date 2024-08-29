from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd


df = pd.read_csv('data/dashboard_data/youtube_data_dashboard.csv')
#count po grupie peirod 
# grouped_df = df.groupby(['PUBLISHED_PERIOD']).size().reset_index(name='Count')
# fig = px.bar(grouped_df, x='PUBLISHED_PERIOD', y='Count')


external_stylesheets = [dbc.themes.COSMO]
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = dbc.Container([
    dcc.Store(id ='memory-output', data= [], storage_type='memory'),
    dbc.Row([
        html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div("One of three columns"),
            html.Div(
                dcc.RangeSlider(
                df['VIDEO_TIME'].min(),
                df['VIDEO_TIME'].max(),
                step=None,
                id='filter-minutes-slider',
                value=[df['VIDEO_TIME'].min(), df['VIDEO_TIME'].max()],
                # marks={str(year): str(year) for year in df['VIDEO_TIME'].unique()}
                )
            ),
            html.Div(id='my-first-graph', children=[])
            # dcc.Graph(id='my-first-graph')
        ], width=6),
        dbc.Col([ 
            html.Div("The second of three columns", className="text-center my-3"),
            html.Div(
                dcc.Dropdown(
                    options=["Avg. number of views", "Avg. number of likes", "Number of movies"],
                    value ="Number of movies",
                    id = "filter-dropdown"
                )
            ),
            html.Div(id='my-second-graph', children=[])
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('3 Chart'),
            dcc.Graph(id='my-third-graph')
        ],width=6),
        dbc.Col([
            html.Div('4 Chart'),
            dcc.Graph(id='my-fourth-graph')
        ],width=6)
    ])

], fluid=True)


@callback(
        Output('memory-output','data'),
        Input('filter-minutes-slider', 'value')
)

def filter_minutes(filter_minutes):
     dff = df[(df['VIDEO_TIME']>= filter_minutes[0]) & (df['VIDEO_TIME']<= filter_minutes[1])]
     return dff.to_dict('records')




##First chart
@callback(
    Output('my-first-graph', 'children'),
    Input('memory-output','data')
)
def update_graf(data):
    dff = pd.DataFrame(data)
    dff = dff.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
    fig = px.bar(dff, x= 'YEAR_MONTH', y= 'count')

    return dcc.Graph(figure= fig)  




# ##First chart
# @callback(
#     Output('my-first-graph', 'children'),
#     Input('crossfilter-year--slider', 'value')
# )
# def update_graf(crossfilter_year_slider):
#     dff = df[(df['VIDEO_TIME']>= crossfilter_year_slider[0]) & (df['VIDEO_TIME']<= crossfilter_year_slider[1])]
#     dff = dff.groupby(['YEAR_MONTH'])['YEAR_MONTH'].describe()['count'].reset_index().sort_values(by="YEAR_MONTH", ascending=True)
#     fig = px.bar(dff, x= 'YEAR_MONTH', y= 'count')

#     return dcc.Graph(figure= fig)  

# chart 2  

@callback(
    Output('my-second-graph', 'children'),
    Input('filter-dropdown', 'value'),
    Input('memory-output','data')
)
def update_second_graph(filter_dropdown, data ):
    df= pd.DataFrame(data)
    if filter_dropdown== 'Avg. number of views':
        dff = df.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": 'mean'}).reset_index().sort_values(by="VIEWCOUNT", ascending=False)
        fig = px.bar(dff,x= 'CATEGORY_TITLE', y= 'VIEWCOUNT')
    elif filter_dropdown== 'Avg. number of likes':
        dff = df.groupby(["CATEGORY_TITLE"]).aggregate({"LIKECOUNT": 'mean'}).reset_index().sort_values(by="LIKECOUNT", ascending=False)
        fig = px.bar(dff,x= 'CATEGORY_TITLE', y= 'LIKECOUNT')
    elif filter_dropdown== 'Number of movies':
        dff = df.groupby(['CATEGORY_TITLE'])['CATEGORY_TITLE'].describe()['count'].reset_index().sort_values(by="count", ascending=False)
        fig = px.bar(dff,x= 'CATEGORY_TITLE', y= 'count')

    return dcc.Graph(figure= fig)  

        






        
        
    
    # dff = 
    # df_group = df.groupby(["CATEGORY_TITLE"]).aggregate({"VIEWCOUNT": sum}).reset_index().sort_values(by="VIEWCOUNT", ascending=False)
    # df_group
    # px.bar(df_group, x ="CATEGORY_TITLE", y="VIEWCOUNT", )




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
    app.run(debug=True)