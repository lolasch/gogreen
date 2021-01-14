# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
global counter
counter = 0
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date
import json
#import time
import calendar
import datetime
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
counter = 0
app.title = 'Go Green'


server = app.server


colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#def main():
    #make_line_charts("Woche", "NO2", "2019-04-01", "2020-12-31", None)
    #global gefiltert 
    #kartenDic = kartenWerte(filtern("NO2", "2019-04-01", "2020-12-31"))
    #karte = px.scatter_mapbox(pd.DataFrame.from_dict(kartenWerte(filtern("NO2", "2019-04-01", "2020-12-31")),orient='index', columns = ["Ort","Lat","Long", "Durchschnitt"]), lat="Lat", lon="Long", zoom=11, height=300, width=870, size = "Durchschnitt", hover_name="Ort",)
    #karte.update_layout(mapbox_style="open-street-map",showlegend=False)
    #karte.update_layout(margin={"r":0,"t":0,"l":30,"b":0})
        

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
            # Radio mit Auswahlmöglichkeit für Luftverschmutzungsart
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
            # Radio mit Auswahlmöglichkeit für Tag/Woche/Monat
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
            #Auswahlmöglichkeit für Zeit
            dcc.DatePickerRange(
                style={
                    'color': colors['text']
                },  
                id='datepicker',
                display_format='DD.MM.Y',
                number_of_months_shown = 6,
                updatemode = 'bothdates',
                with_portal = True,
                min_date_allowed=date(2019, 4, 1),
                max_date_allowed=date(2020, 12, 31),
                initial_visible_month=date(2019, 4, 1),
                start_date=date(2019, 4, 1),
                end_date=date(2020, 12, 31)
            )
        ], className="row") ,
        html.Div([
            html.Div([
                    html.H3('Karte'),
                    html.Div(
                        children = [
                            dcc.Graph(
                                id='g1'
                            ),
                        ]
                    ),

                    html.Div(
                        children = [
                            dcc.Graph(
                                id="corona",
                            ),
                        ] 
                )], className="six columns"),

            html.Div([
                html.H3('Zeitlicher Verlauf'),

                html.Div( 
                    children = [
                        dcc.Graph(
                            id="zeitstrahl",
                        ),
                    ] 
                ),
                html.Div(
                    children = [
                        dcc.Graph(
                            id="zeitverlauf",
                        ),
                    ] 
                ),
            ],
            className="six columns") ,
            html.Div(id='dummy')
        ]),
        html.Div(id='ortDiv', style={'display': 'none'})
    
])


@app.callback([Output('g1', 'figure'),Output('corona', 'figure'),Output('zeitstrahl', 'figure'),Output('zeitverlauf', 'figure')],
    [Input('zeitabschnitt', 'value'),Input('schadwert', 'value'),Input('datepicker', 'start_date'),Input('datepicker', 'end_date'),Input('ortDiv','children')])
def mainCallback(zeit, schadstoff, start_date, end_date, ortKlick = None):
    """ Wird immer getriggert, wenn was passiert. Sammelt alles und stellt das dann in den Outputs dar """
    gefiltert = filtern(schadstoff, start_date, end_date)
    werteZeitstrahl, werteVerlauf = zeitstrahlBerechnen(zeit, gefiltert)
    werteStrahlOrt = ortsWerteBerechnen(zeit, gefiltert)
    werteVerlaufOrt = zeitverlaufOrt(zeit,gefiltert)
    berechneteKarte = karteRendern(gefiltert)
    zeitstrahl, zeitverlauf = zeitstrahlUndVerlaufRendern(schadstoff,werteZeitstrahl,werteVerlauf)
    zeitstrahl, zeitverlauf = orteHinzufuegen(werteStrahlOrt,werteVerlaufOrt,ortKlick,zeitstrahl,zeitverlauf)
    coronaFig = coronaRendern(zeit)
    return (berechneteKarte,coronaFig,zeitstrahl,zeitverlauf)

def karteRendern(gefiltert):
    """Erstellt die Figure Karte mit dem Werten aus gefiltert und gibt diese zurück """
    kartenDic = kartenWerte(gefiltert)
    karte = px.scatter_mapbox(pd.DataFrame.from_dict(kartenDic,orient='index', columns = ["Ort","Lat","Long", "Durchschnitt"]), lat="Lat", color = "Ort", lon="Long", zoom=11, height=300, width=870, size = "Durchschnitt", hover_name="Ort",)
    karte.update_layout(mapbox_style="open-street-map",showlegend=False)
    karte.update_layout(margin={"r":0,"t":0,"l":30,"b":0})
    return karte

