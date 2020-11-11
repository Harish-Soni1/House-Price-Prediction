from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
import sklearn
import os
from sklearn.preprocessing import StandardScaler
folder = os.path.join('static', 'images')

app = Flask(__name__)
model = pickle.load(open('random_forest_model.pkl', 'rb'))
app.config['UPLOAD_FOLDER']=folder
pic = os.path.join(app.config['UPLOAD_FOLDER'], 'OIP_1.jpg')

@app.route('/', methods=['Get', 'POST'])
def Home():
    return render_template('index.html', name=pic)


standard_to = StandardScaler()
@app.route("/predict",methods=['Post'])


def predict():
    dealer = 0
    owner = 0
    rk = 0
    if request.method == 'POST':
        under_construction = request.form['Under_Con']
        if under_construction == 'YES' or under_construction == 'yes' or under_construction == 'Yes' or under_construction == 'Y' or under_construction == 'y':
            under_construction = 1
        else:
            under_construction = 0

        rera = request.form['RERA']
        if rera == 'YES' or rera == 'yes' or rera == 'Yes' or rera == 'Y' or rera == 'y':
            rera = 1
        else:
            rera = 0
        bhk_no = int(request.form['BHK'])
        square_ft = float(request.form['Square_Ft'])
        ready_to_move = request.form['Ready_TO_Move']
        if ready_to_move == 'YES' or ready_to_move == 'yes' or ready_to_move == 'Yes' or ready_to_move == 'Y' or ready_to_move == 'y':
            ready_to_move = 1
        else:
            ready_to_move = 0
        resale = request.form['Resale']
        if resale == 'YES' or resale == 'yes' or resale == 'Yes' or resale == 'Y' or resale == 'y':
            resale = 1
        else:
            resale = 0
        longitude = float(request.form['Longitude'])
        latitude = float(request.form['Latitude'])
        posted_by = request.form['Posted_By']
        if posted_by == "Owner":
            dealer = 0
            owner = 1
        elif posted_by == "Dealer":
            dealer = 1
            owner = 0
        else:
            dealer = 0
            owner = 0
        bhk_or_rk = request.form['bhk_or_rk']
        if bhk_or_rk == "BHK":
            rk = 0
        else:
            rk = 1
        df = pd.DataFrame([[under_construction, rera, bhk_no, int(square_ft), ready_to_move, resale, int(longitude), int(latitude), dealer, owner, rk]], columns=['UNDER_CONSTRUCTION', 'RERA', 'BHK_NO', 'SQUARE_FT', 'READY_TO_MOVE', 'RESALE', 'LONGITUDE', 'LATITUDE', 'Dealer', 'Owner', 'RK'])
        prediction = model.predict(df)
        output = int(prediction)
        if output < 100:
            return render_template('index.html', prediction_text="The House Price is {} Lakh".format(output), name=pic)
        else:
            return render_template('index.html', prediction_text="The House Price is {} Crore".format(output/100), name=pic)
    else:
        return render_template('index.html', prediction_text="Sorry", name=pic)


if __name__ == "__main__":
    app.run(debug=True)

