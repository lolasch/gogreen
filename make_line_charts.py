def make_line_charts(value1, value2):
    if value1 == "Tag":
        quelle = pd.read_csv("./daten/"+ value2 + "Tag.csv")
        zeitstrahl = px.line(quelle, x = "Datum", y="Durchschnitt", title="Tagesschnitt", color= "Ort")
    elif value1 == "Woche":
        quelle = pd.read_csv("./daten/"+ value2 + "Woche.csv")
        zeitstrahl = px.line(quelle, x = "Wochenbeginn", y="Durchschnitt", title="Wochenschnitt", color= "Ort")
    else:
        quelle = pd.read_csv("./daten/"+ value2 + "Monat.csv")
        zeitstrahl = px.line(quelle, x = "Monat", y="Durchschnitt", title="Monatsschnitt", color= "Ort")
    zeitstrahl.update_xaxes(rangeslider_visible=True)

    karte = px.scatter_mapbox(quelle, lat="Lat", lon="Long", zoom=11, height=500, width=800, color= "Ort")
    karte.update_layout(mapbox_style="open-street-map")
    karte.update_layout(margin={"r":0,"t":0,"l":30,"b":0})

    return (
        html.Div([
                html.H3('Karte'),
                dcc.Graph(id='g1', figure=karte)
            ], className="six columns"),

        html.Div([
            html.H3('Zeitlicher Verlauf'),

            html.Div(
                dcc.Graph(
                    id="zeitstrahl",
                    figure=zeitstrahl
                )    
            )
        ],
        className="six columns")
    )
    