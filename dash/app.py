import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data_file = "../waqi-covid19-airqualitydata-2020.csv"
df = pd.read_csv(data_file)
df['Date'] = df['Date'].astype('datetime64[ns]')
cities = sorted(df['City'].unique())
species = sorted(df['Specie'].unique())

# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            html.H2(children='City'),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': i, 'value': i} for i in cities],
            ),
            html.H2(children='Specie'),
            dcc.Dropdown(
                id='specie-dropdown',
                options=[{'label': i, 'value': i} for i in species],
                multi=True
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        # html.Div([
            # dcc.Dropdown(
            #     id='yaxis-column',
            #     options=[{'label': i, 'value': i} for i in available_indicators],
            #     value='Life expectancy at birth, total (years)'
            # ),
            # dcc.RadioItems(
            #     id='yaxis-type',
            #     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #     value='Linear',
            #     labelStyle={'display': 'inline-block'}
            # )
        # ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    # dcc.Slider(
    #     id='year--slider',
    #     min=df['Year'].min(),
    #     max=df['Year'].max(),
    #     value=df['Year'].max(),
    #     marks={str(year): str(year) for year in df['Year'].unique()},
    #     step=None
    # )
])

@app.callback(
    Output('specie-dropdown', 'options'),
    [Input('city-dropdown', 'value')])
def set_cities_options(city):
    dff = df[(df['City'] == city)]
    species = sorted(dff['Specie'].unique())
    return [{'label': i, 'value': i} for i in species]

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('specie-dropdown', 'value')])
def update_graph(city,specie):
    data = []
    if specie:
        for s in specie:
            dff = df[(df['City'] == city) & (df['Specie'] == s)].sort_values(by="Date")
            data.append(dict(
                x=dff['Date'],
                y=dff['median'],
                name=s,
                mode='lines+markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            ))
    return {
        'data': data,
        'layout': dict(
            # xaxis={
            #     'title': xaxis_column_name,
            #     'type': 'linear' if xaxis_type == 'Linear' else 'log'
            # },
            # yaxis={
            #     'title': yaxis_column_name,
            #     'type': 'linear' if yaxis_type == 'Linear' else 'log'
            # },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)