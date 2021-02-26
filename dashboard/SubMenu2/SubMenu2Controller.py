import dash_html_components as html

class sub2ControllerClass:
    def __init__(self):
        self

    def getContent(self,pathname):
        if pathname == "/page-2/1":
            return html.P("Oh cool, this is page 2.1!")
        elif pathname == "/page-2/2":
            return html.P("No way! This is page 2.2!")