import sqlite3
#import matplotlib.pyplot as plt
#import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
#import cufflinks as cf
#import plotly
#import plotly.offline as py
import plotly.graph_objs as go
#import flask as fl
import plotly.subplots as ps
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash.dependencies as dd
import dash_html_components as html
import pandas as pd


def clean_db(df, low=0, high=100):
    df = df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
    for i in tqdm(range(len(df.columns))):
        for j in range(len(df.iloc[:, i])):
            if not low < float(df.iloc[j, i]) < high:
                df.iloc[j, i] = df.iloc[j - 1, i]
    return df

conn = sqlite3.connect('data.db')
sql_q = ('select * from from_nano;')
df = pd.read_sql(sql_q, conn)
df.datatime = pd.to_datetime(df.datatime)
df = df.set_index('datatime')
df = clean_db(df)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True


################## Chart returns ######################

def Temp_trace(start_date=datetime.now() - timedelta(days=2), end_date=datetime.now()):
    conn = sqlite3.connect('data.db')
    sql_q = ('select datatime, air_temp1, soil_temp from from_nano;')
    df = pd.read_sql(sql_q, conn)
    df.datatime = pd.to_datetime(df.datatime)
    df = df.set_index('datatime')
    df = clean_db(df)
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    fig = ps.make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_scatter(x=df.index, y=df.air_temp1, mode="lines", name="Air Temperature", secondary_y=False)
    fig.add_scatter(x=df.index, y=df.soil_temp, mode="lines", name="Soil Temperature", line_shape='spline', secondary_y=True)

    fig.update_layout(
        title='Temperature Over Time',
        # yaxis_title='Temp (C)',
        # xaxis_title='Date',
        legend=dict(
            orientation="h"
        )
    )

    fig.update_yaxes(title_text="Air Temperature (C)", secondary_y=False)
    fig.update_yaxes(title_text="Soil Temperature (C)", secondary_y=True)

    Charts = [
        dcc.Graph(style={'height': 600, 'width': 1200, 'display': 'inline-block', 'vertical-align': 'middle'},
                  figure=fig)]

    return Charts


def Humidity_trace(start_date=datetime.now() - timedelta(days=2), end_date=datetime.now()):
    conn = sqlite3.connect('data.db')
    sql_q = ('select datatime, humidity, soil_moisture from from_nano;')
    df = pd.read_sql(sql_q, conn)
    df.datatime = pd.to_datetime(df.datatime)
    df = df.set_index('datatime')
    df = clean_db(df)
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    fig = ps.make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_scatter(x=df.index, y=df.humidity, mode="lines", name="Humidity")
    fig.add_scatter(x=df.index, y=df.soil_moisture, mode="lines", name="Soil Moisture", line_shape='spline')

    fig.update_layout(
        title='Moisture Levels Over Time',
        yaxis_title='%',
        # xaxis_title='Date',
        legend=dict(
            orientation="h"
        )
    )

    Charts = [
        dcc.Graph(style={'height': 600, 'width': 1200, 'display': 'inline-block', 'vertical-align': 'middle'},
                  figure=fig)]

    return Charts


def gas_trace(start_date=datetime.now() - timedelta(days=2), end_date=datetime.now()):
    conn = sqlite3.connect('data.db')
    sql_q = ('select datatime, methane_levels, CO_levels from from_nano;')
    df = pd.read_sql(sql_q, conn)
    df.datatime = pd.to_datetime(df.datatime)
    df = df.set_index('datatime')
    df = clean_db(df)
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    fig = ps.make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_scatter(x=df.index, y=df.methane_levels, mode="lines", name="Methane", line_shape='spline')
    fig.add_scatter(x=df.index, y=df.CO_levels, mode="lines", name="CO", line_shape='spline')

    fig.update_layout(
        title='Methane and CO levels Over Time',
        yaxis_title='%',
        # xaxis_title='Date'
        legend=dict(
            orientation="h"
        )
    )
    Charts = [
        dcc.Graph(style={'height': 600, 'width': 1200, 'display': 'inline-block', 'vertical-align': 'middle'},
                  figure=fig)]

    return Charts


def Pressure_trace(start_date=datetime.now() - timedelta(days=2), end_date=datetime.now()):
    conn = sqlite3.connect('data.db')
    sql_q = ('select datatime, pressure from from_nano;')
    df = pd.read_sql(sql_q, conn)
    df.datatime = pd.to_datetime(df.datatime)
    df = df.set_index('datatime')
    df = clean_db(df, 100000, 150000)
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    fig = go.Figure()

    fig.add_scatter(x=df.index, y=df.pressure, mode="lines", name="Pressure")

    fig.update_layout(
        title='Pressure Over Time',
        yaxis_title='Pascals',
        # xaxis_title='Date'
    )
    Charts = [
        dcc.Graph(style={'height': 600, 'width': 1200, 'display': 'inline-block', 'vertical-align': 'middle'},
                  figure=fig)]

    return Charts


################# Layouts #################

# initial_start_date = datetime.now() - timedelta(days=7)
# initial_end_date = datetime.now()
initial_end_date = df.index.max()
initial_start_date = initial_end_date - timedelta(days=14)