def coronaRendern(zeit):
    if zeit == "Tag":
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSort.csv") #Fälle nach Tagen 
    else:
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSortWoche.csv") #Fälle nach Wochen
    corona = make_subplots(specs=[[{"secondary_y": True}]])
    corona.add_trace(
        go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Faelle, name="Falldaten"), # Linke Achse -> Fälle
        secondary_y=False,
    )
    corona.add_trace(
        go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Tote, name="Tode"),secondary_y=True, # Rechte Achse -> Tode
    )

    corona.update_layout(title_text="Corona-Inzidenzzahlen in Barcelona",showlegend=False,height=300,margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)
    corona.update_xaxes(title_text="Zeit")
    corona.update_yaxes(title_text="<b>Fallzahlen</b> absolut", secondary_y=False, title_font=dict(color="blue"))
    corona.update_yaxes(title_text="<b>Tode</b> absolut", secondary_y=True,title_font=dict(color="red"))

    return corona


@app.callback(Output('ortDiv','children'), Input('g1','clickData'))
def klickSpeichern(klick):
    """ Simpler Callback, der in ein unsichtbares Div die geklickten Orte schreibt"""
    if klick != None:
        ort = str(klick['points'][0]['hovertext'])
        ort = {"Ort": ort}
        return json.dumps(ort)
    else:
        return None

def zeitstrahlUndVerlaufRendern(schadstoff, werteZeitstrahl, werteVerlauf):
    """Bekommt den Schadstoff (zur Achsenbeschriftung) und die Werte für Zeitstrahl und Verlauf. Returnt zwei Figs damit"""

    zeitstrahlQuelle = pd.DataFrame.from_dict(werteZeitstrahl ,orient='index', columns = ["Monat","Jahr","Wert"])
    verlaufQuelle = pd.DataFrame.from_dict(werteVerlauf ,orient='index', columns = ["Datum","Jahr","Wert"])
    #zeitstrahl2020 = zeitstrahlQuelle.filter(like='2020', axis=0)
    #zeitstrahl2019 = zeitstrahlQuelle.filter(like='2019', axis=0)
    #zeitstrahlQuelle = zeitstrahlQuelle.filter("Jahr"=="2019")
    zeitstrahl = px.line(zeitstrahlQuelle, x="Monat", y="Wert", color = "Jahr", color_discrete_sequence=[ 'blue','gray'])
    zeitverlauf = px.line(verlaufQuelle, x="Datum", y="Wert", color = "Jahr", color_discrete_sequence=['orange', 'pink']) 

    #zeitstrahl.add_trace(px.Scatter(x=zeitstrahl2020.Monat, y=zeitstrahl2020.Wert,line=dict(color="black"), name="2020")),
    #zeitstrahl.add_trace(px.Scatter(x=zeitstrahl2019.Monat, y=zeitstrahl2019.Wert,line=dict(color="black"), name="2019"))
    zeitstrahl.update_layout(height=300,margin={"r":0,"t":30,"l":30,"b":0},title_x=0.5)
    zeitverlauf.update_layout(height=300,margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)

    if schadstoff == "CO":
        zeitverlauf.update_yaxes(title_text="<b>mg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>mg/m³</b>")
    else: 
        zeitverlauf.update_yaxes(title_text="<b>µg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>µg/m³</b>")
    return [zeitstrahl,zeitverlauf]

