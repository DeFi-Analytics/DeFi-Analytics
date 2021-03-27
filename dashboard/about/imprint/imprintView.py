import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go


class imprintViewClass:

    def getImprintContent(self):
        content = [dbc.Card(dbc.CardBody([dbc.Row(dbc.Col(self.createImprintContent())),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoOverview")))]))]
        return content

    @staticmethod
    def createImprintContent():
        contentImprint = [html.H4("Imprint"),
                          html.P(['The website defichain-analytics.com is operated by:', html.Br(),
                                  'Daniel Zirkel', html.Br(),
                                  'Oeschelbronner Weg 4', html.Br(),
                                  '75446 Wiernsheim' , html.Br(),
                                  'Germany', html.Br()]),
                          html.P(['Telegram: ', html.A('https://t.me/DanielZirkel', href='https://t.me/DanielZirkel', target='_blank'), html.Br(),
                                  'e-mail: cakereviewdashboard@gmail.com']),
                          html.P(['Responsible for the contents in the sense of § 5 TMG § 18 Abs. 2 MStV:',html.Br(),
                                  'Daniel Zirkel']),
                          html.P(['1. limitation of liability', html.Br(),
                                  'The contents of this website are created with the greatest possible care. However, the provider does not guarantee the accuracy, completeness and '
                                  'timeliness of the content provided. The use of the contents of the website is at the user''s own risk. Contributions identified by name reflect the '
                                  'opinion of the respective author and not always the opinion of the provider. The mere use of the provider''s website does not constitute any '
                                  'contractual relationship between the user and the provider.']),
                          html.P(['2. external links', html.Br(),
                                  'This website contains links to third-party websites ("external links"). These websites are subject to the liability of the respective operators. '
                                  'When the external links were first created, the provider checked the external content for any legal violations. At that time, no legal violations'
                                  'were apparent. The provider has no influence on the current and future design and content of the linked pages. The inclusion of external links '
                                  'does not imply that the provider adopts the content behind the reference or link as its own. It is not reasonable for the provider to constantly '
                                  'monitor the external links without concrete evidence of legal violations. However, such external links will be deleted immediately if legal '
                                  'violations become known']),
                          html.P(['3. copyrights and ancillary copyrights', html.Br(),
                                  'The contents published on this website are subject to German copyright and ancillary copyright law. Any use not permitted by German copyright '
                                  'and ancillary copyright law requires the prior written consent of the provider or the respective copyright holder. This applies in particular '
                                  'to the copying, editing, translation, storage, processing or reproduction of content in databases or other electronic media and systems. '
                                  'Contents and rights of third parties are marked as such. The unauthorized reproduction or distribution of individual content or complete pages '
                                  'is not permitted and is punishable by law. Only the production of copies and downloads for personal, private and non-commercial use is '
                                  'permitted. The display of this website in external frames is only permitted with written permission.']),
                          ]


        return contentImprint