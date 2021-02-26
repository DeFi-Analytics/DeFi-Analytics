import dash_html_components as html
import dash_core_components as dcc

class content1ViewClass:
    def __init__(self):
        self.content = [html.I("Try typing in input 1"),
                            html.Br(),
                            dcc.Input(id="input1", type="text", placeholder=""),
                            html.Div(id="output")]