def orteHinzufuegen(werteStrahlOrt, werteVerlaufOrt,ortKlick,zeitstrahl,zeitverlauf):
    """ Fügt auf Zeitstrahl/verlauf Spuren der Orte hinzu, wenn die Werte dafür nicht none sind"""
    if ortKlick != None:
        ortsname = json.loads(ortKlick)["Ort"]
        ortQuelle = pd.DataFrame.from_dict(werteStrahlOrt, orient='index', columns = ["Datum","Jahr","Ort","Wert"])
        ortQuelle = ortQuelle[ortQuelle.Ort == ortsname]
        ort2019 = ortQuelle.filter(like='2019', axis=0)
        ort2020 = ortQuelle.filter(like='2020', axis=0)
        #ortFigure = px.line(ortQuelle, x="Datum", y="Wert", color = "Jahr", hover_name="Ort",  color_discrete_sequence=['green', 'red'])
        #ortFigure.data[0].name = "2020 - " + ortsname
        #ortFigure.data[1].name = "2019 - " + ortsname
        #zeitstrahl = go.Figure(data = zeitstrahl.data + ortFigure.data)
        zeitstrahl.add_trace(go.Scatter(x=ort2019.Datum, y=ort2019.Wert, name = ortsname + " 2019"))
        zeitstrahl.add_trace(go.Scatter(x=ort2020.Datum, y=ort2020.Wert, name = ortsname + " 2020"))
        ortVerlaufQuelle = pd.DataFrame.from_dict(werteVerlaufOrt, orient='index', columns = ["Monat","Jahr","Ort","Wert"])
        ortV2019 = ortVerlaufQuelle.filter(like='2019', axis=0)
        ortV2020 = ortVerlaufQuelle.filter(like='2020', axis=0)
        #ortVFigure = px.line(ortVerlaufQuelle, x="Datum", y="Wert", color = "Jahr", hover_name="Ort", color_discrete_sequence=['green', 'red'])
        #ortVFigure.data[0].name = "2020 - " + ortsname
        #ortVFigure.data[1].name = "2019 - " + ortsname
        #zeitstrahl = go.Figure(data = zeitstrahl.data + ortFigure.data)
        zeitverlauf.add_trace(go.Scatter(x=ortV2019.Monat, y=ortV2019.Wert, name = ortsname + " 2019"))
        zeitverlauf.add_trace(go.Scatter(x=ortV2020.Monat, y=ortV2020.Wert, name = ortsname + " 2020"))
    return [zeitstrahl, zeitverlauf]


def filtern(schadstoff, start, end):
    #Öffnet das zum Schadstoff passende File und entfernt alle Linien, die nicht im Datumsrange liegen. Speichert diese in gefiltert
    #
    gefiltert = {}
    start = datetime.datetime(int(start[:4]),int(start[5:7]),int(start[8:10]))
    end = datetime.datetime(int(end[:4]),int(end[5:7]),int(end[8:10]))
    file = open("./daten/" + schadstoff + ".csv")
    next(file)
    for lines in file:
        lines = lines.strip()
        linie = lines.split(",")
        ort = linie[0]
        datum = linie[1].split(" ")
        stunde = int(datum[1]) % 24
        datum = datum[0].split("-")
        datum = datetime.datetime(int(datum[0]),int(datum[1]),int(datum[2]),int(stunde))
        wert = linie[2]
        if wert != "NA":
            if start <= datum and datum <= end:
                gefiltert[ort, datum] = (ort, datum, float(wert))
    return gefiltert

def zeitstrahlBerechnen(zeit, gefiltert):
    #Berechnet die Werte für den Zeistrahl und den Tages/wochen/Monatsverlauf, indem die Daten jeweils in einem Dic gespeichert werden und dann der Mittelwert gebildet wird
    #
    zeitstrahl = {} 
    verlauf = {}
    zeitDic = {}
    verlaufDic = {}
    for item in gefiltert:
        ele = gefiltert[item]
        datum = ele[1]
        wert = ele[2]
        jahr = datum.year
        if zeit == "Tag":
            time = datum.hour
            datum = datetime.datetime(2020,datum.month,datum.day)
        elif zeit == "Woche":
            wochensplit = datum.isocalendar() # Jahr, Wochennummer, Tag
            #xaxis = calendar.day_name[datum.weekday()] #Name des Wochentags -> Samstag
            time = datum.weekday() #Nummer des Tages in der Woche
            #datum = date.fromisocalendar(wochensplit[0] , wochensplit[1], 1) #Datum des Wochenbeginns
            datum = wochensplit[1]
            jahr = wochensplit[0]
        else: 
            time = datum.day
            datum = datum.month
        #Dictionary wird mit Zeug für Zeitstrahl gefüllt
        if (datum, jahr) in zeitDic:
            values = zeitDic[datum,jahr]
            values[0] += wert
            values[1] += 1
            zeitDic[datum,jahr] = values
        else:
            zeitDic[datum,jahr] = [wert,1]
        #Dictionary wird mit Zeug für Verlauf gefüllt
        if (time,jahr) in verlaufDic:
            values = verlaufDic[time,jahr]
            values[0] += wert
            values[1] += 1
            verlaufDic[time,jahr] = values
        else:
            verlaufDic[time,jahr] = [wert, 1]
    #print(verlaufDic)
    

    for elem in sorted(zeitDic):
        values = zeitDic[elem]
        avg = values[0] / values[1]
        datum = str(elem[0])
        jahr = str(elem[1])
        zeitstrahl[datum,jahr] = [datum, jahr, round(avg, 3)]
    
    
    for elem in sorted(verlaufDic):
        values = verlaufDic[elem]
        avg = values[0] / values[1]
        time = str(elem[0])
        jahr = str(elem[1])
        verlauf[time, jahr] = [time,jahr,round(avg, 3)]
    return [zeitstrahl,verlauf]
    
