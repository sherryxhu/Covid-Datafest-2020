import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd


# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

data_file = "../data/airqualitydata-2019-2020.csv"
df = pd.read_csv(data_file)
df['Date'] = df['Date'].astype('datetime64[ns]')
cities_options = sorted(df['City'].unique())
# species_options = sorted(list(df['Specie'].unique()) + ['AQI'])
species_options = sorted(list(df['Specie'].unique()))


layout = html.Div([
    html.H1("Multiple City Analysis",style={'textAlign': 'center'}),
    html.Br(),
    html.P("Compare one statistic across several cities."),
    html.Div([

        html.Div([
            html.H3(children='Cities'),
            dcc.Dropdown(
                id='multiple-city-dropdown',
                options=[{'label': i, 'value': i} for i in cities_options],
                multi=True,
                placeholder= "Select a city...",
            ),
            html.Br(),
            html.H3(children='Specie'),
            dcc.Dropdown(
                id='multiple-specie-dropdown',
                options=[{'label': i, 'value': i} for i in species_options],
                placeholder= "Select a specie...",
            ),
        ],
            style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Br(),
    html.Br(),
    dcc.Graph(id='multiple-city-graphic'),
])


@app.callback(
    Output('multiple-specie-dropdown', 'options'),
    [Input('multiple-city-dropdown', 'value')])
def set_cities_options(cities):
    output = list()
    if cities:
        for c in cities:
            dff = df[df['City'] == c]
            species = list(dff['Specie'].unique())
            if len(output) == 0:
                output = species
            else:
                output = list(set(output) & set(species))
    # return [{'label': i, 'value': i} for i in sorted(list(output)+['AQI'])]
    return [{'label': i, 'value': i} for i in sorted(list(output))]


@app.callback(
    Output('multiple-city-graphic', 'figure'),
    [Input('multiple-city-dropdown', 'value'),
     Input('multiple-specie-dropdown', 'value')])
def update_graph(cities, specie):
    data = []
    colors = ['#ff00ff', '#00ff00','#9900ff','#0000ff','#ff6933','yellow','#ff0066']
    if cities and specie:
        for c,color in zip(cities,colors): # change this to cities
            if specie != "AQI":
                dff = df[(df['City'] == c) & (df['Specie'] == specie)].sort_values(by="Date")
                data.append(go.Scatter(
                    x=dff['Date'],
                    y=dff['median'],
                    name=c,
                    mode='lines+markers',
                    marker={
                        'size': 7,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    line = dict(
                        color = color
                    )
                ))
            else:
                dff = df[(df['City'] == c)].drop_duplicates('Date').sort_values(by="Date")
                data.append(go.Scatter(
                    x=dff['Date'],
                    y=dff['AQI'],
                    name=c,
                    mode='lines+markers',
                    marker={
                        'size': 7,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                ))

    def update_title(cities, specie):
        if cities and specie:
            return "{} {}".format(specie, ", ".join(cities))
        return ""

    return {
        'data': data,
        'layout': dict(
            title=update_title(cities, specie),
            margin={'l': 40, 'b': 40, 't': 100, 'r': 40},
            xaxis=dict(
                autorange=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=7,
                             label='7d',
                             step='day',
                             stepmode='backward'),
                        dict(count=1,
                             label='1d',
                             step='day',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            ),
            plot_bgcolor= '#cce6ff',
            paper_bgcolor = '#cce6ff'
        ),

    }

