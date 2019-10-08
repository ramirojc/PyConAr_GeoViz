import dash
import dash_core_components as dcc
import dash_html_components as html

#import plotly.graph_objects as go
from plotly import graph_objs as go

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    html.H2("Mapa de distribucion Electrica"),

    html.H4("Seleccionar Region"),

    dcc.Dropdown(
        id= 'dd_region',
        options= [
            {'label': 'Centro','value':'centro'},
            {'label': 'Sur', 'value': 'sur'}
        ]),

    dcc.Graph(
        id= 'bars',
        figure= {
            'data': [
                {'x': [0,1,2,4], 'y':[10, 11, 9, 12], 'type': 'scatter', 'mode':'markers', 'name': 'Serie 1'},
                {'y':[12, 11, 9, 7], 'type': 'scatter', 'name': 'Serie 2'}],
            'layout': {
                'title': 'Puntos y Lineas'
            }
        }
    ),

    dcc.Graph(
        id = 'bars2',
        figure = go.Figure(
            data=[
                go.Bar(x=['enero','feb','mar','abr'], y=[20, 21, 22, 25], name='Temperatura'),
                go.Scatter(x=['enero','feb','mar','abr'], y=[10, 9, 8, 9], name='Lluvia')
            ],
            layout= go.Layout(
                title='Clima Argentina',
                legend=go.layout.Legend(x=0,y=1.0)
            )
        )
    )


])

if __name__ == '__main__':
    app.run_server(debug=True)