def ortsWerteBerechnen(zeit,gefiltert):
    orte = {}
    ortsDic={}
    for item in gefiltert:
        ele = gefiltert[item]
        ort = ele[0]
        datum = ele[1]
        wert = ele[2]
        jahr = datum.year
        if zeit == "Tag":
            datum = datetime.datetime(2020,datum.month,datum.day)
        elif zeit == "Woche":
            wochensplit = datum.isocalendar() # Jahr, Wochennummer, Tag
            datum = wochensplit[1]
            jahr = wochensplit[0]
        else: 
            datum = datum.month
        
        if (datum,jahr,ort) in orte:
            values = orte[datum,jahr,ort]
            values[0] += wert
            values[1] += 1
            orte[datum,jahr,ort] = values
        else:
            orte[datum,jahr,ort] = [wert,1]
    for elem in sorted(orte):
        values = orte[elem]
        avg = values[0] / values[1]
        datum = str(elem[0])
        jahr = str(elem[1])
        ort = str(elem[2])
        ortsDic[datum,jahr,ort] = [datum, jahr, ort, round(avg, 3)]
    return ortsDic

def zeitverlaufOrt(zeit, gefiltert):
    #Berechnet die Werte für den Zeistrahl und den Tages/wochen/Monatsverlauf, indem die Daten jeweils in einem Dic gespeichert werden und dann der Mittelwert gebildet wird
    # 
    verlauf = {}
    verlaufDic = {}
    for item in gefiltert:
        ele = gefiltert[item]
        ort = ele[0]
        datum = ele[1]
        wert = ele[2]
        jahr = datum.year
        if zeit == "Tag":
            time = datum.hour
            datum = datetime.datetime(2020,datum.month,datum.day)
        elif zeit == "Woche":
            wochensplit = datum.isocalendar() # Jahr, Wochennummer, Tag
            #xaxis = calendar.day_name[datum.weekday()] #Name des Wochentags -> Samstag
            time = datum.weekday() #Nummer des Tages in der Woche
            #datum = date.fromisocalendar(wochensplit[0] , wochensplit[1], 1) #Datum des Wochenbeginns
            datum = wochensplit[1]
            jahr = wochensplit[0]
        else: 
            time = datum.day
            datum = datum.month
        #Dictionary wird mit Zeug für Verlauf gefüllt
        if (time,jahr,ort) in verlaufDic:
            values = verlaufDic[time,jahr,ort]
            values[0] += wert
            values[1] += 1
            verlaufDic[time,jahr,ort] = values
        else:
            verlaufDic[time,jahr,ort] = [wert, 1]
    #print(verlaufDic)
    
    
    for elem in sorted(verlaufDic):
        values = verlaufDic[elem]
        avg = values[0] / values[1]
        time = str(elem[0])
        jahr = str(elem[1])
        ort = str(elem[2])
        verlauf[time, jahr] = [time,jahr,ort,round(avg, 3)]
    return verlauf

def kartenWerte(gefiltert):
    # Berechnet aus den Daten im Verlauf einen Mittelwert, damit die Karte nur aus einem Wert besteht
    #
    ergebnisDic = {}
    dic = {}
    for item in gefiltert:
        ele = gefiltert[item]
        ort = ele[0]
        wert = ele[2]
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
            ergebnisDic[ele] = ele, 41.3864,2.1874, round(avg, 3)
        elif (ele == "Eixample"):
            ergebnisDic[ele] = ele, 41.3853,2.1538, round(avg, 3)
        elif (ele == "Gràcia"):
            ergebnisDic[ele] = ele, 41.3987,2.1534, round(avg, 3)
        elif (ele == "Palau Reial"):
            ergebnisDic[ele] = ele, 41.3875,2.1151, round(avg, 3)
        elif (ele == "Poblenou"):
            ergebnisDic[ele] = ele, 41.4039,2.2045, round(avg, 3)
        elif (ele == "Sants"):
            ergebnisDic[ele] = ele, 41.3788,2.1321, round(avg, 3)
        elif (ele == "Vall Hebron"):
            ergebnisDic[ele] = ele, 41.4261, 2.148, round(avg, 3)
        else:
            print("Error")
    return ergebnisDic


if __name__ == '__main__':
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True,use_reloader=True)