TempPlots = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.P('Date Range Slider'),
                dcc.DatePickerRange(
                    id='dateRange',
                    min_date_allowed=df.index.min(),
                    max_date_allowed=df.index.max(),
                    start_date=initial_start_date,
                    display_format='DD/MM/Y',
                    end_date=initial_end_date)
            ]),
        ]),
    dbc.Row([
        dcc.Loading(type='graph', id='TempOutput',
                    children=Temp_trace(
                        initial_start_date,
                        initial_end_date
                    ),
                    style={'width': '100%'}
                    )
    ])
], className="mt-4")

HumidityPlots = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.P('Date Range Slider'),
                dcc.DatePickerRange(
                    id='dateRange',
                    min_date_allowed=df.index.min(),
                    max_date_allowed=df.index.max(),
                    start_date=initial_start_date,
                    display_format='DD/MM/Y',
                    end_date=initial_end_date)
            ]),
        ]),
    dbc.Row([
        dcc.Loading(type='graph', id='HumidityOutput',
                    children=Humidity_trace(
                        initial_start_date,
                        initial_end_date
                    ),
                    style={'width': '100%'}
                    )
    ])
], className="mt-4")

GasPlots = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.P('Date Range Slider'),
                dcc.DatePickerRange(
                    id='dateRange',
                    min_date_allowed=df.index.min(),
                    max_date_allowed=df.index.max(),
                    start_date=initial_start_date,
                    display_format='DD/MM/Y',
                    end_date=initial_end_date)
            ]),
        ]),
    dbc.Row([
        dcc.Loading(type='graph', id='GasOutput',
                    children=gas_trace(
                        initial_start_date,
                        initial_end_date
                    ),
                    style={'width': '100%'}
                    )
    ])
], className="mt-4")

PressurePlots = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.P('Date Range Slider'),
                dcc.DatePickerRange(
                    id='dateRange',
                    min_date_allowed=df.index.min(),
                    max_date_allowed=df.index.max(),
                    start_date=initial_start_date,
                    display_format='DD/MM/Y',
                    end_date=initial_end_date)
            ]),
        ]),
    dbc.Row([
        dcc.Loading(type='graph', id='PressureOutput',
                    children=Pressure_trace(
                        initial_start_date,
                        initial_end_date
                    ),
                    style={'width': '100%'}
                    )
    ])
], className="mt-4")

################## Navbar ###################

navbar_item_width = 9

navbar = dbc.NavbarSimple(
    children=[
        dbc.Row([
            dbc.Col([
                dbc.NavItem(dbc.NavLink("Temperature", href="/temperatures",
                                        style={'width': 19 * navbar_item_width, 'display': 'inline-block'}))
            ]),
            dbc.Col([
                dbc.NavItem(dbc.NavLink("Humidity", href="/humidity",
                                        style={'width': 11 * navbar_item_width, 'display': 'inline-block'})),
            ]),
            dbc.Col([
                dbc.NavItem(dbc.NavLink("Methane & CO", href="/methane_co_levels",
                                        style={'width': 18 * navbar_item_width, 'display': 'inline-block'})),
            ]),
            dbc.Col([
                dbc.NavItem(dbc.NavLink("Pressure", href="/pressure",
                                        style={'width': 8 * navbar_item_width, 'display': 'inline-block'}))
            ])
        ])
    ],
    brand="Garden Monitor",
    sticky="top",
    expand='lg',
    light=True
)

################## App layout ###################

app.layout = html.Div([dcc.Location(id='url', refresh=False), navbar, html.Div(id='page-content')])


################# Call backs ###################

@app.callback(dd.Output('TempOutput', 'children'), [
    dd.Input('dateRange', 'start_date'),
    dd.Input('dateRange', 'end_date'),
])
def _drawTempPlots(start_date, end_date):
    return Temp_trace(start_date=start_date, end_date=end_date)


@app.callback(dd.Output('HumidityOutput', 'children'), [
    dd.Input('dateRange', 'start_date'),
    dd.Input('dateRange', 'end_date'),
])
def _drawHumidityPlots(start_date, end_date):
    return Humidity_trace(start_date=start_date, end_date=end_date)


@app.callback(dd.Output('GasOutput', 'children'), [
    dd.Input('dateRange', 'start_date'),
    dd.Input('dateRange', 'end_date'),
])
def _drawGasPlots(start_date, end_date):
    return gas_trace(start_date=start_date, end_date=end_date)

@app.callback(dd.Output('PressureOutput', 'children'), [
    dd.Input('dateRange', 'start_date'),
    dd.Input('dateRange', 'end_date'),
])
def _drawPressurePlots(start_date, end_date):
    return Pressure_trace(start_date=start_date, end_date=end_date)


@app.callback(dd.Output('page-content', 'children'), [dd.Input('url', 'pathname')])
def display_page(pathname):
    if str(pathname).lower() == '/temperatures':
        return TempPlots
    elif str(pathname).lower() == '/':
        return TempPlots
    elif str(pathname).lower() == '/humidity':
        return HumidityPlots
    elif str(pathname).lower() == '/methane_co_levels':
        return GasPlots
    elif str(pathname).lower() == '/pressure':
        return PressurePlots
    #     elif str(pathname).lower() == '/appendix':
    #         return Appendix
    # else:
    #     return fl.abort(404)


if __name__ == "__main__":
    app.run_server(debug=False, port=5001, host='0.0.0.0')
