from dash import Dash, html, dcc, callback, Output, Input, State, dash_table, MATCH, ALL
import plotly.express as px
# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime

YOUTUBE_LOGO ='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'
df = pd.read_csv('data/dashboard_data/youtube_data_dashboard.csv')
#count po grupie peirod 
# grouped_df = df.groupby(['PUBLISHED_PERIOD']).size().reset_index(name='Count')
# fig = px.bar(grouped_df, x='PUBLISHED_PERIOD', y='Count')

# len(df)   df['VIEWCOUNT'].mean()  df['COMMENTCOUNT'].mean() df['LIKECOUNT'].mean()

# print( 'https://www.youtube.com/watch?v=' + df['VIDEOID'])

test = [ f'[{title}]({link})' for title, link in zip(df['TITLE'], ('https://www.youtube.com/watch?v=' + df['VIDEOID'])) ]
        

print([{'name': 'TITLE', 'id': 'TITLE', 'presentation': 'markdown'},{'name': i, 'id': i} for i in ['VIEWCOUNT', 'LIKECOUNT', 'COMMENTCOUNT', 'PUBLISHED_PERIOD', 'DAY_OF_WEEK_NAME', 'CATEGORY_TITLE']])

