import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import visdcc
import json
import ast

app = dash.Dash()
# with open('schema.json', 'r', encoding='utf-8') as f:
#     schema = json.load(f)
with open('schema.json', 'r', encoding='utf-8') as json_file:
        contents = json_file.read()
        schema = ast.literal_eval(contents)
sc_list = []
i = 0
# for elem in schema:
#     sc_list.append({'id': i, 'label': elem['creator']})
#     i += 1
sc_list = set([schema[key]['creator'] for key in schema])
app.layout = html.Div([
      visdcc.Network(id = 'net',
                     options = dict(autoResize = 'true', height= '600px', width= '800px', layout = dict (hierarchical = 'true'), shape = 'circle', size = '60',
                     scaling = dict(min = '100', max = '200', label = dict(enabled = 'true', min = '14', max ='500', maxVisible = '30', drawThreshold = '5'),
                     customScalingFunction = "function (min,max,total,value) {\
        if (max === min) {\
          return 0.5;\
        }\
        else {\
          let scale = 1 / (max - min);\
          return Math.max(0,(value - min)*scale);\
        }\
      }"))),
      dcc.Input(id = 'label',
                placeholder = 'Enter a label ...',
                type = 'text',
                value = ''  ),
      html.Br(),html.Br(),
      dcc.RadioItems(id = 'color',
                     options=[{'label': 'Red'  , 'value': '#ff0000'},
                              {'label': 'Green', 'value': '#00ff00'},
                              {'label': 'Blue' , 'value': '#0000ff'} ],
                     value='Red'  )
])

@app.callback(
    Output('net', 'data'),
    [Input('label', 'value')])
def myfun(x):
    data ={'nodes':[{'id': i, 'label':item} for i, item in enumerate(sc_list)],
           'edges':[{'id':'1-3', 'from': 1, 'to': 3},
                    {'id':'1-2', 'from': 1, 'to': 2},
                    {'id':'4-3', 'from': 4, 'to': 3}]
           }
    return data
    return data

@app.callback(
    Output('net', 'options'),
    [Input('color', 'value')])
def myfun(x):
    return {'nodes':{'color': x}}

if __name__ == '__main__':
    app.run_server()
