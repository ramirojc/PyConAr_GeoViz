import dash
import dash_core_components as dcc
import dash_html_components as html

from plotly import graph_objs as go

import pandas as pd

#external_css = ['https://codepen.io/khan-sbm/pen/zYObZPx.css']

import pandas as pd

trd = pd.read_csv('./data/UNI_TRD_ENF17.csv')

app = dash.Dash(__name__)
server = app.server

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

app.layout = html.Div([

    html.H1("Mapa de distribucion Electrica"),
    html.H3("Seleccionar Region"),

    dcc.Dropdown(
        options= [dict(label=x, value=x) for x in trd.CONJ.unique()]
    ),

    dcc.Graph(
        figure= go.Figure(
            data = [
                go.Scattermapbox(
                    lat= trd.lat,
                    lon= trd.lon,
                    mode='markers',
                ),

            ],

            layout = go.Layout(
                mapbox = go.layout.Mapbox(
                    accesstoken= mapbox_access_token,
                    center= dict(lat=trd.lat.mean(), lon=trd.lon.mean()),
                    zoom=10,
                    pitch=45,
                    style='light'
                ),
                margin= dict(t=10,r=10,b=10,l=10)
            )
        )
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)