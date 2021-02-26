

Implementierung

Anforderungen an die Implementierung

Aus der explorativen Datenanalyse und den daraus resultierenden Experimenten, wurden für den zu entwickelnden Prototyp im Hinblick auf die Untersuchungshypothese folgende Anforderungen an diesen entwickelt. Dabei wird im Folgenden zwischen Anforderungen für die Visualisierung der Daten, sowie der Benutzung und Handhabe des Prototyps unterschieden.

Visualisierungsanforderungen:

- (1) Visualisierung gemessener Werte eines Schadstoffes und der Lokalität an der dieser jeweils gemessen worden ist

Begründung: Durch eine solche Visualisierung sollen mögliche Korrelationen eines gemessenen Wertes und dem Ort der Messung untersucht werden. Dabei soll der Einfluss des Ortes durch dessen Charakteristika wie zum Beispiel Verkehrssituation, Bebauung, Grünflächenanteil usw. analysiert werden. Zudem soll dadurch eine mögliche Erklärunggrundlage gefunden werden für unterschiedliche Messergebnisse an verschiedenen Orten zu gleichen Zeitpunkten

- (2) Visualisierung eines Vergleichs der gemessenen Werte an den verschiedenen Orten/Messstationen

Begründung: Es soll untersucht werden, ob die Luftqualität/Luftverschmutzungen an den verschiedenen Orten/Messtationen unterschiedlich ist und wie sehr sie sich von den anderen Orten unterscheidet

- (3) Visualisierung der Anzahl der festgestellten Infizierten an Covid-19 im zeitlichen Verlauf
Begründung: Die Infektionszahl ist ein Indikator, der die Auswirkung einer Pandemie beschreibt. U.a. wird anhand dieser politischen Maßnahmen festgelegt um Pandemie einzudämmen.

- (4) Visualisierung der Anzahl der Todesfälle mit Covid-19-Infizierung im zeitlichen Verlauf

Begründung: Analog zur Infektionszahl sind die Todesfälle ein Indikator, der die Auswirkung einer Pandemie beschreibt. Er wird auch zur Begründung von politischen Maßnahmen zur Eindämmung der Pandemie verwendet

- (5) Visualisierung von Regierungsmaßnahmen und deren jeweilige Zeitpunkte in Zusammenhang mit der Pandemie und deren Verlauf

Begründung: Regierungsmaßnahmen werden zu Eindämmung zur Pandemie getroffen. Diese können starke bis schwache Auswirkungen auf das gesellschaftliche Leben haben und somit das ganze Umfeld/Umwelt beeinflussen.

- (6) Visualisierung von Messwerten eines Schadstoffes und der Zeitpunkt der Messung

Begründung: Durch eine solche Visualisierung soll nach einer möglichen Korrelation zwischen Messwert und dem Zeitpunkt der Messung gesucht werden. Dabei sollen zeitliche Charakteristika wie zum Beispiel Uhrzeit (Berufsverkehr), Wochentag (Arbeitstag, Wochenende), Datum (Coronamaßnahmen, Arbeitszeit, Ferienzeit), Woche/Monat (Coronamaßnahmen, Jahreszeit, Ferienzeit) betrachtet werden. Dadurch soll eine Erklärungsgrundlage gefunden werden, um mögliche Schwankungen der Messwerte an einem Ort zu verschiedenen Zeitpunkten zu erklären

- (7) Visualisierung von Messwerten von unterschiedlichen Schadstoffen/Schadstoffklassen im zeitlichen Verlauf

Begründung: Durch die Visualisierung von Messwerten unterschiedlicher Schadstoffe sollen mögliche Differenzen in den verschiedenen zeitlichen Verläufen entdeckt werden. Ziel soll die mögliche Detektion der Stärke des Einflusses des Messzeitpunktes sein.

- (8) Visualisierung eines Vergleichs von Messwerten eines Schadstoffes in einem Jahr vor der Corona-Pandemie und dem Jahr 2020 zum jeweils gleichen Jahreszeitpunkt

Begründung: Durch diesen Vergleich soll untersucht werden, ob ein Einfluss dieses Ereignisses sowie der hieraus resultierenden Umstände (politische Maßnahmen wie Abstandsregelungen, Maskenpflicht, Ausgangssperre, Geschäftsschließungen) erkennbar wird. Dabei soll auch das mögliche Ausmaß der Veränderung sichtbar gemacht werden.

- (9) Visualisierung eines Vergleichs eines gemessenen Wertes eines Schadstoffes an einem Ort im Vergleich zum Durchschnitt der gemessenen Werte an allen anderen Stationen
Begründung: Ziel dieser Visualisierung ist es Besonderheiten, Gemeinsamkeit und oder Abweichungen vom Durchschnitt zu erkennen und aufzuzeigen


