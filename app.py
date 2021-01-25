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
#locale.setlocale(locale.LC_ALL, 'de_DE') # nur Lokal. Kann Heroku nicht!

external_scripts = ["https://cdn.plot.ly/plotly-locale-de-latest.js"]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_scripts=external_scripts, external_stylesheets=external_stylesheets)
#app.scripts.append_script({"external_url": "https://cdn.plot.ly/plotly-locale-de-latest.js"})
app.title = 'Decelearte'


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
    berechneteKarte, kartenDic = karteRendern(gefiltert,ortKlick)
    zeitstrahl, zeitverlauf = zeitstrahlUndVerlaufRendern(zeit, schadstoff,werteZeitstrahl,werteVerlauf, start, ende,startTag,endTag)
    zeitstrahl, zeitverlauf = orteHinzufuegen(werteStrahlOrt,werteVerlaufOrt,ortKlick,zeitstrahl,zeitverlauf)
    coronaFig = coronaRendern(zeit)
    infobox = infoboxErstellen(schadstoff,kartenDic, ortKlick, start,ende)
    return (berechneteKarte,coronaFig,zeitstrahl,zeitverlauf, infobox)

def karteRendern(gefiltert,ortKlick):
    """Erstellt die Figure Karte mit dem Werten aus gefiltert und gibt diese zurück """
    kartenDic = kartenWerte(gefiltert)

    sequence = ['#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000']
    if ortKlick != None:
        ort = json.loads(ortKlick)["Ort"]
        counter = 0
        for elem in kartenDic:
            if elem == ort:
                break
            counter += 1
        sequence[counter] = "#b10000" 
    
    karte = px.scatter_mapbox(pd.DataFrame.from_dict(kartenDic,orient='index', columns = ["Ort","Lat","Long", "Durchschnitt"]), lat="Lat", color = "Ort", lon="Long", zoom=11, height=300, size = "Durchschnitt", 
    color_discrete_sequence=sequence,hover_name="Ort",title="<b>Air Quality Measure Stations</b>")
    karte.update_layout(mapbox_style="open-street-map",showlegend=False)
    karte.update_layout(margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)
    return karte,kartenDic

def coronaRendern(zeit):
    if zeit == "Tag":
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSort.csv") #Fälle nach Tagen 
    else:
        coronaWerte = pd.read_csv("./daten/Faelle_nach_KreisenSortWoche.csv") #Fälle nach Wochen
    
    sub = make_subplots(specs=[[{"secondary_y": True}]])
    sub.add_trace(go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Faelle, name="Falldaten"), secondary_y=False)# Linke Achse -> Fälle
    sub.add_trace(go.Scatter(x=coronaWerte.Datum, y=coronaWerte.Tote, name="Tode",line=dict(color = "orange")), secondary_y=True,) # Rechte Achse -> Tode
    

    massnahmenQuelle = pd.read_csv("./daten/maßnahmen.csv")
    sub.add_trace(go.Bar(x = massnahmenQuelle.Date, y = massnahmenQuelle.Value1, marker_color = "rgba(205, 205, 205, 1)", hovertext = massnahmenQuelle.Event),secondary_y=False)
    
    sub.update_layout(title_text="<b>Corona incident rate in Barcelona</b>",showlegend=False,height=300,margin={"r":0,"t":40,"l":30,"b":0},title_x=0.5)
    sub.update_xaxes(title_text="Zeit")
    sub.update_yaxes(title_text="<b>Cases</b> absolute", secondary_y=False, title_font=dict(color="orange"))
    sub.update_yaxes(title_text="<b>Deaths</b> absolute", secondary_y=True,title_font=dict(color="blue"))
    #sub.update_yaxes(title_text="<b>Events</b>" ,tickvals=["Events"], visible = True, row= 4, col = 1)
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
        #print(klick)
        ort = str(klick['points'][0]['hovertext'])
        ort = {"Ort": ort}
        return json.dumps(ort)
    else:
        return None

