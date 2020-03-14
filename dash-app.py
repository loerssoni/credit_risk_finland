
import pandas as pd
import numpy as np
import joblib

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import dash_table


gb = joblib.load('gb.pkl')
y = pd.read_hdf('y.h5', 'x')
preds = pd.read_hdf('preds.h5', 'X')

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
             children='\n'),
    html.Div(id='output-container-button',
             children='\n'),
    html.Div([
    dash_table.DataTable(
    id='company-info',
    columns=[{"name": i, "id": i} for i in pd.read_hdf('pred_X.h5', 'X', where='yTunnus == "0"').columns[:9]],
    data=[],
    )
    ]),
    
    html.H2(children='Päätöksenteon tulkinta'),
    html.P('Muuttamalla liukusäädinten asetuksia voit tutkia, kuinka ennuste' +\
        'kuvitteelliselle yritykselle muuttuu tietojen muuttuessa.'),
    html.Div([
    
    html.Div(id='slider-output-container', children='', style={'padding': 30}),
    html.Div([
    dcc.Dropdown(
        id='muoto',
        options=[
        {'label': 'AOY', 'value': 'AOY'},
        {'label': 'OK', 'value': 'OK'},
        {'label': 'OY', 'value': 'OY'},
        {'label': 'OYJ', 'value': 'OYJ'},
        {'label': 'VOJ', 'value': 'VOJ'},
        {'label': 'VOY', 'value': 'VOY'},
        ],
    ),
    html.P('Yritysmuoto'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    dcc.Dropdown(
        id='toimiala',
        options=[
        {'label': 'Maatalous, metsätalous ja kalatalous', 'value':'0'},
        {'label':'Kaivostoiminta ja louhinta', 'value':'1'},
        {'label':'Teollisuus', 'value':'2'},
        {'label':'Sähkö-, kaasu- ja lämpöhuolto, jäähdytysliiketoiminta', 'value':'3'},
        {'label':'Vesihuolto, jätehuolto jne.', 'value':'4'},
        {'label':'Rakentaminen', 'value':'5'},
        {'label':'Tukku- ja vähittäiskauppa; moottoriajoneuvojen korjaus', 'value':'6'},
        {'label':'Kuljetus ja varastointi', 'value':'7'},
        {'label':'Majoitus- ja ravitsemistoiminta', 'value':'8'},
        {'label':'Informaatio ja viestintä', 'value':'9'},
        {'label':'Rahoitus- ja vakuutustoiminta', 'value':'10'},
        {'label':'Kiinteistöalan toiminta', 'value':'11'},
        {'label':'Ammatillinen, tieteellinen ja tekninen toiminta', 'value':'12'},
        {'label':'Hallinto- ja tukipalvelutoiminta', 'value':'13'},
        {'label':'Julkinen hallinto ja maanpuolustus', 'value':'14'},
        {'label':'Koulutus', 'value':'15'},
        {'label':'Terveys- ja sosiaalipalvelut', 'value':'16'},
        {'label':'Taiteet, viihde ja virkistys', 'value':'17'},
        {'label':'Muu palvelutoiminta', 'value':'18'},
        {'label':'Kotitalouksien toiminta työnantajina', 'value':'19'},
        {'label':'Kansainvälisten organisaatioiden toiminta', 'value':'20'},
        {'label':'Toimiala tuntematon', 'value':'21'},
        ],
    ),
    html.P('Toimiala'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='tulo',
        min=0,
        max=1.279177e+06,
        step=100,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Lopullinen verotettava tulo'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='verot',
        min=0,
        max=2.794776e+05,
        step=100,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Lopulliset maksettavat verot'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='ennakot',
        min=0,
        max=2.826432e+05,
        step=100,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Maksetut ennakot'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='palautus',
        min= -3.390683e+04,
        max=2.989562e+04,
        step=100,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Jäännösvero/Veronpalautus'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='muutokset',
        min=0,
        max=30,
        step=1,
        value=0,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Muutosten määrä yritysrekisterissä'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}),
    html.Div([
    daq.Slider(
        id='tyypit',
        min=0,
        max=20,
        step=1,
        value=0,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Muutostyyppien määrä yritysrekisterissä'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}), 
    html.Div([
    daq.Slider(
        id='ika',
        min=0,
        max=40,
        step=1,
        value=10,
        handleLabel={"showCurrentValue": True,"label": " "}),
    html.P('Yrityksen ikä'),
    ], style={'width': '35%', 'display': 'inline-block','padding': 20}), 
    ])
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('company-info', 'data')],
    [dash.dependencies.State('yid', 'value')])
def update_output(data, value):
    if value is None:
        return '\n'
    pred = preds.loc[value.strip(),:].values[0].round(4)*100
    return 'Todennäköisyys: {}%'.format(pred)

@app.callback(
    dash.dependencies.Output('company-status', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('yid', 'value')])
def update_status(n_clicks, value):
    if value is None:
        return '\n'
    if value.strip() in y.values:    
        return 'Yrityksellä on merkintöjä protestilistalla 1.11.2019 - 4.3.2020.'
    return 'Ei merkintöjä protestilistalla 1.11.2019 - 4.3.2020.'

@app.callback(
    dash.dependencies.Output('company-info', 'data'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('yid', 'value')])
def update_status(n_clicks, value):
    if value is None:
        return []
    X = pd.read_hdf('pred_X.h5', 'X', where='yTunnus == "{}"'.format(value.strip())).iloc[:,:9]
    return X.to_dict('records')

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('tulo', 'value'),
    dash.dependencies.Input('verot', 'value'),
     dash.dependencies.Input('ennakot', 'value'),
    dash.dependencies.Input('palautus', 'value'),
    dash.dependencies.Input('muutokset', 'value'),
    dash.dependencies.Input('tyypit', 'value'),
    dash.dependencies.Input('ika', 'value'),
    dash.dependencies.Input('muoto', 'value'),
    dash.dependencies.Input('toimiala', 'value'),])
def update_dummy_prediction(tulo, verot,ennakot, palautus,
                            muutokset, tyypit, ika, muoto, toimiala):
    X = pd.read_hdf('predX.h5', 'X', where='Ytunnus == "0"')
    X.loc[len(X)] = 2014.5
    X.iloc[:,2:10] = [tulo, verot, ennakot, palautus, palautus,
                      muutokset, tyypit, 365*ika]
    X.iloc[:,10:] = 0
    if toimiala is not None:
        X.loc[:,'Toimiala{}'.format(toimiala)] = 1
    if muoto is not None:
        X.loc[:,'company_form_{}'.format(muoto)] = 1
    
    X.iloc[:,6] = abs(np.min([X.values[0][5], 0]))
    X.iloc[:,5] = abs(np.max([X.values[0][5], 0]))
    
    features = X.columns[1:10]
    for col in features:
        for col2 in features:
            X[col+'*'+col2] = (X[col2] * X[col])
    for col in features:
        for col2 in features:
            X[col+'/'+col2] = (X[col2] / X[col])

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    X_agg = X.groupby('Ytunnus').agg(['mean', 'last'])
    X_agg.columns = [' '.join(col) for col in X_agg.columns]

    return 'Todennäköisyys: ' + str((gb.predict_proba(X_agg)[0][1]*100).round(2)) + '%'



if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
