app.layout = html.Div(style={'backgroundColor': colors['background']},children=[

    html.Img(style={
        'width': 250,
        'display': 'block',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'text-align': 'center'
    }, src=app.get_asset_url('gogreen.png')),

    html.Div(children='Luftqualität während einer Pandemie.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(
        style={
            'display': 'block',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'text-align': 'center'
        }, children=[
            # Radio mit Auswahlmöglichkeit für Luftverschmutzungsart
            dcc.RadioItems(
                inputStyle={
                    #'textAlign': 'center',
                    #'color': colors['text'],
                    'margin-left' : '10px'
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
                inputStyle={
                    #'textAlign': 'center',
                    #'color': colors['text'],
                    'margin-left' : '10px'
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
        ], className="row"),
    html.Div(
        style={
            'display' : 'flex',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'text-align': 'center',
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
            html.Div(style={'flex':'1', 'width': "5%",'margin-right':'0px', 'margin-left' : '10px'},children = [
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

    html.Div([
        html.Div(
            #style={'border-style': 'solid', 'border-color': 'grey', 'border-width': '1px'}, 
            children=[
                html.Div(
                    style={'display': 'flex'}, 
                    children=[
                        html.Div( # Karte
                            style={'width': '60%'},
                            children=[dcc.Graph(id='g1')], 
                            className="flex-child"
                        ),
                        html.Div( #Infobox
                            style={'width': '40%','padding': '20px'}, 
                            children=[html.H3("Infobox"),
                            html.Ul(id='infobox')], 
                            className="flex-child"
                        ),
                    ], className="flex-container"),
                html.Div([dcc.Graph(id="corona"), #Corona-Graph
                ]
            )], className="six columns"),

        html.Div([
            html.Div([dcc.Graph(id="zeitstrahl")]), #Zeitstrahl
            html.Div([dcc.Graph(id="zeitverlauf")]), #Zeitverlauf
            ],
            className="six columns"
        ),
        ],className="row"
    ),
        html.Div(id='ortDiv', style={'display': 'none'},className="row"),
])
