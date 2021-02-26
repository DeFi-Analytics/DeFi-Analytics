import dash_html_components as html
from .Content1.content1View import content1ViewClass
from .Content1.content1Callbacks import content1CallbacksClass

class sub1ControllerClass:
    def __init__(self, app):
        self.app = app
        self.content1View = content1ViewClass()

        self.content1Callbacks = content1CallbacksClass()       # create callbacks on top level
        self.content1Callbacks.register_callbacks(app)


    def getContent(self,pathname):
        if pathname in ["/", "/page-1/1"]:
            return self.content1View.content
        elif pathname == "/page-1/2":
            return html.P("This is the content of page 1.2. Yay!")