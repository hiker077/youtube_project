import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample Data
df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Values": [10, 20, 30, 40]
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id='scatter-chart'),
    dcc.Graph(id='bar-chart')
])

# Callback to update the bar chart based on scatter chart selection
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('scatter-chart', 'clickData')]
)
def update_bar_chart(clickData):
    if clickData is None:
        filtered_df = df
    else:
        selected_category = clickData['points'][0]['x']
        filtered_df = df[df['Category'] == selected_category]

    fig = px.bar(filtered_df, x='Category', y='Values')
    return fig

# Initial scatter chart
app.layout.children[0].figure = px.scatter(df, x='Category', y='Values')


if __name__ == '__main__':
    app.run_server(debug=True)

