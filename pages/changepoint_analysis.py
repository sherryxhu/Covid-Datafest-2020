import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_table

import pandas as pd

fig1_options = ['Change Points that Occur Before Lockdown',
                'Change Points that Occur After Lockdown']

fig1_y = [71,35]

fig1 = go.Figure([go.Bar(x=fig1_options,y=fig1_y)])
fig1.update_layout(title='Change Point Dates Compared to Lockdown Dates')

df = pd.read_csv('data/table.csv')


fig2_labels = ['no2','co','o3','pm25','pm10','so2']
fig2_values = [12,8,3,7,1,4]
fig2 = go.Figure(data=[go.Pie(labels=fig2_labels, values=fig2_values)])
fig2.update_layout(title="Change Points After Lockdown")

layout = html.Div([
    html.H1("China: Change Point Analysis", style={'textAlign': 'center'}),
    html.Br(),
    html.P(""),
    dcc.Graph(id='bar-graphic', figure=fig1),
    html.Br(),
    html.H6("Number of Days Between Change Points and Lockdown (for Change Points that Occur After Lockdown)"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_table={
            'maxWidth': '500px',
        }
    ),
    html.Br(),
    dcc.Graph(id='pie-graphic', figure=fig2)
])

