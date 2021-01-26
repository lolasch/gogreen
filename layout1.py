app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[


    html.Div(
        style={
            'display': 'block',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'text-align': 'center'
        }, children=[
            html.Div(style={'display':'flex'},children=[
                html.Div(style = {'flex':1.5},children=[
                    #html.H1('Decelerate.',style={'margin-bottom':'-10px', 'text-align':'left'}),
                    html.H2('Decelerate.',
                            style={'margin-bottom': '-10px', 'text-align': 'left'}),
                    html.H2('Air quality in Barcelona during a pandemic.',
                            style={'text-align': 'left'}),
                ]),
                html.Div(style={'flex':0.5},children=[
                    html.Img(style={
                        'width': 150,
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                        'text-align': 'center'
                    }, src=app.get_asset_url('pfennigelius.png')),
                ]),
                html.Div(
                    style={'flex':1}, children=[
                        #html.H4("Choose a time period:", style={'padding-bottom': '0px', 'margin-bottom':'0px'}),
                        html.Div(style={'display':'flex', 'padding-top':'20px', 'padding-right':'15px'},children=[
                            html.Div(style={'flex-basis':'10%'}, children=[
                                dcc.Input(
                                    id='startTag',
                                    type="number",
                                    value=1,
                                    min=1,
                                    step=1,
                                ), ]),
                            html.Div(style={'flex-basis':'30%'}, children=[
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
                                    clearable=False,
                                ), ]),
                            html.H3("-",style={'flex-basis':'10%', 'margin-top':'0px'}),
                            html.Div(style={'flex-basis':'10%'}, children=[
                                dcc.Input(
                                    id='endTag',
                                    type="number",
                                    value=31,
                                    min=1,
                                    step=1,
                                ), ]),
                            html.Div(style={'flex-basis':'30%'}, children=[
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
                                    clearable=False,
                                ), 
                            ]),
                        ]),
                        dcc.RadioItems(
                            inputStyle={
                                # 'textAlign': 'center',
                                # 'color': colors['text'],
                                'margin-left': '10px',
                                'margin-top': '10px'
                            },
                            id="zeitabschnitt",
                            options=[
                                {'label': 'Day', 'value': 'Tag'},
                                {'label': 'Week', 'value': 'Woche'},
                                {'label': 'Month', 'value': 'Monat'}
                            ],
                            value='Woche',
                            labelStyle={'display': 'inline-block'}
                        ),
                        dcc.RadioItems(
                            inputStyle={
                                # 'textAlign': 'center',
                                # 'color': colors['text'],
                                'margin-left': '10px',
                                'margin-top': '10px'
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
                ]),
            ])
        ], className="row"),
    html.Hr(),

    html.Div(children=[
        html.Div(children=[
            html.Div(
                #style={'border-style': 'solid', 'border-color': 'grey', 'border-width': '1px'},
                children=[
                    html.Div(
                        style={'display': 'flex'},
                        children=[
                            html.Div(  # Karte
                                style={'width': '30%'},
                                children=[dcc.Graph(id='g1')],
                                className="flex-child"
                            ),
                            html.Div(  # Infobox
                                style={'width': '20%', 'padding': '20px'},
                                children=[html.H3("Infobox"),
                                        html.Ul(id='infobox'),
                                        html.Button('remove station', id='reset',style={'display': 'none'},hidden=True)],
                                className="flex-child"
                            ),
                            html.Div(
                                style={'width': '50%', 'padding': '20px'},
                                children=[
                                    # Zeitstrahl
                                    html.Div([dcc.Graph(id="corona")]),
                                ], className="flex-child")
                        ], className="flex-container"),
                ]
            )], className="row"),

        html.Div([
            html.Div([dcc.Graph(id="zeitstrahl"),  # Corona-Graph

                    html.Div([dcc.Graph(id="zeitverlauf")]),  # Zeitverlauf
                    ],
                    className="row"
                    ),
        ], className="row"
        ),
    ]),
    html.Div(id='ortDiv', style={'display': 'none'}, className="row"),
    
])
