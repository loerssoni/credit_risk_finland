
import pandas as pd
import joblib

import dash
import dash_html_components as html
import dash_core_components as dcc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False

app.layout = html.Div([
    html.H1(children='Yritysten ja yhteisöjen todennäköisyys joutua protestilistalle'), 
    html.Div(id='header',
             children='Syötä y-tunnus'),
    html.Div(dcc.Input(id='yid', type='text')),
    html.Button('Laske', id='button'),
    html.Div(id='status',
             children=''),
    html.Div(id='output-container-button',
             children='')
    
])

x = pd.read_csv('pred_X.csv', usecols=['Y-tunnus'])
gb = joblib.load('gb.pkl')


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('yid', 'value')])
def update_output(n_clicks, value):
    if value is None:
        return ''
    print('Luetaan yrityksen tietoja...')
    X = pd.read_csv('pred_X.csv',skiprows=(x[x['Y-tunnus'] != value.strip()].index + 1), index_col=0)
    if len(X) == 0:
        return 'Yrityksen tietoja ei löytynyt.'
    X_agg = X.groupby('Y-tunnus').agg(['mean', 'last'])
    X_agg.columns = [' '.join(col) for col in X_agg.columns]
    print('Lasketaan ennustetta...')
    return 'Todennäköisyys: '+str((gb.predict_proba(X_agg)[0][1]*100).round(2)) + '%'

@app.callback(
    dash.dependencies.Output('status', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('yid', 'value')])
def update_status(n_clicks, value):
    if value is None:
        return ''
    return 'Haetaan tietoja yritykselle {}'.format(value)
    
    
    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
