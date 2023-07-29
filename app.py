import numpy as np
from flask import Flask, request, jsonify, render_template
import sklearn
import pickle
import pandas as pd
from markupsafe import Markup
import requests


from utils.solution import fertilizer_dic

app = Flask(__name__, static_url_path='/static')
model = pickle.load(open('RandomForest.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict')
def predict():
    return render_template('predict.html', current_page = 'predict')


@app.route('/crp_rcmnd', methods =['POST'])
def crp_rcmnd():
    features = [float(x) for x in request.form.values()]
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    return render_template('predict.html', prediction_text="Recommended Crop: {}".format(prediction), current_page='crp_rcmnd')


@app.route('/rcmnd')
def rcmnd():
    return render_template('rcmnd.html', current_page='rcmnd')

@ app.route('/solution_predict', methods=['POST'])
def solution_recommend():

    crop_name = str(request.form['crop'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorus'])
    K = int(request.form['potassium'])
    ph = float(request.form['ph'])

    features = [N, P, K, ph]

    current_fetures = np.array(features)

    df = pd.read_csv('Data/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]
    phr = df[df['Crop'] == crop_name]['pH'].iloc[0]

    features1 = [nr, pr, kr, phr]

    good_features = np.array(features1)

    n = nr - N
    p = pr - P
    k = kr - K
    ph1 = phr- ph

    temp = {abs(n): "N", abs(p): "P", abs(k): "K", abs(ph1):"ph"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"

    elif max_value == "K":
        if p < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    else:
        if ph1 < 0:
            key = 'PHHigh'
        else:
            key = "PHlow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('rcmnd.html', text1= "Current Parameters: {}".format(current_fetures), text2 = "Recommended Parameters: {}".format(good_features), recommendation=response)


@app.route('/hydroponic')
def hydroponic():
    return render_template('hydroponics.html', current_page = 'hydroponic')

@app.route('/p_model')
def p_model():
    return render_template('p_model.html', current_page = 'p_model')

if __name__ == "__main__":
    app.run(debug=True)
