import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd


layout = html.Div([
    html.H1("Lockdown Analysis", style={'textAlign': 'center'}),
    html.Br(),
    html.P("Compare point change dates across the US. A point change is defined as the time at which the typical pattern was broken. The larger the bubble, the earlier it changed."),
    # dcc.Graph(id='map-graphic', figure=fig),
])
