import dash
import dash_bootstrap_components as dbc
from appIndexString import appIndexStringClass

# link fontawesome to get the chevron icons
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
app.index_string = appIndexStringClass.getAppIndexString()
server = app.server