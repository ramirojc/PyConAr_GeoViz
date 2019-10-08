import dash
import dash_core_components as dcc
import dash_html_components as html

from plotly import graph_objs as go

import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('./data/2014_world_gdp_with_codes.csv')

app.layout = html.Div([

    html.H1("Mapas"),

    dcc.Graph(
        figure= go.Figure(
            data = [
                go.Scattergeo(
                    lat=[-31.44234],
                    lon=[-64.19320],
                )
            ]
        )
    ),

    dcc.Graph(
        figure= go.Figure(
            data = [
                go.Choropleth(
                    locations = df.CODE,
                    z = df.GDP,
                    text = df.COUNTRY
                )
            ]
        )
    ),


])

if __name__ == '__main__':
    app.run_server(debug=True)