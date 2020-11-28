import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app

search_content = html.Div(
    [
        dbc.Row([
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("@", addon_type="prepend"),
                        dbc.Input(placeholder="Поиск", id='input_search'),
                    ],
                    size="lg",
                    className="mb-3",
                )
            ),
        ], style={'margin-top': '20rem', 'margin-right': '20rem', 'margin-left': '20rem'}),
        dbc.Row(
            dbc.Col(
                dbc.Button("Найти", outline=True, color="primary", className="mr-1", id='btn_search',
                           style={'width': '100%', 'margin-top': '1rem'}),
                width={"size": 2, "offset": 5},
            )
        )
    ],
    id="search",
)

layout = html.Div([search_content])

@app.callback(
    [Output("url", "pathname")],
    Input("btn_search", "n_clicks"),
    State("input_search", "value")
)
def render_page_content(n, value_new):
    global value
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    # settings.value = value_new
    if "btn_search" in changed_id and n is not None:
        return "/page-2",
    else:
        return dash.no_update
