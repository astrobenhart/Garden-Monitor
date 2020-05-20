import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from Read_db import get_env_data, get_data_by_id

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)


df = get_env_data()


app.layout = html.Div([
    dcc.Graph(
        id='Air-Temp',
        figure={
            'data': [
                dict(
                    x=df['datatime'],
                    y=df['air_temp1'],
                    # text='Air Temp',
                    # mode='markers',
                    # opacity=0.7,
                    # marker={
                    #     'size': 15,
                    #     'line': {'width': 0.5, 'color': 'white'}
                    # },
                )
            ],
            'layout': dict(
                xaxis={'type': 'date', 'title': 'Datetime'},
                yaxis={'title': 'Air Temperature (C)'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)