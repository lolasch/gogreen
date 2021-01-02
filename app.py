# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options




app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Go Green',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Luftqualität während einer Pandemie.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
            dcc.RadioItems(        
            style={
                'textAlign': 'center',
                'color': colors['text']
            },    
            id="schadwert",
            options=[      
                {'label': 'CO', 'value': 'CO'},  
                {'label': 'NO', 'value': 'NO'},
                {'label': 'NO2', 'value': 'NO2'},
                {'label': 'NOx', 'value': 'NOx'},
                {'label': 'O3', 'value': 'O3'},
                {'label': 'PM10', 'value': 'PM10'},
                {'label': 'SO2', 'value': 'SO2'}
            ],
            value='NO',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.RadioItems(
            style={
                'textAlign': 'center',
                'color': colors['text']
            }, 
            id="zeitabschnitt",
            options=[        
                {'label': 'Tage', 'value': 'Tag'},
                {'label': 'Woche', 'value': 'Woche'},
                {'label': 'Monat', 'value': 'Monat'}
            ],
            value='Tag',
            labelStyle={'display': 'inline-block'}
        ),
        html.Div(id='time'),    
    ], className="row")
])

@app.callback(Output('time', 'children'),
    [Input('zeitabschnitt', 'value'),
    Input('schadwert', 'value')])
def make_line_charts(value1, value2):
    if value1 == "Tag":
        quelle = pd.read_csv("./daten/"+ value2 + "Tag.csv")
        figure = px.line(quelle, x = "Datum", y="Durchschnitt", title="Tagesschnitt", color= "Ort")
    elif value1 == "Woche":
        quelle = pd.read_csv("./daten/"+ value2 + "Woche.csv")
        figure = px.line(quelle, x = "Wochennummer", y="Durchschnitt", title="Wochenschnitt", color= "Ort")
    else:
        quelle = pd.read_csv("./daten/"+ value2 + "Monat.csv")
        figure = px.line(quelle, x = "Monat", y="Durchschnitt", title="Monatsschnitt", color= "Ort")
    figure.update_xaxes(rangeslider_visible=True)

    fig2 = px.scatter_mapbox(quelle, lat="Lat", lon="Long", zoom=11, height=500, width=800, size="Durchschnitt", color= "Ort")
    fig2.update_layout(mapbox_style="open-street-map")
    fig2.update_layout(margin={"r":0,"t":0,"l":30,"b":0})

    return (
        html.Div([
                html.H3('Karte'),
                dcc.Graph(id='g1', figure=fig2)
            ], className="six columns"),

        html.Div([
            html.H3('Zeitlicher Verlauf'),

            html.Div(
                dcc.Graph(
                    id="zeitstrahl",
                    figure=figure
                )    
            )
        ],
        className="six columns")
    )
    

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