Neben der Anforderung für die Visualisierung stellen sich wie oben beschrieben auch gewisse Anforderungen zur Benutzung und Handhabe des Prototyps

Usabilityanforderungen

- (10) Möglichkeit zur Eingrenzung des zu betrachtenden Zeitraums für alle Visualisierungen

Begründung: Es soll möglich sein einen gewissen Zeitraum genauer zu explorieren, um den genaueren Verlauf zum Beispiel in Korrelation eins zeitlichen Ereignisses zu betrachten (z.B. Zeitraum des Lockdowns)

- (11) Auswahlmöglichkeit zur Betrachtung des Schadstoffes

Begründung: Es soll möglich sein den Schadstoff auszuwählen, dessen gemessene Werte visualisiert werden. Das ist deshalb sinnvoll, weil die verschiedenen Schadstoffe zum einen in unterschiedlichen Einheiten gemessen werden und zum anderen die verschiedenen Schadstoffe durch verschiedene Tätigkeiten verursacht werden(PM10→Verkehr, NO2→Heizöl). Ein genaueres Betrachten ist somit möglich.

- (12) Auswahlmöglichkeit der zeitlichen Aggregation für Visualisierungen über die Zeit

Begründung: Durch die unterschiedliche zeitliche Betrachtung soll es möglich sein, die Verläufe auf verschiedene Untersuchungsziele zu betrachten (z.B.: Monatliche Trends, Besondere einzelne Tage, Tageszeitunterschiede). Sie soll für alle Visualisierungen gelten, damit ein Vergleich und sinnvoller zeitlicher Zusammenhang zwischen den verschiedenen Visualisierungen hergestellt werden kann

- (13) Auswahlmöglichkeit zur Betrachtung der Messwerte eine einzelne Station
Begründung: Es soll möglich sein, je nach Untersuchungsgegenstand die passende Station auszuwählen um die dort gemessenen Werte separiert zu betrachten. Werte von anderen unwichtigen Stationen können somit von der Visualisierung ausgeschlossen bzw. können wichtige Messwerte einer Station je nach Bedarf hervorgehoben werden. 

Visualisierung

Anhand dieser Anforderungen wurde folgendes Programm (siehe Bild) zur Visualisierung der Daten und damit verbundenen Untersuchung der Hypothese implementiert. 

Für die Umsetzung von Anforderung 1 wurde ein Scatter-Geo/Bubble-Map implementiert (Bild). Dieser ist oben links in der Gesamtansicht zu sehen. Durch das Zentrum der Kreise (Scatter/Bubble) wird der Standort der Messung bzw. der Messtation(Geographische Koordinate) auf einer Karte markiert. Die Größe der Kreise zeigt dabei durchschnittlichen Messwert im gewählten Zeitraum (oben rechts) an dem jeweiligen Standort. Alternativ wurde auch die Darstellung als Choroplethenkarte in Betracht gezogen. Das wurde verworfen, da die Choroplethenkarte geographische Flächen betrachtet. Die untersuchten Messstationen messen in begrenztem Radius, sodass eine Übertragung auf eine größere geographische Fläche in diesem Fall nicht sinnvoll ist. Die Anzahl der Messstationen ist auch zu gering, um größere geographische Räume als eine Einheit zu betrachten. Die Größe des durchschnittlichen Messewerte, würde zudem bei einer Choroplethenkarte meist über Farbe codiert werden. Das würde zu Schwierigkeiten bei der exakten Unterscheidung bei ähnlichen Werten führen. Bei Kreisen unterschiedlicher Größen ist das bei geringem Unterschied für den Betrachter einfacher. Damit kann auch die Umsetzung von Anforderung 2, Vergleich der Messtationen untereinander, unterstützt werden.
Der Vorteil einer Bubble-Map ist zudem, das in die Karte herein- und herausgezoomt werden kann, sodass das exakte Umfeld einer Messstation betrachtet werden kann (z.B. Park, Autobahn usw.) Das wäre bei einer gefärbten Choroplethenkarte nur sehr schwer möglich. 
Die Bubble-Map bietet außerdem den Vorteil, dass über die Farbe der Kreise weitere Informationen visualisiert werden können. Dieser Vorteil wurde für die Umsetzung der Anforderung 13 genutzt. Die Bubbles haben zunächst einen einheitliche Farbe(schwarz). Der Prototyp wurde so programmiert, dass über ein Klick auf einen der Scatter die entsprechende Station ausgewählt werden kann. Diese Bubble erscheint nun in der Farbe Rot und die gemessenen Werteverläufe der ausgewählten Station werden nun in den unteren beiden Graphen in der gleichen Farbe (Rot) gezeigt. Dadurch wird eine farbliche Konsistenz geschaffen. Die Alternative jeder Station exakt eine individuelle Farbe wurde verworfen, da die Stationenanzahl zum einen zu hoch ist um jeder Station eine wirklich für den Betrachter auf Anhieb unterscheidbare Farben zu bieten und damit eine leichte zu entstehende Verbindung zwischen Station/Lokalität und Farbe zu gewährleisten, als auch dass die Stationen sich je nach Schadstoffklasse zu sehr von Ihrer Lokalität unterscheiden. Selbst bei nur kleinen Veränderungen wie von einer Straßenkreuzung zur nächsten Straßenkreuzung bei gleicher Benennung der Station, wäre ein Beibehalten der Farbe ein inhaltliche Irreführung auf Grund des begrenzten Messradius einer Messstation.

