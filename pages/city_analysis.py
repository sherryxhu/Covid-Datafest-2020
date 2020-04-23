import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

# data_file = "../waqi-covid19-airqualitydata-2020.csv"
data_file = "../data/airqualitydata-2019-2020.csv"
df = pd.read_csv(data_file)
df['Date'] = df['Date'].astype('datetime64[ns]')
cities = sorted(df['City'].unique())
# species = sorted(list(df['Specie'].unique()) + ['AQI'])
species = sorted(list(df['Specie'].unique()))

changepoint_file = '../data/changepoints.csv'
df_changepoint = pd.read_csv(changepoint_file)

layout = html.Div([
    html.H1("City Analysis", style={'textAlign': 'center'}),
    html.Br(),
    html.P("Examine different statistics for one city."),
    html.Div([

        html.Div([
            html.H3(children='City'),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': i, 'value': i} for i in cities],
                placeholder= "Select a city...",
            ),
            html.Br(),
            html.H3(children='Specie'),
            dcc.Dropdown(
                id='specie-dropdown',
                options=[{'label': i, 'value': i} for i in species],
                multi=True,
                placeholder= "Select a specie...",
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
    # species = sorted(list(dff['Specie'].unique()) + ['AQI'])
    species = sorted(list(dff['Specie'].unique()))
    return ([{'label': i, 'value': i} for i in species], None)


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('specie-dropdown', 'value')])
def update_graph(city, specie):
    data = []
    changepoint_dates = []
    colors = ['#ff00ff', '#00ff00','#9900ff','#0000ff','#ff6933']
    if city and specie:
        i = 0
        for s in specie:
            changepoint_dates += list(
                df_changepoint[(df_changepoint['City'] == city) & (df_changepoint['Specie'] == s)]['Date'].apply(
                    str))
    
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
                        'line': {'width': 0.5, 'color': 'blue'}
                    },
                    line=dict(
                        color=colors[i]
                    )
                ))
            else:
                dff = df[(df['City'] == city)].drop_duplicates('Date').sort_values(by="Date")
                data.append(go.Scatter(
                    x=dff['Date'],
                    y=dff['AQI'],
                    name=s,
                    mode='lines+markers',
                    marker={
                        'size': 7,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    line=dict(
                        color=colors[i]
                    )
                ))
            i += 1
            

    def update_title(city, specie):
        if city and specie:
            return "{} {}".format(city, ", ".join(specie))
        return ""

    shapes = [{
        'type': 'line',
        # x-reference is assigned to the x-values
        'xref': 'x',
        # y-reference is assigned to the plot paper [0,1]
        'yref': 'paper',
        'x0': d,
        'y0': 0,
        'x1': d,
        'y1': 1,
        'opacity': 0.3,
        'line': {
            'color': 'dark green',
            'width': 2,
        },
        'name': 'change point'
    } for d in changepoint_dates]
    return {
        'data': data,
        'layout': dict(
            title=update_title(city, specie),
            margin={'l': 40, 'b': 40, 't': 100, 'r': 40},
            shapes=shapes,
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
