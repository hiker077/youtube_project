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
    dbc.Row([
        html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div("One of three columns"),
            dcc.Graph(id='my-first-graph')
            ], width=6),
        dbc.Col([ 
            html.Div("The second of three columns", className="text-center my-3"),
            dcc.Graph(id='my-second-graph')
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