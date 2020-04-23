import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app
df = pd.read_csv("../data/COVID-19-data-pop-lat-lng-changepoints.csv")
df = df[df['Country']=="US"]
df['text'] = df['City'] + '<br>Change Date for ' + df['Specie'] + ':<br>' + df['Date']
# colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
fig = go.Figure()
date_format = "%Y-%m-%d"
current_date = datetime.strptime('2020-04-22', date_format)
df['current_date'] = current_date
df['Date'] = df['Date'].astype('datetime64[ns]')
df['size'] = (df['current_date'] - df['Date']).astype('timedelta64[D]')

species = df['Specie'].unique()
for s in species:
    dff = df[df['Specie']==s]
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = dff['lng'],
        lat = dff['lat'],
        text = dff['text'],
        marker = dict(
            size = dff['size']*10,
            # color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = s))

fig.update_layout(
        title_text='USA Changepoints',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)',
        ),
    )

layout = html.Div([
    html.H1("Map Analysis", style={'textAlign': 'center'}),
    html.Br(),
    html.P("Compare change dates and lockdown dates across the US and China."),
    dcc.Graph(id='map-graphic', figure=fig),
])

#
# @app.callback(
#     Output('map-graphic', 'figure'),
#     [Input('multiple-city-dropdown', 'value'),
#      Input('multiple-specie-dropdown', 'value')])
# def update_graph(cities, specie):
#     data = []
#     if cities and specie:
#         for c in cities: # change this to cities
#             if specie != "AQI":
#                 dff = df[(df['City'] == c) & (df['Specie'] == specie)].sort_values(by="Date")
#                 data.append(go.Scatter(
#                     x=dff['Date'],
#                     y=dff['median'],
#                     name=c,
#                     mode='lines+markers',
#                     marker={
#                         'size': 7,
#                         'opacity': 0.5,
#                         'line': {'width': 0.5, 'color': 'white'}
#                     }
#                 ))
#             else:
#                 dff = df[(df['City'] == c)].drop_duplicates('Date').sort_values(by="Date")
#                 data.append(go.Scatter(
#                     x=dff['Date'],
#                     y=dff['AQI'],
#                     name=c,
#                     mode='lines+markers',
#                     marker={
#                         'size': 7,
#                         'opacity': 0.5,
#                         'line': {'width': 0.5, 'color': 'white'}
#                     }
#                 ))
#
#     def update_title(cities, specie):
#         if cities and specie:
#             return "{} {}".format(specie, ", ".join(cities))
#         return ""
#
#     return {
#         'data': data,
#         'layout': dict(
#             title=update_title(cities, specie),
#             margin={'l': 40, 'b': 40, 't': 100, 'r': 40},
#             xaxis=dict(
#                 autorange=True,
#                 rangeselector=dict(
#                     buttons=list([
#                         dict(count=1,
#                              label='1m',
#                              step='month',
#                              stepmode='backward'),
#                         dict(count=7,
#                              label='7d',
#                              step='day',
#                              stepmode='backward'),
#                         dict(count=1,
#                              label='1d',
#                              step='day',
#                              stepmode='backward'),
#                         dict(step='all')
#                     ])
#                 ),
#                 rangeslider=dict(
#                     visible=True
#                 ),
#                 type='date'
#             )
#         ),
#
#     }
#
