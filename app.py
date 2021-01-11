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
    
    html.Img(style={
        'width' : 250,
        'display' : 'block',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'text-align': 'center'
    },src=app.get_asset_url('gogreen.png')),

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
    zeitstrahlBerechnen(zeit)
    kartenWerte()

    zeitstrahlQuelle = pd.read_csv("./daten/zeitstrahl.csv")
    zeitstrahl = px.line(zeitstrahlQuelle, x = "Datum", y="Wert", color= "Ort")

    verlaufQuelle = pd.read_csv("./daten/verlauf.csv")
    zeitverlauf = px.line(verlaufQuelle, x="Zeit", y="Wert", color="Ort")
    if zeit == "Tag":
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSort.csv")
    else:
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSortWoche.csv")

    zeitstrahl.update_layout(height=300,margin={"r":0,"t":30,"l":30,"b":0},title_x=0.5)
    zeitverlauf.update_layout(height=300,margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)

    if schadstoff == "CO":
        zeitverlauf.update_yaxes(title_text="<b>mg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>mg/m³</b>")
    else: 
        zeitverlauf.update_yaxes(title_text="<b>µg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>µg/m³</b>")
    corona = make_subplots(specs=[[{"secondary_y": True}]])
    corona.add_trace(
        go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Faelle, name="yaxis data"),
        secondary_y=False,
    )
    corona.add_trace(
        go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Tote, name="yaxis2 data"),secondary_y=True,
    )

    corona.update_layout(title_text="Corona-Inzidenzzahlen",showlegend=False,height=300,margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)
    corona.update_xaxes(title_text="Zeit")
    corona.update_yaxes(title_text="<b>Fallzahlen</b> absolut", secondary_y=False, title_font=dict(color="red"))
    corona.update_yaxes(title_text="<b>Tote</b> absolut", secondary_y=True,title_font=dict(color="blue"))
    #corona.update_layout(xaxis_range=[start_date,end_date])

    karte = px.scatter_mapbox(pd.read_csv("./daten/karte.csv"), lat="Lat", lon="Long", zoom=11, height=300, width=870, color= "Ort", size = "Durchschnitt")
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
    

                

def filtern(schadstoff, start, end):
    #Öffnet das zum Schadstoff passende File und entfernt alle Linien, die nicht im Datumsrange liegen. Speichert diese in gefiltert
    #
    output = open("./daten/gefiltert.csv", "w")
    output.write("Ort,Datum,Wert\n")
    start = datetime.datetime(int(start[:4]),int(start[5:7]),int(start[8:10]))
    end = datetime.datetime(int(end[:4]),int(end[5:7]),int(end[8:10]))
    with open("./daten/" + schadstoff + ".csv") as file:
        next(file)
        for lines in file:
            lines = lines.strip()
            linie = lines.split(",")
            datum = linie[1].split(" ")[0]
            datum = datum.split("-")
            datum = datetime.datetime(int(datum[0]), int(datum[1]), int(datum[2]))
            if start <= datum and datum <= end:
                output.write(lines + "\n")

def zeitstrahlBerechnen(zeit):
    #Berechnet die Werte für den Zeistrahl und den Tages/wochen/Monatsverlauf, indem die Daten jeweils in einem Dic gespeichert werden und dann der Mittelwert gebildet wird
    #
    zeitstrahl = open("./daten/zeitstrahl.csv", "w")
    zeitstrahl.write("Ort,Datum,Wert\n") 
    verlauf = open("./daten/verlauf.csv", "w")
    verlauf.write("Ort,Zeit,Wert\n")
    file = open("./daten/gefiltert.csv")
    zeitDic = {}
    verlaufDic = {}
    next(file)
    for lines in file:
        lines = lines.strip()
        linie = lines.split(",")
        ort = linie[0]
        wert = linie[2]
        if wert != "NA":
            wert = float(wert)
            if zeit == "Tag":
                datum = linie[1].split(" ")[0]
                time = linie[1].split(" ")[1]
            elif zeit == "Woche":
                datum = linie[1].split(" ")[0].split("-")
                datum = datetime.datetime(int(datum[0]), int(datum[1]), int(datum[2])) # Formatiert Datum ins ISO-Format
                wochensplit = datum.isocalendar() # Jahr, Wochennummer, Tag
                wochentag = calendar.day_name[datum.weekday()] #Name des Wochentags -> Samstag
                time = datum.weekday() #Nummer des Tages in der Woche
                datum = date.fromisocalendar(wochensplit[0] , wochensplit[1], 1) #Datum des Wochenbeginns
            else: 
                datum = linie[1].split("-")
                monat = datum[0] + "-" + datum[1]
                time = int(datum[2])
            #Dictionary wird mit Zeug für Zeitstrahl gefüllt
            if (ort,datum) in zeitDic:
                values = zeitDic[(ort,datum)]
                values[0] += wert
                values[1] += 1
                zeitDic[(ort,datum)] = values
            else:
                zeitDic[(ort,datum)] = [wert, 1]
            #Dictionary wird mit Zeug für Verlauf gefüllt
            if (ort,time) in verlaufDic:
                values = verlaufDic[ort,time]
                values[0] += wert
                values[1] += 1
                verlaufDic[ort,time] = values
            else:
                verlaufDic[ort,time] = [wert, 1]

    for ele in sorted(zeitDic):
        values = zeitDic[ele]
        avg = values[0] / values[1]
        ort = str(ele[0])
        datum = str(ele[1])
        zeitstrahl.write(ort + "," + datum + "," + "%.3f" %avg + "\n")
    
    for ele in sorted(verlaufDic):
        values = verlaufDic[ele]
        avg = values[0] / values[1]
        ort = str(ele[0])
        time = str(ele[1])
        verlauf.write(ort + "," + time + "," + "%.3f" %avg + "\n")

def kartenWerte():
    # Berechnet aus den Daten im Verlauf einen Mittelwert, damit die Karte nur aus einem Wert besteht
    #
    kartenFile = open("./daten/karte.csv", "w")
    kartenFile.write("Lat,Long,Ort,Durchschnitt\n")
    with open("./daten/verlauf.csv", "r")  as file:
        next(file)
        dic = {}
        for lines in file:
            lines = lines.strip()
            linie = lines.split(",")
            ort = linie[0]
            wert = float(linie[2])
            if (ort) in dic:
                values = dic[ort]
                values[0] += wert
                values[1] += 1
                dic[ort] = values
            else:
                dic[ort] = [wert, 1]

    for ele in dic:
        values = dic[ele]
        avg = values[0] / values[1]
        if (ele == "Ciutadella"):
            kartenFile.write("41.3864,2.1874," + str(ele) + "," + "%.3f" %avg + "\n")
        elif (ele == "Eixample"):
            kartenFile.write("41.3853,2.1538," + str(ele) + "," + "%.3f" %avg + "\n")
        elif (ele == "Gràcia"):
            kartenFile.write("41.3987,2.1534," + str(ele) + "," + "%.3f" %avg + "\n")
        elif (ele == "Palau Reial"):
            kartenFile.write("41.3875,2.1151," + str(ele) + "," + "%.3f" %avg + "\n")
        elif (ele == "Poblenou"):
            kartenFile.write("41.4039,2.2045," + str(ele) + "," + "%.3f" %avg + "\n")
        elif (ele == "Sants"):
            kartenFile.write("41.3788,2.1321," + str(ele) + "," + "%.3f" %avg + "\n")
        elif (ele == "Vall Hebron"):
            kartenFile.write("41.4261,2.148," + str(ele) + "," + "%.3f" %avg + "\n")
        else:
            print("Error")


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=True)
