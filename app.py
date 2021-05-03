from flask import Flask, request, render_template
import os
import joblib

path = os.getcwd()

with open('Models/model.sav', 'rb') as f:
    randomforest = joblib.load(f)

def get_predictions(age,sex,cp, trestbps, chol, req_model):
    mylist = [age,sex,cp, trestbps, chol]
    mylist = [float(i) for i in mylist]
    vals = [mylist]

    if req_model == 'RandomForest':
        #print(req_model)
        return randomforest.predict(vals)[0]

    else:
        return "Cannot Predict"


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']
        cp = request.form['cp']
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        req_model = request.form['req_model']

        target = get_predictions(age,sex,cp, trestbps, chol, req_model)

        if target==1:
            sale_making = 'Patient is likely to have heart disease'
        else:
            sale_making = 'Patient is unlikely to have heart disease'

        return render_template('home.html', target = target, sale_making = sale_making)
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)