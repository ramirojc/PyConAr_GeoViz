import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from plotly import graph_objs as go

import pandas as pd

##################################################

trd = pd.read_csv('./data/UNI_TRD_ENF17.csv')

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

map_layout = go.Layout(
        mapbox= go.layout.Mapbox(
            accesstoken= mapbox_access_token,
            center= dict(lat=trd.lat.mean(), lon=trd.lon.mean()),
            zoom=10,
            pitch=45,
            style='light'),
        margin= dict(l=0,t=0,b=0,r=0)
        )

conj_name = {
    15615: 'Boa Aventura',
    16070: 'Nova Friburgo',
    16068: 'Campo do Coelho',
    15616: 'Vale dos Peoes',
    16069: 'Conselheiro Paulino'
}
##################################################

app = dash.Dash(__name__)
server = app.server

###################################################
# Layout
###################################################

app.layout = html.Div([

    html.Div([
        html.H2("Mapa de distribucion Electrica")
    ], className='row'),

    html.Div([
        html.Div([
            html.H6("Seleccione Regiones"),

            dcc.Dropdown(
                id= 'dd_region',
                multi= True,
                placeholder= 'Regiones',
                options= [dict(label=conj_name[x], value=x) for x in trd.CONJ.unique()],
                value= trd.CONJ.unique())
        ], className= 'pretty_container four columns'),

        html.Div([
            html.H6("Codificacion color"),

            dcc.RadioItems(
                id= 'ra_color_cod',
                options= [
                    dict(label='Frecuencia de Cortes', value='FIC'),
                    dict(label='Duracion Media de Cortes', value='DIC'),
                    dict(label='Grupo Electrico', value='CONJ')],
                value= 'FIC'
            )
        ], className= 'pretty_container four columns'),

        html.Div([
            html.H6("Codificacion tamaño"),

            dcc.RadioItems(
                id= 'ra_size_cod',
                options= [
                    dict(label='Duracion Media de Cortes', value='DIC'),
                    dict(label='Consumo Total', value='ENE_12'),
                    dict(label='Perdidas Transformador', value='PER_TOT')],
                value= 'DIC'
            )
        ], className= 'pretty_container four columns')

    ], className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id = 'map')
        ], className= 'pretty_container eight columns'),

        html.Div([
            dcc.Graph(id= 'aux-graph')
        ], className= 'pretty_container four columns')

    ], className='row')

], className= 'mainContainer')

###################################################
# CallBacks
###################################################
@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='dd_region', component_property='value')]
)
def update_map(region):
    print(region)

    trd_selecion = trd[trd.CONJ.isin(region)]

    map_data=[
        go.Scattermapbox(
            lat=trd_selecion.lat,
            lon=trd_selecion.lon,
            mode='markers')
    ]

    return go.Figure(data= map_data, layout= map_layout)


#####################################################
if __name__ == '__main__':
    app.run_server(debug=True)