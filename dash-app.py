
import pandas as pd
import numpy as np
import joblib

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
gb = joblib.load('gb.pkl')
y = pd.read_hdf('y.h5', 'x')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.css.config.serve_locally = False
app.scripts.config.serve_locally = False

app.layout = html.Div([
    html.H2(children='Yritysten ja yhteisöjen todennäköisyys joutua protestilistalle'), 
    html.Div(id='header',
             children='Syötä y-tunnus'),
    html.Div(dcc.Input(id='yid', type='text')),
    html.Button('Laske', id='button'),
    html.Div(id='company-status',
             children=''),
    html.Div(id='output-container-button',
             children=''),

    html.H2(children='Päätöksenteon visualisointi'),
    html.Div([

    html.Div(id='slider-output-container', children='', style={'padding': 30}),

    html.Div([
    daq.Slider(
        id='tulo',
        min=0,
        max=3.37308e+09,
        step=1000,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Lopullinen verotettava tulo'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='verot',
        min=-25205.5,
        max=6.74619e+08,
        step=1000,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Lopulliset maksettavat verot'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='ennakot',
        min=0,
        max=6.74625e+08,
        step=1000,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Maksetut ennakot'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='palautus',
        min=-3.71537e+07,
        max=2.92022e+07,
        step=1000,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Jäännösvero/Veronpalautus'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='oy',
        min=0,
        max=1,
        step=1,
        value=0,
        handleLabel={"showCurrentValue": True,"label": " "}),
        html.P('Osakeyhtiö (1 = on osakeyhtiö)'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='muutokset',
        min=0,
        max=171,
        step=1,
        value=0,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Muutosten määrä yritysrekisterissä'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='tyypit',
        min=0,
        max=44,
        step=1,
        value=0,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Muutostyyppien määrä yritysrekisterissä'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),

    ])

])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('yid', 'value')])
def update_output(n_clicks, value):
    if value is None:
        return ''
    X = pd.read_hdf('pred_X.h5', 'X', where='yTunnus == "{}"'.format(value.strip()))

    if len(X) == 0:
        return 'Yrityksen tietoja ei löytynyt.'

    features = X.columns[1:]
    for col in features:
        for col2 in features:
            X[col+'*'+col2] = (X[col2] * X[col])
    for col in features:
        for col2 in features:
            X[col+'/'+col2] = (X[col2] / X[col])

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    X_agg = X.groupby('yTunnus').agg(['mean', 'last'])
    X_agg.columns = [' '.join(col) for col in X_agg.columns]

    return 'Todennäköisyys: '+str((gb.predict_proba(X_agg)[0][1]*100).round(2)) + '%'

@app.callback(
    dash.dependencies.Output('company-status', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('yid', 'value')])
def update_status(n_clicks, value):
    if value is None:
        return ''
    if value.strip() in y.values:    
        return 'Yrityksellä on merkintöjä protestilistalla 1.11.2019 - 4.3.2020.'
    return 'Ei merkintöjä protestilistalla 1.11.2019 - 4.3.2020.'

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('tulo', 'value'),
    dash.dependencies.Input('verot', 'value'),
    dash.dependencies.Input('ennakot', 'value'),
    dash.dependencies.Input('palautus', 'value'),
    dash.dependencies.Input('oy', 'value'),
    dash.dependencies.Input('muutokset', 'value'),
    dash.dependencies.Input('tyypit', 'value'),])
def update_dummy_prediction(tulo, verot, ennakot, palautus,
                           oy, muutokset, tyypit):
    X = pd.read_hdf('pred_X.h5', 'X', where='yTunnus == "0"')
    X.loc[len(X)] = 2014.5
    X.iloc[:,2:] =[tulo, verot, ennakot, palautus, palautus,
                           oy, muutokset, tyypit]
    X.iloc[:,6] = abs(np.min([X.values[0][5], 0]))
    X.iloc[:,5] = abs(np.max([X.values[0][5], 0]))
    features = X.columns[1:]
    for col in features:
        for col2 in features:
            X[col+'*'+col2] = (X[col2] * X[col])
    for col in features:
        for col2 in features:
            X[col+'/'+col2] = (X[col2] / X[col])

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    X_agg = X.groupby('yTunnus').agg(['mean', 'last'])
    X_agg.columns = [' '.join(col) for col in X_agg.columns]

    return 'Todennäköisyys: ' + str((gb.predict_proba(X_agg)[0][1]*100).round(2)) + '%'



if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