Für die Umsetzung der Anforderung 4-7 wurden Liniendiagramme gewählt. Liniendiagramme sind für kontinuierliche Zeitreihendaten, wie die Anzahl der Corona-Infizierten, der Todesfälle und auch der Schadstoffmesswerte, eine angemessene Visualisierung. Im folgenden Liniendiagramm (siehe Bild) wurden die Anzahl der Infizierten, die Todesfälle und die Regierungsmaßnahmen visualisiert. In blauer Farbe ist die Anzahl der Covid-19-Infizierten codiert und in Gelb die Anzahl der Todesfälle in Covid-19 zum jeweiligen Zeitpunkt. Mit grauen vertikalen Balken jeweils eine Regierungsmaßnahme. Dabei gilt für alle drei Werte, die gleiche x-Achse, welches der kalendarischen Jahresverlauf des Jahres 2020 ist. Somit wird der zeitliche Zusammenhang sehr deutlich. Die y-Achse hingegen ist nicht für alle in diesem Liniendiagramm dargestellten Informationen einheitlich: für die Anzahl der Infizierten gilt die y-Achsenskalierung auf der linken Seite, für die Anzahl der Anzahl der Todesfälle die y-Achsenskalierung auf der rechten Seite(siehe Bild). Für die unterschiedliche y-Achsenskalierung wurde sich entschieden, da bei einer einheitlichen y-Achsenskalierung, der Verlauf der Anzahl Todesfälle auf Grund des großen absoluten Unterschiedes in der Anzahl zur Anzahl der Infizierten, weniger deutlich erkennbar ist. Auch eine getrennte Darstellung der Verläufe hätte den Nachteil, dass der zeitliche Zusammenhang zwischen Infizierungsanzahl, Todesanzahl und Regierungsmaßnahme weniger sichtbar wird.

Für die gemessenen Werte eines Schadstoffes wurde folgendes Liniendiagramm programmiert. (siehe Bild)
Dabei wird auf der x-Achse als Einteilung der allgemeine kalendarische Jahresverlauf genutzt (01.01.-31.12). So ist ein direkter Vergleich von den gemessenen Werten aus dem Jahr 2019 vor der Pandemie (dargestellt als gestrichelte Linie: - - -) und den gemessenen Werten aus dem Pandemiejahr 2020 möglich (Anforderung 8). Bei exakter chronologischer Einteilung(1.1.2019 – 31.12.2020) wäre der Vergleich schwieriger ersichtlich, da nur eine kontinuierliche Linie abgebildet wäre und an zwei verschiedenen x-Positionen suchen müsste.. 
Auf der y-Achse ist entsprechend des Schadstoffes die passende Werteskalierung anhand der gemessenen Werte in der für den Schadstoff entsprechenden Einheit zu finden. Die Farbe schwarz, die Defaultfarbe aller Bubbles in der Bubble-Map, zeigt dabei den Durchschnittswert über alle Stationen hinweg. Wird wie bei der Bubble-Map beschrieben eine Station ausgewählt und dadurch diese in der Karte rot markiert, erscheint in gleichem Rot, ebenso wieder in gestrichelt, die Werte dieser Station im Jahr 2019 und in durchgezogener Linie die Werte der ausgewählten Station aus dem Jahr 2020. Durch diese Farbkonsistenz wird eine direkte inhaltliche Verbindung zwischen Karte und Liniendiagramm geschaffen. Eine Legende zeigt das zusätzlich noch einmal an. Somit ist eine Einordnung der Station zur Gesamtsituation möglich (Anforderung 9)
Eine alternative Darstellung der verschiedenen Werteverläufe in Form eines Flächendiagramms, das ebenso für Zeitreihen geeignet ist, oder in Form eines unstacked-Barcharts erwiesen sich schlecht, da der direkte Vergleich zwischen 2019 und 2020 bei gleichzeitigem Vergleich von Durchschnitt aller Stationen und einer Station, als schwierig ersichtlich sowie der ganze Graph insgesamt unübersichtlich wirkt. 
Ebenso unübersichtlich wirkte es die Wertverläufe aller gemessenen Schadstoffe in einem Graphen zu visualisieren. Die Alternative der gleichzeitigen Darstellung aller Schadstoffe in Form eines Small-Multiples wurde als gut betrachtet, in Zusammenspiel mit dem Scatter-Geo aber als unpassend. So wären auf an fast allen Koordinaten mehrere sich überlagernde Kreise, da an einer Station meist zu mehreren Schadstoffen gleichzeitig Werte erhoben wurden. Erschwerend kommt hinzu, dass an vielen Stationen nicht allen Schadstoffe aufgezeichnet worden sind. 

