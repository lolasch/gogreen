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
from datetime import date, datetime
import json
import linecache
#import time
import calendar
import datetime
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from past.builtins import execfile
import locale
locale.setlocale(locale.LC_ALL, 'de_DE')

external_scripts = ["https://cdn.plot.ly/plotly-locale-de-latest.js"]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_scripts=external_scripts, external_stylesheets=external_stylesheets)
#app.scripts.append_script({"external_url": "https://cdn.plot.ly/plotly-locale-de-latest.js"})
app.title = 'Go Green'


server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

execfile('layout1.py')


@app.callback([Output('g1', 'figure'),Output('corona', 'figure'),Output('zeitstrahl', 'figure'),Output('zeitverlauf', 'figure'),Output('infobox', 'children')],
    [Input('zeitabschnitt', 'value'),Input('schadwert', 'value'),Input('start','value'), Input('ende','value'),Input('ortDiv','children'),Input('startTag','value'), Input('endTag','value')])
def mainCallback(zeit, schadstoff, start, ende, ortKlick,startTag, endTag):
    """ Wird immer getriggert, wenn was passiert. Sammelt alles und stellt das dann in den Outputs dar """
    gefiltert = filtern(schadstoff, int(start), int(ende), startTag,endTag)
    werteZeitstrahl, werteVerlauf = zeitstrahlBerechnen(zeit, gefiltert)
    werteStrahlOrt = ortsWerteBerechnen(zeit, gefiltert)
    werteVerlaufOrt = zeitverlaufOrt(zeit,gefiltert)
    berechneteKarte, kartenDic = karteRendern(gefiltert)
    zeitstrahl, zeitverlauf = zeitstrahlUndVerlaufRendern(zeit, schadstoff,werteZeitstrahl,werteVerlauf, start, ende,startTag,endTag)
    zeitstrahl, zeitverlauf = orteHinzufuegen(werteStrahlOrt,werteVerlaufOrt,ortKlick,zeitstrahl,zeitverlauf)
    coronaFig = coronaRendern(zeit)
    infobox = infoboxErstellen(schadstoff,kartenDic, ortKlick, start,ende)
    return (berechneteKarte,coronaFig,zeitstrahl,zeitverlauf, infobox)

def karteRendern(gefiltert):
    """Erstellt die Figure Karte mit dem Werten aus gefiltert und gibt diese zurück """
    kartenDic = kartenWerte(gefiltert)
    karte = px.scatter_mapbox(pd.DataFrame.from_dict(kartenDic,orient='index', columns = ["Ort","Lat","Long", "Durchschnitt"]), lat="Lat", color = "Ort", lon="Long", zoom=11, height=300, size = "Durchschnitt", hover_name="Ort",title="<b>Karte von Barcelona</b>")
    karte.update_layout(mapbox_style="open-street-map",showlegend=False)
    karte.update_layout(margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)
    return karte,kartenDic

def coronaRendern(zeit):
    if zeit == "Tag":
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSort.csv") #Fälle nach Tagen 
    else:
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSortWoche.csv") #Fälle nach Wochen
    sub = make_subplots(rows=4, cols=1, shared_xaxes=True, specs = [[{"secondary_y": True, "rowspan": 3}],[None],[None],[{"secondary_y": False}]])
    sub.add_trace(go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Faelle, name="Falldaten"),row=1, col=1, secondary_y=False)# Linke Achse -> Fälle
    sub.add_trace(go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Tote, name="Tode"),row=1, col=1, secondary_y=True,) # Rechte Achse -> Tode
    

    massnahmenQuelle = pd.read_csv("./daten/maßnahmen.csv")
    sub.append_trace(go.Scatter(x = massnahmenQuelle.Datum, y = massnahmenQuelle.Wert, mode = 'lines+markers', hovertext = massnahmenQuelle.Ereignis),row=4, col=1)
    
    sub.update_layout(title_text="<b>Corona-Inzidenzzahlen in Barcelona</b>",showlegend=False,height=300,margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5, hovermode="x unified")
    sub.update_xaxes(title_text="Zeit")
    sub.update_yaxes(title_text="<b>Fallzahlen</b> absolut", secondary_y=False, title_font=dict(color="blue"), row=1, col=1)
    sub.update_yaxes(title_text="<b>Tode</b> absolut", secondary_y=True,title_font=dict(color="red"))
    sub.update_yaxes(title_text="<b>Ereignisse</b>" ,tickvals=["Ereignis"], visible = True, row= 4, col = 1)
    sub.update_xaxes(visible = False, row = 1, col = 1)
    return sub

