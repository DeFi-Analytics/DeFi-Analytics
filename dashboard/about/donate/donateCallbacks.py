from dash.dependencies import Input, Output, State
import pyperclip

class donateCallbacksClass:
    def __init__(self, app):

        @app.callback(Output('inputDonateAddress', 'value'),
                      [Input('buttonCopyAddress', 'n_clicks'),
                       Input('inputDonateAddress', 'value')])
        def copyAdressToClipboard(buttonClicked, donateAddress):
            pyperclip.copy(donateAddress)
            return donateAddress