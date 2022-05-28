import dash_html_components as html
import dash_bootstrap_components as dbc

from dash_table.Format import Format, Group
from dash_table import DataTable

class cfpViewClass:

    def getCFPContent(self, data):
        content = [dbc.Card(dbc.CardBody([dbc.Row(dbc.Col(self.createCFPTableContent(data)))]))]
        return content

    @staticmethod
    def createCFPTableContent(data):
        listLinks = []
        listResult = []
        listDFI = []
        for index, row in data.iterrows():
            listLinks.append(html.A(html.P('Link'),href=data.loc[index,'Link to github'],target='_blank', className='defiLink'))
            if data.loc[index,'result'] == 'passed':
                listResult.append(html.B(data.loc[index, 'result'], style={'color': 'green'}))
            else:
                listResult.append(html.B(data.loc[index,'result'],style={'color': 'red'}))
            listDFI.append(html.Div("{:,.0f}".format(data.loc[index,'dfi']), style={'text-align': 'end'}))

        data['Github'] = listLinks
        data['Result'] = listResult
        data['DFI'] = listDFI

        data2Show = data[['#','Title','Requester','Github','DFI','Result']]

        cfpDataTable = dbc.Table.from_dataframe(data2Show, striped=True, bordered=True, hover=True)
        contentChangelog = [html.H4("CFP List"),
                            cfpDataTable]
        return contentChangelog