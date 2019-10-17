import dash
import dash_core_components as dcc
import dash_html_components as html

from plotly import graph_objs as go

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    html.H1("Mapa de distribucion"),
    html.P("Esto es una descripcion"),
    html.Hr()

])

if __name__ == '__main__':
    app.run_server(debug=True)