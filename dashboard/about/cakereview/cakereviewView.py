import dash_html_components as html
import dash_bootstrap_components as dbc

import os
import base64


class cakereviewViewClass:

    def getCakereviewContent(self):
        content = [dbc.Card(dbc.CardBody([dbc.Row(dbc.Col(self.createCakereviewContent()))]))]
        return content

    @staticmethod
    def createCakereviewContent():
        workDir = os.path.abspath(os.getcwd())
        image_filename = workDir + '/assets/'+'screenshotCakedefiReview.png'
        encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

        contentCakereview = [html.H4("Cakedefi-Review"),
                             html.Div([html.P(['The origin DefiChain-Analytics was ', html.A('https://www.cakedefi-review.com/', href='https://www.cakedefi-review.com/', target='_blank'),
                                               ', which will continue to exists. But in future only with content regarding CakeDeFi.',]),
                                       html.A(html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'display': 'block', 'max-width': '100%', 'height': 'auto'}), href='https://www.cakedefi-review.com/', target='_blank'),])]
        return contentCakereview