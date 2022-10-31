from tkinter import TRUE
import numpy as np
import pickle
import pandas
import os
from flask import Flask, request, render_template

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "t46ljv3Q9IXQkrCwI7FOvm4ngTWF_2z5A7mRVG8XB6rS"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
                               "apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json','Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
#scale = pickle.load(open(r'scale1.pkl', 'rb'))


@app.route('/')  # rendering the html template
def home():
    return render_template('home.html')


@app.route('/predict', methods=["POST", "GET"])  # rendering the html template
def predict():
    return render_template("input.html")


# route to show the predictions in a web UI
@app.route('/submit', methods=["POST","GET"])
def submit():
    
    #  reading the inputs given by the user
    Gender = request.form["Gender"]
    Married = request.form["Married"]
    Dependents = request.form["Dependents"]
    Education = request.form["Education"]
    Self_Employed = request.form["Self_Employed"]
    ApplicantIncome = request.form["Applicant Income"]
    CoapplicantIncome = request.form["Co Applicant Income"]
    LoanAmount = request.form["Loan Amount"]
    Loan_Amount_Term = request.form["Loan Amount Term"]
    Credit_History = request.form["Credit History"]
    Property_Area = request.form["Property Area"]

    t = [[int(Gender), int(Married), int(Dependents), int(Education), int(Self_Employed),int(ApplicantIncome), 
          int(CoapplicantIncome), int(LoanAmount), int(Loan_Amount_Term),int(Credit_History), int(Property_Area)]]

    payload_scoring = {"input_data": [{"field": [['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                                                  'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                                                  'Loan_Amount_Term', 'Credit_History', 'Property_Area']], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/9f38cb18-2351-4174-895b-f5b5904a4242/predictions?version=2022-05-02',
                                     json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    print(pred)
    if (pred == 0):
        return render_template("output.html", result="Loan wiil Not be Approved")
    else:
        return render_template("output.html", result="Loan will be Approved")

    # showing the prediction results in a UI


if __name__ == "__main__":

    # app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=TRUE)
