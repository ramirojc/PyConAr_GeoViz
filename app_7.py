import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from plotly import graph_objs as go

import pandas as pd
import numpy as np

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

##################################################
trd = pd.read_csv('./data/UNI_TRD_ENF17.csv')

conj_name = {
    15615: 'Boa Aventura',
    16070: 'Nova Friburgo',
    16068: 'Campo do Coelho',
    15616: 'Vale dos Peoes',
    16069: 'Conselheiro Paulino'
}

trd['CONJ_N'] = trd.CONJ.copy()
for i,c in enumerate(trd.CONJ_N.unique()):
    trd.CONJ_N.replace(c,i,inplace=True)

map_layout = go.Layout(
        mapbox= go.layout.Mapbox(
            accesstoken= mapbox_access_token,
            center= dict(lat=trd.lat.mean(), lon=trd.lon.mean()),
            zoom=10,
            pitch=45,
            style='light'),
        margin= dict(l=0,t=0,b=0,r=0)
        )

FIC_dist_layout = go.Layout(
    title= 'Distribucion Frecuencia de Cortes',
    height= 300,
    margin= dict(l=30,t=50,b=30,r=30),
    barmode='overlay',
    legend_orientation='h'
)

DIC_dist_layout = go.Layout(
    title= 'Distribucion Duracion de Cortes',
    height= 300,
    margin= dict(l=30,t=50,b=30,r=30),
    barmode='overlay',
    legend_orientation='h'
)

ENE_dist_layout = go.Layout(
    title= 'Distribucion Consumo',
    height= 300,
    margin= dict(l=30,t=50,b=30,r=30),
    barmode='overlay',
    legend_orientation='h'
)

app = dash.Dash(__name__)
server = app.server

###################################################
# Layout
###################################################

app.layout = html.Div([

    html.Div([
        html.H2(" Mapa de distribucion Electrica")
    ], style={'text-align': 'center'}),

    html.Div([
        html.Div([
            html.H6("Seleccione Regiones"),

            dcc.Dropdown(
                id= 'dd_region',
                multi= True,
                placeholder= 'Regiones',
                options= [dict(label=conj_name[x], value=x) for x in trd.CONJ.unique()],
                value= list(trd.CONJ.unique()))
        ], className= 'pretty_container four columns'),

        html.Div([
            html.H6("Codificacion color"),

            dcc.RadioItems(
                id= 'ra_color',
                options= [
                    dict(label='Frecuencia de Cortes', value='FIC'),
                    dict(label='Duracion Media de Cortes', value='DIC'),
                    dict(label='Grupo Electrico', value='CONJ_N')],
                value= 'FIC'
            )
        ], className= 'pretty_container four columns'),

        html.Div([
            html.H6("Codificacion tamaño"),

            dcc.RadioItems(
                id= 'ra_size',
                options= [
                    dict(label='No Codificar', value='FIX_SIZE'),
                    dict(label='Duracion Media de Cortes', value='DIC'),
                    dict(label='Consumo Total', value='ENE_12')],
                value= 'FIX_SIZE'
            )
        ], className= 'pretty_container four columns')



    ], className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id = 'map')
        ], className= 'pretty_container eight columns'),

        html.Div(id='map_side_div', children=[], className= 'pretty_container four columns')

    ], className='row'),

    html.Div([
        html.H6("  Seleccione un area del mapa para comparar distribuciones")
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id='FIC_dist')
        ], className= 'pretty_container four columns'),

        html.Div([
            dcc.Graph(id='DIC_dist')
        ], className= 'pretty_container four columns'),

        html.Div([
            dcc.Graph(id='ENE_dist')
        ], className= 'pretty_container four columns')



    ], className='row'),

], className= 'mainContainer')

###################################################
# CallBacks
###################################################

@app.callback(
    [Output(component_id='map', component_property='figure'),
    Output('map_side_div', 'children')],
    [Input('dd_region', 'value'),
     Input('ra_color', 'value'),
     Input('ra_size', 'value')],
    [State("map", "relayoutData")]
)
def update_map(region, color_var, size_var, map_layout_data):
    print(region, color_var, size_var)

    trd_selection = trd[trd.CONJ.isin(region)]

    color_norm = trd_selection[color_var]

    if size_var == 'FIX_SIZE':
        size_norm = 10
        trd_selection['FIX_SIZE'] = trd_selection[color_var]

    else:
        trd_max = trd_selection[size_var].quantile(0.95)
        size_norm = np.log1p(trd_selection[size_var]/trd_max)*30
        size_norm.clip(6, 25, inplace=True)

    info = trd_selection.FIC.map('<b>Frec Corte:</b> {:,.2f}'.format) + \
           trd_selection.DIC.map('<br><b>Dur Corte:</b> {:,.2f}'.format) + \
           trd_selection.ENE_12.map('<br><b>Consumo:</b> {:,.2f}'.format)

    map_data = [
        go.Scattermapbox(
            lat=trd_selection.lat,
            lon=trd_selection.lon,
            mode='markers',
            marker=dict(
                size=size_norm,
                cmin=color_norm.quantile(0.1),
                cmax=color_norm.quantile(0.9),
                color=color_norm,
                colorscale='RdBu',
                reversescale=True,
                showscale=True
            ),
        )]

    side_div = dcc.Graph(figure = go.Figure(
        data=[
            go.Scatter(x=trd_selection[color_var], y=trd_selection[size_var],
                    mode='markers', name='Correlacion')
        ],
        layout= go.Layout(
            title='Correlacion Entre Variables',
            margin=dict(l=20, t=50, b=20, r=20),
        )
    )
    )

    if map_layout_data:
        print(map_layout_data)
        print(map_layout_data.keys())

        if 'mapbox.center' in map_layout_data.keys():
            # Lock Camera Position
            cam_lat = float(map_layout_data['mapbox.center']['lat'])
            cam_lon = float(map_layout_data['mapbox.center']['lon'])
            cam_zoom = float(map_layout_data['mapbox.zoom'])

            map_layout.mapbox.center.lat = cam_lat
            map_layout.mapbox.center.lon = cam_lon
            map_layout.mapbox.zoom = cam_zoom


    return dict(data=map_data, layout=map_layout), side_div

@app.callback(
    [Output('FIC_dist','figure'),
     Output('DIC_dist','figure'),
     Output('ENE_dist','figure')],
    [Input('map', 'selectedData')]
)
def plot_dist(selectedData):
    print('seleccion:')

    FIC_dist_data = [go.Histogram(x=trd.FIC,
                                  nbinsx=30, histnorm='probability density', name='Total', opacity=0.75)]
    DIC_dist_data = [go.Histogram(x=trd.DIC,
                                  nbinsx=30, histnorm='probability density', name='Total', opacity=0.75)]
    ENE_dist_data = [go.Histogram(x=trd.ENE_12,
                                  nbinsx=30, histnorm='probability density', name='Total', opacity=0.75)]


    return dict(data=FIC_dist_data, layout=FIC_dist_layout),\
           dict(data=DIC_dist_data, layout=DIC_dist_layout),\
           dict(data=ENE_dist_data, layout=ENE_dist_layout)


#####################################################
if __name__ == '__main__':
    app.run_server(debug=True)