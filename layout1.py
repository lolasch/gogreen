app.layout = html.Div(style={'backgroundColor': colors['background']},children=[

    


    html.Div(
        style={
            'display': 'block',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'text-align': 'center'
        }, children=[
            html.Div([
                #html.H1('Decelerate.',style={'margin-bottom':'-10px', 'text-align':'left'}),
                html.H2('Slow down - take a deep breath.',style={'margin-bottom':'-10px', 'text-align':'left'}),
                html.H2('Air quality in Barcelona during a Pandemic.',style={'margin-bottom':'00px', 'text-align':'left'}),
            ],className= "six columns"),
            # Radio mit Auswahlmöglichkeit für Luftverschmutzungsart
            
            # Radio mit Auswahlmöglichkeit für Tag/Woche/Monat
            
            html.Div(
                style={
                    'display' : 'flex',
                    'margin-left': 'auto',
                    'margin-right': 'auto',
                    'text-align': 'center',
                    'margin-top':'30px',
                    'width' : '500px',
                }, children=[
                    html.Div(style={'flex':'1', 'width': '0px', 'margin-right':'0px', 'padding-right':'0px'},children = [
                        dcc.Input(
                            id='startTag',
                            type = "number",
                            value= 1,
                            min = 1,
                            step = 1
            ),],className = "six columns"),
            html.Div(style={'flex':'1', 'width': "40%", 'margin-left' : '0px','margin-right':'10px'},children = [
                dcc.Dropdown(
                    id='start',
                    options=[
                        {'label': 'January', 'value': '1'},
                        {'label': 'February', 'value': '2'},
                        {'label': 'March', 'value': '3'},
                        {'label': 'April', 'value': '4'},
                        {'label': 'May', 'value': '5'},
                        {'label': 'June', 'value': '6'},
                        {'label': 'July', 'value': '7'},
                        {'label': 'August', 'value': '8'},
                        {'label': 'September', 'value': '9'},
                        {'label': 'October', 'value': '10'},
                        {'label': 'November', 'value': '11'},
                        {'label': 'December', 'value': '12'}
                    ],
                    value='1',
                    clearable = False,
            ),],className = "six columns"),
            html.Div(style={'flex':'1', 'width': "5%",'margin-right':'0px','margin-left' : '10px'},children = [
                dcc.Input(
                    id='endTag',
                    type = "number",
                    value= 31,
                    min = 1,
                    step = 1
            ),],className = "six columns"),
            html.Div(style={'flex':'1', 'width': "40%", 'margin-left' : '0px'},children = [
                dcc.Dropdown(
                    id='ende',
                    options=[
                        {'label': 'January', 'value': '1'},
                        {'label': 'February', 'value': '2'},
                        {'label': 'March', 'value': '3'},
                        {'label': 'April', 'value': '4'},
                        {'label': 'May', 'value': '5'},
                        {'label': 'June', 'value': '6'},
                        {'label': 'July', 'value': '7'},
                        {'label': 'August', 'value': '8'},
                        {'label': 'September', 'value': '9'},
                        {'label': 'October', 'value': '10'},
                        {'label': 'November', 'value': '11'},
                        {'label': 'December', 'value': '12'}
                    ],
                    value='12',
                    clearable = False,
            ),],className = "six columns"),
            
        ], className="row"),
        dcc.RadioItems(
                inputStyle={
                    #'textAlign': 'center',
                    #'color': colors['text'],
                    'margin-left' : '10px',
                    'margin-top' : '10px'
                },
                id="zeitabschnitt",
                options=[
                    {'label': 'Day', 'value': 'Tag'},
                    {'label': 'Week', 'value': 'Woche'},
                    {'label': 'Month', 'value': 'Monat'}
                ],
                value='Tag',
                labelStyle={'display': 'inline-block'}
            ),
        dcc.RadioItems(
                inputStyle={
                    #'textAlign': 'center',
                    #'color': colors['text'],
                    'margin-left' : '10px',
                    'margin-top' : '10px'
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
        ], className="row"),
    html.Hr(),

    html.Div([
        html.Div(
            #style={'border-style': 'solid', 'border-color': 'grey', 'border-width': '1px'}, 
            children=[
                html.Div(
                    style={'display': 'flex'}, 
                    children=[
                        html.Div( # Karte
                            style={'width': '30%'},
                            children=[dcc.Graph(id='g1')], 
                            className="flex-child"
                        ),
                        html.Div( #Infobox
                            style={'width': '20%','padding': '20px'}, 
                            children=[html.H3("Infobox"),
                            html.Ul(id='infobox')], 
                            className="flex-child"
                        ),
                        html.Div(
                            style={'width': '50%','padding': '20px'}, 
                            children=[
                            html.Div([dcc.Graph(id="corona")]), #Zeitstrahl
                        ],className="flex-child")
                    ], className="flex-container"),
                
                ]
            )], className="row"),

        html.Div([
            html.Div([dcc.Graph(id="zeitstrahl"), #Corona-Graph
            
            html.Div([dcc.Graph(id="zeitverlauf")]), #Zeitverlauf
            ],
            className="row"
        ),
        ],className="row"
    ),
        html.Div(id='ortDiv', style={'display': 'none'},className="row"),
    
])