@app.callback([Output("startTag", 'max'), Output("startTag", 'value')],
            [Input('start','value')])
def TagAnzeigenStart(startMonat):
    startMonat = int(startMonat)
    if startMonat in set((1,3,5,7,8,10,12)):
        return [31,1]
    elif startMonat in set((4,6,9,11)):
        return [30,1]
    else:
        return [29,1]

@app.callback([Output("endTag", 'max'), Output("endTag", 'value')],
            [Input('ende','value')])
def TagAnzeigenEnde(endMonat):
    endMonat = int(endMonat)
    if endMonat in set((1,3,5,7,8,10,12)):
        return [31,31]
    elif endMonat in set((4,6,9,11)):
        return [30,30]
    else:
        return [29,29]



@app.callback(Output('ortDiv','children'), Input('g1','clickData'))
def klickSpeichern(klick):
    """ Simpler Callback, der in ein unsichtbares Div die geklickten Orte schreibt"""
    if klick != None:
        ort = str(klick['points'][0]['hovertext'])
        ort = {"Ort": ort}
        return json.dumps(ort)
    else:
        return None

def zeitstrahlUndVerlaufRendern(zeit, schadstoff, werteZeitstrahl, werteVerlauf, start, ende, startTag,endTag):
    """Bekommt den Schadstoff (zur Achsenbeschriftung) und die Werte für Zeitstrahl und Verlauf. Returnt zwei Figs damit"""
    zeitstrahlQuelle = pd.DataFrame.from_dict(werteZeitstrahl ,orient='index', columns = ["Monat","Jahr","Wert"])
    verlaufQuelle = pd.DataFrame.from_dict(werteVerlauf ,orient='index', columns = ["Datum","Jahr","x-Achse","Wert"])
    #zeitstrahl2020 = zeitstrahlQuelle.filter(like='2020', axis=0)
    #zeitstrahl2019 = zeitstrahlQuelle.filter(like='2019', axis=0)
    #zeitstrahlQuelle = zeitstrahlQuelle.filter("Jahr"=="2019")
    zeitstrahl = px.line(zeitstrahlQuelle, x="Monat", y="Wert", color = "Jahr", color_discrete_sequence=[ 'blue','gray'])
    zeitverlauf = px.line(verlaufQuelle, x="x-Achse", y="Wert", color = "Jahr", color_discrete_sequence=['orange', 'pink']) 

    #zeitstrahl.add_trace(px.Scatter(x=zeitstrahl2020.Monat, y=zeitstrahl2020.Wert,line=dict(color="black"), name="2020")),
    #zeitstrahl.add_trace(px.Scatter(x=zeitstrahl2019.Monat, y=zeitstrahl2019.Wert,line=dict(color="black"), name="2019"))
    zeitstrahl.update_layout(height=300,margin={"r":0,"t":50,"l":30,"b":20},title_x=0.5, hovermode="x unified")
    zeitverlauf.update_layout(height=300,margin={"r":0,"t":50,"l":30,"b":0},title_x=0.5, hovermode="x unified")

    if schadstoff == "CO":
        zeitverlauf.update_yaxes(title_text="<b>mg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>mg/m³</b>")
    else: 
        zeitverlauf.update_yaxes(title_text="<b>µg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>µg/m³</b>")
    start = calendar.month_name[int(start)]
    ende = calendar.month_name[int(ende)]
    if zeit == "Tag":        
        zeitverlauf.update_layout(title_text = "<b>Durchschnittlicher täglicher Verlauf von %s zwischen dem %s. %s und dem %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitverlauf.update_xaxes(title_text = "Uhrzeit")
        zeitstrahl.update_layout(title_text = "<b>Täglicher Verlauf von %s ab dem %s. %s bis zum %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitstrahl.update_xaxes(title_text = "Datum", ticktext=["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"], 
        tickvals=["2020-01-15","2020-02-15","2020-03-15","2020-04-15","2020-05-15","2020-06-15","2020-07-15","2020-08-15","2020-09-15","2020-10-15","2020-11-15","2020-12-15"])
    elif zeit == "Woche":
        zeitverlauf.update_layout(title_text = "<b>Durchschnittlicher wöchentlicher Verlauf von %s zwischen dem %s. %s und dem %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitverlauf.update_xaxes(title_text = "Tag in der Woche")
        zeitstrahl.update_layout(title_text = "<b>Wöchentlicher Verlauf von %s ab dem %s. %s bis zum %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitstrahl.update_xaxes(title_text = "Wochennummer")
    else:
        zeitverlauf.update_layout(title_text = "<b>Durchschnittlicher monatlicher Verlauf von %s zwischen dem %s. %s und dem %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitverlauf.update_xaxes(title_text = "Tag im Monat")
        zeitstrahl.update_layout(title_text = "<b>Monatlicher Verlauf %s ab dem %s. %s bis zum %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitstrahl.update_xaxes(title_text = "Monatsnummer")


    return [zeitstrahl,zeitverlauf]

def orteHinzufuegen(werteStrahlOrt, werteVerlaufOrt,ortKlick,zeitstrahl,zeitverlauf):
    """ Fügt auf Zeitstrahl/verlauf Spuren der Orte hinzu, wenn die Werte dafür nicht none sind"""
    if ortKlick != None:
        ortsname = json.loads(ortKlick)["Ort"]
        ortQuelle = pd.DataFrame.from_dict(werteStrahlOrt, orient='index', columns = ["Datum","Jahr","Ort","Wert"])
        ortQuelle = ortQuelle[ortQuelle.Ort == ortsname]
        ort2019 = ortQuelle.filter(like='2019', axis=0)
        ort2020 = ortQuelle.filter(like='2020', axis=0)
        ortFigure = px.line(ortQuelle, x="Datum", y="Wert", color = "Jahr", hover_name="Ort",  color_discrete_sequence=['green', 'red'])
        ortFigure.data[0].name = "2020 - " + ortsname
        ortFigure.data[1].name = "2019 - " + ortsname
        #zeitstrahl = go.Figure(data = zeitstrahl.data + ortFigure.data)
        #zeitstrahl.update_layout(height=300,margin={"r":0,"t":30,"l":30,"b":0},title_x=0.5)
        zeitstrahl.add_trace(go.Scatter(x=ort2019.Datum, y=ort2019.Wert, name = ortsname + " 2019"))
        zeitstrahl.add_trace(go.Scatter(x=ort2020.Datum, y=ort2020.Wert, name = ortsname + " 2020"))
        ortVerlaufQuelle = pd.DataFrame.from_dict(werteVerlaufOrt, orient='index', columns = ["Monat","Jahr","Ort","xAchse","Wert"])
        ortV2019 = ortVerlaufQuelle.filter(like='2019', axis=0)
        ortV2020 = ortVerlaufQuelle.filter(like='2020', axis=0)
        #ortVFigure = px.line(ortVerlaufQuelle, x="Datum", y="Wert", color = "Jahr", hover_name="Ort", color_discrete_sequence=['green', 'red'])
        #ortVFigure.data[0].name = "2020 - " + ortsname
        #ortVFigure.data[1].name = "2019 - " + ortsname
        #zeitstrahl = go.Figure(data = zeitstrahl.data + ortFigure.data)
        zeitverlauf.add_trace(go.Scatter(x=ortV2019.xAchse, y=ortV2019.Wert, name = ortsname + " 2019"))
        zeitverlauf.add_trace(go.Scatter(x=ortV2020.xAchse, y=ortV2020.Wert, name = ortsname + " 2020"))
    return [zeitstrahl, zeitverlauf]

def infoboxErstellen(schadstoff, kartenDic, ortKlick, start, ende):
    result = ()
    summe = 0
    for ele in kartenDic:
        values = kartenDic[ele]
        summe += float(values[3])
    avg = summe/len(kartenDic)
    result += (html.Li("Algemeiner Durchschnitt: " + str(round(avg, 3)))),
   
    if ortKlick != None:
        ort = json.loads(ortKlick)["Ort"]
        ortsWert = kartenDic[ort][3]
        result += (html.Li("Schnitt " + str(ort) + ": " + str(ortsWert))),
    
    startTag = datetime.datetime(2020,int(start),1).timetuple().tm_yday
    endTag = datetime.datetime(2020,int(ende),1).timetuple().tm_yday
    
    startline = linecache.getline("./daten/Faelle_nach_KreisenSort.csv", startTag + 1)
    startline = startline.strip()
    faelleSummeStart = int(startline.split(",")[3])
    todeSummeStart = int(startline.split(",")[4])

    endline = linecache.getline("./daten/Faelle_nach_KreisenSort.csv", endTag + 1)
    endline = endline.strip()
    faelleSummeEnde = int(endline.split(",")[3])
    todeSummeEnde = int(endline.split(",")[4])

    faelleSumme = faelleSummeEnde - faelleSummeStart
    todeSumme = todeSummeEnde - todeSummeStart
    result += (html.Li("Kumulierte Fälle im Zeitraum: " + str(faelleSumme))),
    result += (html.Li("Kumulierte Tode im Zeitraum: " + str(todeSumme))),

    return result
    


def filtern(schadstoff, start, end, startTag, endTag):
    #Öffnet das zum Schadstoff passende File und entfernt alle Linien, die nicht im Datumsrange liegen. Speichert diese in gefiltert
    #
    gefiltert = {}
    #start = datetime.datetime(int(start[:4]),int(start[5:7]),int(start[8:10]))
    #end = datetime.datetime(int(end[:4]),int(end[5:7]),int(end[8:10]))
    file = open("./daten/" + schadstoff + ".csv")
    next(file)
    for lines in file:
        lines = lines.strip()
        linie = lines.split(",")
        ort = linie[0]
        datum = linie[1].split(" ")
        stunde = int(datum[1]) % 24
        datum = datum[0].split("-")
        jahr = int(datum[0])
        monat = int(datum[1])
        tag = int(datum[2])
        wert = linie[2]
        if wert != "NA":
            if (start == monat and tag >= startTag) or (start < monat and monat < end) or (end == monat and tag <= endTag):
                datum = datetime.datetime(jahr, monat, tag,int(stunde))
                gefiltert[ort, datum] = (ort, datum, float(wert))
    return gefiltert

def zeitstrahlBerechnen(zeit, gefiltert):
    """Berechnet die Werte für den Zeistrahl und den Tages/wochen/Monatsverlauf, indem die Daten jeweils in einem Dic gespeichert werden und dann der Mittelwert gebildet wird
    """
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
            xaxis = str(time).zfill(2) + ":00"
        elif zeit == "Woche":
            wochensplit = datum.isocalendar() # Jahr, Wochennummer, Tag
            xaxis = calendar.day_name[datum.weekday()] #Name des Wochentags -> Samstag
            time = datum.weekday() #Nummer des Tages in der Woche
            #datum = date.fromisocalendar(wochensplit[0] , wochensplit[1], 1) #Datum des Wochenbeginns
            datum = wochensplit[1]
            jahr = wochensplit[0]
        else: 
            time = datum.day
            xaxis = str(time) + "."
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
        if (time,jahr,xaxis) in verlaufDic:
            values = verlaufDic[time,jahr,xaxis]
            values[0] += wert
            values[1] += 1
            verlaufDic[time,jahr, xaxis] = values
        else:
            verlaufDic[time,jahr, xaxis] = [wert, 1]
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
        xaxis = str(elem[2])
        verlauf[time, jahr] = [time,jahr,xaxis,round(avg, 3)]
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
            xaxis = str(time).zfill(2) + ":00"
        elif zeit == "Woche":
            wochensplit = datum.isocalendar() # Jahr, Wochennummer, Tag
            xaxis = calendar.day_name[datum.weekday()] #Name des Wochentags -> Samstag
            time = datum.weekday() #Nummer des Tages in der Woche
            #datum = date.fromisocalendar(wochensplit[0] , wochensplit[1], 1) #Datum des Wochenbeginns
            datum = wochensplit[1]
            jahr = wochensplit[0]
        else: 
            time = datum.day
            xaxis = str(time) + "."
            datum = datum.month
        #Dictionary wird mit Zeug für Verlauf gefüllt
        if (time,jahr,ort,xaxis) in verlaufDic:
            values = verlaufDic[time,jahr,ort,xaxis]
            values[0] += wert
            values[1] += 1
            verlaufDic[time,jahr,ort,xaxis] = values
        else:
            verlaufDic[time,jahr,ort,xaxis] = [wert, 1]
    #print(verlaufDic)
    
    
    for elem in sorted(verlaufDic):
        values = verlaufDic[elem]
        avg = values[0] / values[1]
        time = str(elem[0])
        jahr = str(elem[1])
        ort = str(elem[2])
        xaxis = str(elem[3])
        verlauf[time, jahr] = [time,jahr,ort,xaxis,round(avg, 3)]
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