def zeitstrahlUndVerlaufRendern(zeit, schadstoff, werteZeitstrahl, werteVerlauf, start, ende, startTag,endTag):
    """Bekommt den Schadstoff (zur Achsenbeschriftung) und die Werte für Zeitstrahl und Verlauf. Returnt zwei Figs damit"""
    zeitstrahlQuelle = pd.DataFrame.from_dict(werteZeitstrahl ,orient='index', columns = ["Monat","Jahr","Wert"])
    verlaufQuelle = pd.DataFrame.from_dict(werteVerlauf ,orient='index', columns = ["Datum","Jahr","xAchse","Wert"])
    zeitstrahl2020 = zeitstrahlQuelle.filter(like='2020', axis=0)
    zeitstrahl2019 = zeitstrahlQuelle.filter(like='2019', axis=0)
    zeitverlauf2020 = verlaufQuelle.filter(like='2020', axis=0)
    zeitverlauf2019 = verlaufQuelle.filter(like='2019', axis=0)
    zeitstrahl = go.Figure()
    zeitverlauf = go.Figure()
    #zeitstrahlQuelle = zeitstrahlQuelle.filter("Jahr"=="2019")
    #zeitstrahl = px.line(zeitstrahlQuelle, x="Monat", y="Wert", color = "Jahr", color_discrete_sequence=['rgba(255, 0, 0, 1)','rgba(255, 0, 0, 0.5)'])
    #zeitverlauf = px.line(verlaufQuelle, x="x-Achse", y="Wert", color = "Jahr", color_discrete_sequence=['orange', 'pink']) 

    
    zeitstrahl.add_trace(go.Scatter(x=zeitstrahl2020.Monat, y=zeitstrahl2020.Wert,mode='lines',line=dict(color="rgba(0,0,0, 1)"), name="2020"))
    zeitstrahl.add_trace(go.Scatter(x=zeitstrahl2019.Monat, y=zeitstrahl2019.Wert,mode='lines',line=dict(color="rgba(0,0,0, 0.5)", dash='dash'), name="2019"))
    zeitverlauf.add_trace(go.Scatter(x=zeitverlauf2020.xAchse, y=zeitverlauf2020.Wert,mode='lines',line=dict(color="rgba(0,0,0, 1)"), name="2020")),
    zeitverlauf.add_trace(go.Scatter(x=zeitverlauf2019.xAchse, y=zeitverlauf2019.Wert,mode='lines',line=dict(color="rgba(0,0,0, 0.5)", dash='dash'), name="2019"))
    zeitstrahl.update_layout(height=300,margin={"r":20,"t":50,"l":50,"b":20},title_x=0.5, hovermode="x unified")
    zeitverlauf.update_layout(height=200,margin={"r":20,"t":50,"l":50,"b":0},title_x=0.5, hovermode="x unified")

    if schadstoff == "CO":
        zeitverlauf.update_yaxes(title_text="<b>mg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>mg/m³</b>")
    else: 
        zeitverlauf.update_yaxes(title_text="<b>µg/m³</b>")
        zeitstrahl.update_yaxes(title_text="<b>µg/m³</b>")
    start = calendar.month_name[int(start)]
    ende = calendar.month_name[int(ende)]
    if zeit == "Tag":        
        zeitverlauf.update_layout(title_text = "<b>Average daily course of %s between %s. %s and the %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitverlauf.update_xaxes(title_text = "Time")
        zeitstrahl.update_layout(title_text = "<b>Daily course of %s between %s. %s and the %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitstrahl.update_xaxes(title_text = "Date", ticktext=["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 
        tickvals=["2020-01-15","2020-02-15","2020-03-15","2020-04-15","2020-05-15","2020-06-15","2020-07-15","2020-08-15","2020-09-15","2020-10-15","2020-11-15","2020-12-15"])
    elif zeit == "Woche":
        zeitverlauf.update_layout(title_text = "<b>Average weekly course of %s between %s. %s and %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitverlauf.update_xaxes(title_text = "Day of the Week")
        zeitstrahl.update_layout(title_text = "<b>Weekly course of %s between %s. %s and %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitstrahl.update_xaxes(title_text = "Weeknumber")
    else:
        zeitverlauf.update_layout(title_text = "<b>Average monthly course of %s between %s. %s and %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitverlauf.update_xaxes(title_text = "Day of the Month")
        zeitstrahl.update_layout(title_text = "<b>Monthly course %s between %s. %s and %s. %s</b>" % (schadstoff,startTag,start,endTag,ende),title_x=0.5)
        zeitstrahl.update_xaxes(title_text = "Monthnumber")


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
        #zeitstrahl.update_layout(height=300,margin={"r":0,"t":30,"l":30,"b":0},title_x=0.5)

        zeitstrahl.add_trace(go.Scatter(x=ort2020.Datum, y=ort2020.Wert, name = ortsname + " 2020",mode='lines',line=dict(color="rgba(177,0,0, 1)")))
        zeitstrahl.add_trace(go.Scatter(x=ort2019.Datum, y=ort2019.Wert, name = ortsname + " 2019",mode='lines',line=dict(color="rgba(117, 0, 0, 0.5)",dash='dash')))
        ortVerlaufQuelle = pd.DataFrame.from_dict(werteVerlaufOrt, orient='index', columns = ["Monat","Jahr","Ort","xAchse","Wert"])
        ortV2019 = ortVerlaufQuelle.filter(like='2019', axis=0)
        ortV2020 = ortVerlaufQuelle.filter(like='2020', axis=0)
        #ortVFigure = px.line(ortVerlaufQuelle, x="Datum", y="Wert", color = "Jahr", hover_name="Ort", color_discrete_sequence=['green', 'red'])
        #ortVFigure.data[0].name = "2020 - " + ortsname
        #ortVFigure.data[1].name = "2019 - " + ortsname
        #zeitstrahl = go.Figure(data = zeitstrahl.data + ortFigure.data)
        zeitverlauf.add_trace(go.Scatter(x=ortV2020.xAchse, y=ortV2020.Wert, name = ortsname + " 2020",mode='lines',line=dict(color="rgba(117, 0, 0, 1)")))
        zeitverlauf.add_trace(go.Scatter(x=ortV2019.xAchse, y=ortV2019.Wert, name = ortsname + " 2019",mode='lines',line=dict(color="rgba(117, 0, 0, 0.5)",dash='dash')))
        
    return [zeitstrahl, zeitverlauf]

def infoboxErstellen(schadstoff, kartenDic, ortKlick, start, ende):
    result = ()
    summe = 0
    for ele in kartenDic:
        values = kartenDic[ele]
        summe += float(values[3])
    avg = summe/len(kartenDic)
    result += (html.Li("Average all stations: " + str(round(avg, 3)))),
   
    if ortKlick != None:
        ort = json.loads(ortKlick)["Ort"]
        ortsWert = kartenDic[ort][3]
        result += (html.Li("Average in " + str(ort) + ": " + str(ortsWert))),
    
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
    result += (html.Li("All cases summed up: " + str(faelleSumme))),
    result += (html.Li("All deaths summed up: " + str(todeSumme))),

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
            print("StandortFehler")
    return ergebnisDic


if __name__ == '__main__':
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True,use_reloader=True)