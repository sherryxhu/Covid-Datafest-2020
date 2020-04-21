import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd


# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

# data_file = "../waqi-covid19-airqualitydata-2020.csv"
data_file = "../US_AQI.csv"
df = pd.read_csv(data_file)
df['Date'] = df['Date'].astype('datetime64[ns]')
cities = sorted(df['City'].unique())
species = sorted(list(df['Specie'].unique()) + ['AQI'])


layout = html.Div([
    html.H1("Title",style={'textAlign': 'center'}),
    html.Br(),
    html.P("Description here"),
    html.Div([

        html.Div([
            html.H3(children='City'),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': i, 'value': i} for i in cities],
            ),
            html.Br(),
            html.H3(children='Specie'),
            dcc.Dropdown(
                id='specie-dropdown',
                options=[{'label': i, 'value': i} for i in species],
                multi=True
            ),
        ],
            style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Br(),
    html.Br(),
    dcc.Graph(id='indicator-graphic'),
])


@app.callback(
    [Output('specie-dropdown', 'options'),
     Output('specie-dropdown', 'value')],
    [Input('city-dropdown', 'value')])
def set_cities_options(city):
    dff = df[df['City'] == city]
    species = sorted(list(dff['Specie'].unique()) + ['AQI'])
    return ([{'label': i, 'value': i} for i in species], None)


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('specie-dropdown', 'value')])
def update_graph(city, specie):
    data = []
    if specie:
        for s in specie:
            if s != "AQI":
                dff = df[(df['City'] == city) & (df['Specie'] == s)].sort_values(by="Date")
                data.append(go.Scatter(
                    x=dff['Date'],
                    y=dff['median'],
                    name=s,
                    mode='lines+markers',
                    marker={
                        'size': 7,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                ))
            else:
                dff = df[(df['City'] == city)].drop_duplicates('AQI').sort_values(by="Date")
                data.append(go.Scatter(
                    x=dff['Date'],
                    y=dff['median'],
                    name=s,
                    mode='lines+markers',
                    marker={
                        'size': 7,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                ))

    def update_title(city, specie):
        if city and specie:
            return "{} {}".format(city, ", ".join(specie))
        return ""

    return {
        'data': data,
        'layout': dict(
            title=update_title(city, specie),
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
                type='date'
            )
        ),

    }

