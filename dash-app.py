import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
from sklearn.externals import joblib

app = dash.Dash(__name__) 

app.layout = html.Div(children = [
    html.H1(children='Ennuste luottoprotestien todennäköisyydestä'),
    html.P([
        html.Label('Y-tunnus'),
        dcc.Input(value='1', type='text', id='yid')
    ]),
    html.P([
        html.Label('Ennuste '),
        dcc.Input(value='Lasketaan...', type='text', id='pred'),
    ])
])

gb = joblib.load('gb.pkl')
x = pd.read_csv('pred_X.csv', usecols=['Y-tunnus'])

@app.callback(
    Output(component_id='pred', component_property='value'),
    [Input(component_id='yid', component_property='value')]
)
def update_prediction(yid):
    X = pd.read_csv('pred_X.csv',skiprows=(x[x['Y-tunnus'] != yid].index + 1), index_col=0)
    if len(X) == 0:
        return 'Yrityksen tietoja ei löytynyt.'
    X_agg = X.groupby('Y-tunnus').agg(['mean', 'last'])
    X_agg.columns = [' '.join(col) for col in X_agg.columns]

    return str((gb.predict_proba(X_agg)[0][1]*100).round(2)) + '%'


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
