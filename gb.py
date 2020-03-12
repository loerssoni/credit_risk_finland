import pandas as pd 
import flask
from sklearn.externals import joblib

gb = joblib.load('gb.pkl')

app = flask.Flask(__name__)

@app.route("/", methods=["GET","POST"]) 
def predict():
    data = {"success": False}
    params = flask.request.args
    if "G1" in params.keys(): 
        X = pd.read_csv('pred_X.csv',skiprows=(x[x['Y-tunnus'] != params.get('G1')].index + 1), index_col=0)
        if len(X) == 0:
            data['response'] = 'Yrityksen tietoja ei löytynyt.'
        else:
            X_agg = X.groupby('Y-tunnus').agg(['mean', 'last'])
            X_agg.columns = [' '.join(col) for col in X_agg.columns]
            data['response'] = str((gb.predict_proba(X_agg)[0][1]*100).round(2)) + '%'
        data['success'] = True
    return flask.jsonify(data)

if  __name__  == '__main__':
    app.run(host='0.0.0.0') 
