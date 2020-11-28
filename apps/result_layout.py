import json

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
# import settings
import ast
import configparser
config = configparser.ConfigParser()
config.read('confg.ini')
open_data_cat_eng = ast.literal_eval(config['CATEGORIES']['open_data_eng'])
open_data_cat_rus = ast.literal_eval(config['CATEGORIES']['open_data_rus'])
open_data_decs = ast.literal_eval(config['CATEGORIES_DESCRIPTION']['open_data_desc'])
# print(config['CATEGORIES']['open_data_rus'])
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        open_data_cat_rus[i],
                        color="light",
                        id=f"group-{i}-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody([
                    dbc.Row(open_data_decs[i]),
                    dbc.Button(
                        "Подробнее",
                        id=f"group-{i}-btn",
                        style={'margin-top': '1rem'}
                    )
                ]),
                id=f"collapse-{i}",
                style={'padding': '1rem'}
            ),
        ]
    )

def make_list_item(link, title):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    html.A(
                        dbc.Button(
                            title,
                            color="light",
                            id=link,
                        ), href=link
                    )
                )
            ),
        ],
        style={'width' : '100%'}
    )


tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [make_item(i) for i in range(len(open_data_cat_rus))], className="accordion"
            )
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Ведомства"),
        dbc.Tab(tab2_content, label="Открытые данные"),
    ]
)

result_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col(
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupAddon("@", addon_type="prepend"),
                                        dbc.Input(placeholder="Поиск", id = "input_search1"),
                                    ],
                                    size="lg",
                                ),
                                width=10
                            ),
                            dbc.Col(
                                dbc.Button("Найти", outline=True, color="primary", id='btn_search1',
                                           style={'width': '100%', 'height' : '100%'}),
                                width={"size": 2},
                            )
                        ]),
                        dbc.Row(dbc.Col(tabs), style={'margin-top': '1rem'})
                    ],
                    style={'margin-top': '2rem', 'margin-left': '2rem'},
                    width=5
                ),
                dbc.Col(html.Div(id='charts'))
            ]
        )

    ],
    style={'margin-top': '6rem'},
    id="search",
)

layout = html.Div([result_content])

toggle_output = [Output(f"collapse-{i}", "is_open") for i in range(len(open_data_cat_rus))]
toggle_output.append(Output('charts', 'children'))
@app.callback(
    toggle_output,
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(len(open_data_cat_rus))],
    [State(f"collapse-{i}", "is_open") for i in range(len(open_data_cat_rus))],
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False, ''
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    with open('goverment.json') as json_file:
        contents = json_file.read()
        goverment = ast.literal_eval(contents)
        # print(goverment)

    card_content_sets = [
        dbc.CardHeader("Количество наборов"),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col(html.H1(len(goverment), className="card-title")),
                    dbc.Col(dbc.Button("Развернуть", color="primary", id='collapse_list_btn'))
                ])
            ]
        ),
    ]

    departments_set = set([goverment[key]['creator'] for key in goverment])
    # print(departments_set)

    card_content_deps = [
        dbc.CardHeader("Количество ведомств"),
        dbc.CardBody(
            [
                html.H1(len(departments_set), className="card-title"),
            ]
        ),
    ]

    subjects_set = set([goverment[key]['subject'] for key in goverment])
    # print(departments_set)

    card_content_subj = [
        dbc.CardHeader("Количество тематик"),
        dbc.CardBody(
            [
                html.H1(len(subjects_set), className="card-title"),
            ]
        ),
    ]

    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(card_content_sets, color="light")),
                    dbc.Col(dbc.Card(card_content_subj, color="light")),
                    dbc.Col(dbc.Card(card_content_deps, color="light"))
                ]
            ),
        ], style={'margin' : '2rem', 'margin-left': '1rem', 'width': '100%'}

    )

    for key in goverment:
        print(goverment[key]['subject'])
    charts_content = html.Div([
        dbc.Row(cards),
        dbc.Collapse(
            dbc.Row([make_list_item('https://data.gov.ru/', goverment[key]['title']) for key in goverment]),
            id="collapse_list", style={'margin': '1rem', 'margin-right': '2rem'}
        ),
    ])

    if button_id == "group-0-toggle" and n1:
        return not is_open1, False, False, charts_content
    elif button_id == "group-1-toggle" and n2:
        return False, not is_open2, False, charts_content
    elif button_id == "group-2-toggle" and n3:
        return False, False, not is_open3, charts_content
    return False, False, False, ''


@app.callback(
    Output("collapse_list", "is_open"),
    [Input("collapse_list_btn", "n_clicks")],
    [State("collapse_list", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
