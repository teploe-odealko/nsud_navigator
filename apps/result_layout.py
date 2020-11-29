import json

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import requests
import visdcc
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
# import settings
import ast
import configparser
import json
config = configparser.ConfigParser()
config.read('confg.ini')
open_data_cat_eng = ast.literal_eval(config['CATEGORIES']['open_data_eng'])
open_data_cat_rus = ast.literal_eval(config['CATEGORIES']['open_data_rus'])
open_data_decs = ast.literal_eval(config['CATEGORIES_DESCRIPTION']['open_data_desc'])
with open('goverment.json') as json_file:
    # contents = json_file.read()
    # goverment = ast.literal_eval(contents)
    goverment = json.load(json_file)

goverment_df = pd.DataFrame.from_dict(goverment, orient='index')
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
            dbc.CardBody(
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
    ], style={'min-width' : '30rem'}
)

result_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [

                        dbc.Row([
                            dbc.Col(
                                dbc.DropdownMenu(
                                    label="Категории",
                                    children=[
                                        dbc.Row(dbc.Col(tabs), style={'margin-top': '1rem'})
                                    ], style={'height': "100%"}
                                ),
                                width={"size": 2},
                            ),
                            dbc.Col(
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupAddon("@", addon_type="prepend"),
                                        dbc.Input(placeholder="Поиск", id = "input_search1"),
                                    ],
                                    size="lg",
                                ),
                                width=5
                            ),

                            dbc.Col(
                                dbc.Button("Найти", outline=True, color="primary", id='btn_search1',
                                           style={'width': '100%', 'height' : '100%'}),
                                width={"size": 2},
                            ),
                        ]),
                        dbc.CardGroup(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col(html.H6("Количество наборов", className="card-title"), width=9),
                                            dbc.Col(html.H6(len(goverment)), width=3)
                                        ], justify="between")
                                    ]
                                ),
                                color="primary", outline=True
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col(html.H6("Количество тематик", className="card-title"), width=9),
                                            dbc.Col(
                                                html.H6(len(set([goverment[key]['subject'] for key in goverment]))
                                                ), width=3)
                                        ], justify="between")
                                    ]
                                ),
                                color="primary", outline=True
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col(html.H6("Количество ведомств", className="card-title"), width=9),
                                            dbc.Col(
                                                html.H6(len(set([goverment[key]['creator'] for key in goverment]))
                                            ), width=3)
                                        ], justify="between")
                                    ]
                                ),
                                color="primary", outline=True
                            ),
                        ], style={'margin':'1rem 0rem'}
                    ),
                        # dbc.Row([
                        #     dbc.Col(html.H6('Количество наборов: ' + str(len(goverment))), style={'color': 'gray'}),
                        #     dbc.Col(html.H6('Количество наборов: ' + str(len(goverment))), style={'color': 'gray'}),
                        #     dbc.Col(html.H6('Количество наборов: ' + str(len(goverment))), style={'color': 'gray'}),
                        # ], style={'margin-top': '1rem'}),
                        dbc.Row(dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2("Наборы данных", className="card-title"),
                                        dbc.Row([make_list_item('https://data.gov.ru/', goverment[key]['title']) for key in goverment], id="datasets_result")
                                    ]
                                )
                            )
                        ))
                        #
                    ],
                    style={'margin-top': '2rem', 'margin-left': '2rem'},
                    width=7
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

    charts_content = html.Div([
    dbc.Row(
        [
            # dbc.Col(
            #     # dbc.Card(
            #     #     dbc.CardBody(
            #     #         [
            #     #             html.H2("Наборы данных", className="card-title"),
            #     #             dbc.Row([make_list_item('https://data.gov.ru/', goverment[key]['title']) for key in goverment])
            #     #         ]
            #     #     )
            #     # ),
            #     width=6
            # ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("Карта данных", className="card-title"),
                            visdcc.Network(id = 'net',
                                 options = dict(
                                     layout = dict (hierarchical = 'true'),
                                     physics=dict(
                                         repulsion=dict(springConstant=5)
                                     ),
                                     edges=dict(
                                         length=250
                                     ),
                                     nodes=dict(color='#33A2B8', font = dict(color="white")),
                                     height= '600px', shape = 'circle', size = '80',
                                     scaling = dict(min = '300', max = '500',
                                                    label = dict(enabled = 'true', min = '14', max ='500', maxVisible = '30', drawThreshold = '5'),

                                        customScalingFunction = "function (min,max,total,value) {\
                            if (max === min) {\
                              return 0.5;\
                            }\
                            else {\
                              let scale = 1 / (max - min);\
                              return Math.max(0,(value - min)*scale);\
                            }\
                          }")))
                        ]
                    )
                ), style={'margin-top': '6rem'}
            )
        ],
        style={'padding-right':'1rem'}
    )
    ])

    if button_id == "group-0-toggle" and n1:
        return not is_open1, False, False, charts_content
    elif button_id == "group-1-toggle" and n2:
        return False, not is_open2, False, charts_content
    elif button_id == "group-2-toggle" and n3:
        return False, False, not is_open3, charts_content
    return False, False, False, ''


@app.callback(
    Output('net', 'data'),
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(len(open_data_cat_rus))])
def myfun(n1, n2, n3):
    departments_set = list(set([goverment[key]['creator'] for key in goverment]))

    departments_set_short = []
    for i, dep in enumerate(departments_set):
        tmp_list = [word[0:6] for word in departments_set[i].split()]
        tmp_list.insert(int(len(tmp_list)/3), '\n')
        tmp_list.insert(2*int(len(tmp_list)/3), '\n')
        departments_set_short.append(' '.join(tmp_list))

    l1 = list(range(len(departments_set)))
    l2 = l1.copy()
    l2.insert(0,l2.pop())

    for dep in departments_set:
        # print(dep)
        print(goverment_df[goverment_df['creator'] == dep]['title'].values)
    data ={'nodes':[{'id': i, 'label':item} for i, item in enumerate(departments_set_short)],
           'edges':[{'id':f"{i}-{j}", 'from': i, 'to': j} for i, j in zip(l1,l2)]
           }
    return data

@app.callback(
    Output("collapse_list", "is_open"),
    [Input("collapse_list_btn", "n_clicks")],
    [State("collapse_list", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("datasets_result", "children"),
    [Input("btn_search1", "n_clicks")],
    [State("input_search1", "value")],
)
def search(btn, value):
    headers = {
      'Content-Type': 'application/json',

    }
    uri = 'http://localhost:9200/test_index/_search'
    query = json.dumps({
       "query": {
        "multi_match": {
          "query": value,
          "fuzziness": "auto",
          "fields": [
            "title^3",
            "description^2",
            "data_scheme",
            "creator"
          ]
        }
      }
    })
    response = requests.get(uri, data=query, headers=headers)
    try:
        hits = json.loads(response.text)['hits']['hits']
    except:
        return ''
    # print(len(hits))
    # return dash.no_update
    # print([hit['_source']['title'] for hit in hits])
    # print(hits)
    # print(type(hits))
    # try:
    #     hits = hits.reverse()
    # except TypeError:
    #     print('hits is none')
    #     return ''
    # print(hits)
    # if type(hits) == type([]):
    res = [make_list_item('https://data.gov.ru/', hit['_source']['title']) for hit in hits]
    print(res)
    res.reverse()
    return res
    # return dash.no_update
    # return ;
