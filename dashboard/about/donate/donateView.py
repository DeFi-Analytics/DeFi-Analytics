import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


class donateViewClass:

    def getDonateContent(self):
        content = [dbc.Card(dbc.CardBody([html.H4("Donation"),
                             html.Div([html.P(['If you want to support this project, you can send me DFI on the following address:']),
                                       dbc.InputGroup([dbc.InputGroupAddon(dbc.Button("Copy", id="buttonCopyAddress"), addon_type="append",),
                                             dbc.Input(id="inputDonateAddress", value="dDqcZ64xoqMyHmzpacWnnkBvVoRX8xojQ4", disabled=True)]),
                                       html.P(['After the first deposit I will also make an evaluation and put it here to track the made donations.']),
                                       ])]))]
        return content

