# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date
import calendar
import datetime
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Go Green'

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

    html.Div(
        style={
                'display' : 'block',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'text-align': 'center'
        },children = [   

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
            value='NO2',
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
        dcc.DatePickerRange(
            style={
                'color': colors['text']
            },  
            id='datepicker',
            min_date_allowed=date(2019, 4, 1),
            max_date_allowed=date(2020, 11, 30),
            initial_visible_month=date(2019, 4, 1),
            start_date=date(2019, 4, 1),
            end_date=date(2020, 11, 30)
        ),
        html.Div(id='time'), 

    ], className="row")  
])

@app.callback(Output('time', 'children'),
    [Input('zeitabschnitt', 'value'),
    Input('schadwert', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date')])
def make_line_charts(zeit, schadstoff, start_date, end_date):
    filtern(schadstoff, start_date, end_date)
    verlaufBerechnen(zeit)

    if zeit == "Tag":
        quelle = pd.read_csv("./daten/"+ schadstoff + "Tag.csv")
        zeitstrahl = px.line(quelle, x = "Datum", y="Durchschnitt", title="Tagesschnitt", color= "Ort")
        mitteTag = pd.read_csv("./daten/verlaufTag.csv")
        zeitverlauf = px.line(mitteTag, x="Uhrzeit", y="Wert", color="Ort", title = "Durchschnittliche tägliche Luftbelastung vom " + start_date +" bis " + end_date)
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSort.csv")
    elif zeit == "Woche":
        quelle = pd.read_csv("./daten/"+ schadstoff + "Woche.csv")
        zeitstrahl = px.line(quelle, x = "Wochenbeginn", y="Durchschnitt", title="Wochenschnitt", color= "Ort")
        mitteWoche = pd.read_csv("./daten/verlaufWoche.csv")
        zeitverlauf = px.line(mitteWoche, x="Wochentag", y="Wert", color="Ort", title = "Durchschnittliche wöchentliche Luftbelastung im Zeitraum " + start_date +" bis " + end_date)
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSortWoche.csv")
    else:
        quelle = pd.read_csv("./daten/"+ schadstoff + "Monat.csv")
        zeitstrahl = px.line(quelle, x = "Monat", y="Durchschnitt", title="Monatsschnitt", color= "Ort")
        mitteMonat = pd.read_csv("./daten/verlaufMonat.csv")
        zeitverlauf = px.line(mitteMonat, x="Tag", y="Wert", color="Ort", title = "Durchschnittliche monatliche Luftbelastung im Zeitraum " + start_date +" bis " + end_date)
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSortWoche.csv")
    zeitstrahl.update_layout(xaxis_range=[start_date,end_date])
    zeitstrahl.update_layout(height=300,margin={"r":0,"t":30,"l":30,"b":0},title_x=0.5)
    zeitverlauf.update_layout(height=300,margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)
    corona = make_subplots(specs=[[{"secondary_y": True}]])
    corona.add_trace(
        go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Faelle, name="yaxis data"),
        secondary_y=False,
    )
    corona.add_trace(
        go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Tote, name="yaxis2 data"),secondary_y=True,
    )

    corona.update_layout(title_text="Corona-Inzidenzzahlen",showlegend=False,height=300,margin={"r":0,"t":40,"l":0,"b":0},title_x=0.5)
    corona.update_xaxes(title_text="Zeit")
    corona.update_yaxes(title_text="<b>Fallzahlen</b>", secondary_y=False, title_font=dict(color="red"))
    corona.update_yaxes(title_text="<b>Tote</b>", secondary_y=True,title_font=dict(color="blue"))
    #corona.update_layout(xaxis_range=[start_date,end_date])

    karte = px.scatter_mapbox(quelle, lat="Lat", lon="Long", zoom=11, height=300, width=800, color= "Ort", size = "Durchschnitt")
    karte.update_layout(mapbox_style="open-street-map",showlegend=False)
    karte.update_layout(margin={"r":0,"t":0,"l":30,"b":0})


    return (
        html.Div([
                html.H3('Karte'),
                html.Div(
                    dcc.Graph(id='g1', figure=karte)
                ),

                html.Div(
                    dcc.Graph(
                        id="corona",
                        figure=corona
                )    
            )], className="six columns"),

        html.Div([
            html.H3('Zeitlicher Verlauf'),

            html.Div(
                dcc.Graph(
                    id="zeitstrahl",
                    figure=zeitstrahl
                )    
            ),
            html.Div(
                dcc.Graph(
                    id="zeitverlauf",
                    figure=zeitverlauf
                )    
            )
        ],
        className="six columns")
    )
    
def verlaufBerechnen(zeitabschnitt):
    #Die Funktion berechnet den Tages-Wochen-Monatsdurschnitt für den jeweilgen Zeitraum
    #
    if zeitabschnitt == "Tag":
        with open("./daten/gefiltert.csv") as file:
            tagout = open("./daten/verlaufTag.csv", "w")
            tagout.write("Lat,Long,Ort,Uhrzeit,Wert\n")
            next(file)
            dic = {}
            for lines in file:
                lines = lines.strip()
                linie = lines.split(",")
                lat = linie[0]
                lon = linie[1]
                ort = linie[2]
                datum = linie[3]
                uhrzeit = datum.split(" ")[1]
                wert = linie[4]
                if wert != "NA":
                    wert = float(wert)
                    if (lat,lon,ort, uhrzeit) in dic:
                        values = dic[(lat,lon,ort,uhrzeit)]
                        values[0] += wert
                        values[1] += 1
                        dic[(lat,lon,ort,uhrzeit)] = values
                    else:
                        dic[(lat,lon,ort,uhrzeit)] = [wert, 1]
        for ele in sorted(dic):
            values = dic[ele]
            avg = values[0] / values[1]
            tagout.write(str(ele[0]) + "," + str(ele[1]) + "," + str(ele[2]) + "," + str(ele[3]) + "," + "%.3f" %avg + "\n")
            
    elif zeitabschnitt == "Woche":
         with open("./daten/gefiltert.csv") as file:
            tagout = open("./daten/verlaufWoche.csv", "w")
            tagout.write("Lat,Long,Ort,Wochentag,Wert\n")
            next(file)
            dic = {}
            for lines in file:
                lines = lines.strip()
                linie = lines.split(",")
                lat = linie[0]
                lon = linie[1]
                ort = linie[2]
                wert = linie[4]
                datum = linie[3].split(" ")[0]
                datum = datum.split("-")
                datum = datetime.datetime(int(datum[0]), int(datum[1]), int(datum[2]))
                wochentag = calendar.day_name[datum.weekday()]
                if wert != "NA":
                    wert = float(wert)
                    if (lat,lon,ort, wochentag) in dic:
                        values = dic[(lat,lon,ort,wochentag)]
                        values[0] += wert
                        values[1] += 1
                        dic[(lat,lon,ort,wochentag)] = values
                    else:
                        dic[(lat,lon,ort,wochentag)] = [wert, 1]
            for ele in sorted(dic):
                values = dic[ele]
                avg = values[0] / values[1]
                tagout.write(str(ele[0]) + "," + str(ele[1]) + "," + str(ele[2]) + "," + str(ele[3]) + "," + "%.3f" %avg + "\n")
    else:
        with open("./daten/gefiltert.csv") as file:
            tagout = open("./daten/verlaufMonat.csv", "w")
            tagout.write("Lat,Long,Ort,Tag,Wert\n")
            next(file)
            dic = {}
            for lines in file:
                lines = lines.strip()
                linie = lines.split(",")
                lat = linie[0]
                lon = linie[1]
                ort = linie[2]
                wert = linie[4]
                datum = linie[3].split(" ")[0]
                tag = int(datum.split("-")[2])
                if wert != "NA":
                    wert = float(wert)
                    if (lat,lon,ort,tag) in dic:
                        values = dic[lat,lon,ort,tag]
                        values[0] += wert
                        values[1] += 1
                        dic[lat,lon,ort,tag] = values
                    else:
                        dic[lat,lon,ort,tag] = [wert, 1]
            for ele in sorted(dic):
                values = dic[ele]
                avg = values[0] / values[1]
                tagout.write(str(ele[0]) + "," + str(ele[1]) + "," + str(ele[2]) + "," + str(ele[3]) + "," + "%.3f" %avg + "\n")
                

def filtern(schadstoff, start, end):
    #Öffnet das zum Schadstoff passende File und entfernt alle Linien, die nicht im Datumsrange liegen. Speichert diese in gefiltert
    #
    output = open("./daten/gefiltert.csv", "w")
    output.write("Lat,Long,Ort,Datum,Wert\n")
    start = datetime.datetime(int(start[:4]),int(start[5:7]),int(start[8:10]))
    end = datetime.datetime(int(end[:4]),int(end[5:7]),int(end[8:10]))
    with open("./daten/" + schadstoff + ".csv") as file:
        next(file)
        for lines in file:
            lines = lines.strip()
            linie = lines.split(",")
            datum = linie[3].split(" ")[0]
            datum = datum.split("-")
            datum = datetime.datetime(int(datum[0]), int(datum[1]), int(datum[2]))
            if start <= datum and datum <= end:
                output.write(lines + "\n")



if __name__ == '__main__':
    app.run_server(debug=True, threaded=True,use_reloader=True)