Um dennoch alle Schadstoffe berücksichtigen zu können (Anforderung 11), wurde folgendes Bedienelement implementiert (Bild). Dort ist es möglich exakt einen der Schadstoffe auszuwählen. Je nach Auswahl zeigen die Karte als auch die unteren beiden Linegraphen die entsprechenden Werte des ausgewählten Schadstoffes an. Ebenso ist es möglich den betrachteten Zeitraum über das Bedienungselement einzuschränken (Anforderung 10). Alle Graphen passen sich dem entsprechend an um auch hier wieder eine zeitliche Konsistenz zu gewährleisten. Ebenso ist es hier möglich, die zeitliche Aggregation zu bestimmen (Anforderung 11). Auswahl besteht zwischen Tag, Woche, Monat. Das wirkt sich auch hier auf alle Graphen aus, ist aber besonders wichtig für den untersten Linegraph (sieh Bild). Dieser zeigt je nach Auswahl den durchschnittlichen Verlauf innerhalb eines Tages (0.00 Uhr bis 23.59), einer Woche (Montag bis Sonntag) oder innerhalb eines Monats (1. Tag des Monats bis zum 31. Tag eines Monats an) an. Wie beim obendrüber sich befindlichen Linegraph werden alle dort bekannten Visualisierungsmuster übernommen (schwarz gestrichelt: Durchschnittlicher Werteverlauf von allen Stationen 2019, schwarz durchgezogen: Durchschnittlicher Werteverlauf von allen Stationen 2020, rot gestrichelt: Werteverlauf der im Scatter-Geo ausgewählten Station 2019, rot durchgezogen: Werteverlauf der im Scatter-Geo ausgewählten Station 2020)

In der Infobox (siehe Bild) wird zur Schlagzahleinordnung und groben Zusammenfassung die absoluten Zahlen zum Durchschnittsmesswert aller Stationen entsprechend dem ausgewählten Schadstoff im gewählten Zeitraum angezeigt. Ebenso wird in tabellarischer Form die absoluten Zahlen der Covid-19-Infizierten und Todesfälle mit Covid-19 in dem gewählten Zeitraum angezeigt.

Tools

Für die Umsetzung der Visualisierung wurden hauptsächlich Tools gesucht, die eine hohe Interaktivität zwischen den verschiedenen Graphen bietet, sodass ein Benutzer, schnell die Ansicht seiner Wahl erhält. Deshalb kamen Altair, plotly/dash als auch d3.js in Betracht. Altair ist ein Visualisierungsbibliothek in Python welche auf auf Vega/Vega-Lite basiert. Mit Altair ist es mit sehr geringem Implementieraufwand möglich alle gängigen Visualisierungstypen zu implementieren. Allerdings sind bei der Interaktivität und der Individualisierung der einzelnen Visualisierungen schnell die Grenzen erreicht. Das wäre bei d3.js nicht der Fall. D3 bietet alle Freiheiten der Gestaltung und Implementierung. Allerdings ist der Programmieraufwand sehr hoch. Hinzukommt, dass das Erlernen sich als schwierig gestaltet auf Grund von schwächen in der Dokumentation und Inkompatibilitäten von Versionen. 
Deshalb wurde dieser Prototyp mit plotly/Dash implementiert. Plotly ist ein mächtige Visualisierungsbibliothek in der Programmiersprache Python, welches die Möglichkeit zu Realisierung aller bekannten Visualisierungstechnicken mit großer Möglichkeit zur Individualisierung bietet. Über das damit verbundene Framework Dash, lassen sich die mit Plotly programmierten Visualisierung in HTML-Seiten einbinden und gleichzeitig Interaktivität zwischen den Graphen herstellen (Bild). Über CSS lässt sich zudem das weitere Erscheinungsbild neben der Graphen komplett individualisieren. Darüber hinaus bestand innerhalb des Teams Erfahrung mit Python sowie mit plotly/Dash.
