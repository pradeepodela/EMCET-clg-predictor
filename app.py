from flask import Flask, render_template, request, jsonify, render_template_string
import json
import pyrebase
import datetime
app = Flask(__name__)


config = {
   'apiKey': "AIzaSyBwRBcKz9DC68UVsMBygkANr_QixS0ZaKA",
  'authDomain': "mypy-19226.firebaseapp.com",
  'databaseURL': "https://mypy-19226-default-rtdb.firebaseio.com",
  'projectId': "mypy-19226",
  'storageBucket': "mypy-19226.appspot.com",
  'messagingSenderId': "990787705081",
  'appId': "1:990787705081:web:ab15b33b11bbea973dea28",
  'measurementId': "G-298F64SX86"
}

firebase = pyrebase.initialize_app(config)


# Load colleges data
with open('data.json', 'r') as f:
    colleges = json.load(f)
    data = colleges

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    name = request.form['name']
    phonenumber = request.form['phonenumber']
    hall = request.form['hall']
    rank = int(request.form['rank'])
    gender = request.form['gender']
    caste = request.form['caste']
    branch = request.form['branch']
    datas = {
        "name": name,
        "phonenumber": phonenumber,
        "hall": hall,
        "rank": rank,
        "gender":gender,
        "caste": caste,
        "branch": branch,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db = firebase.database()
    db.child("users").push(datas)
    
    

    
    # Handling newline characters in caste
    caste = caste.replace("\\n", "\n")
    
    filtered_colleges = []

    for college in data:
        try:
            if int(college[caste]) >= rank:
                if branch != 'ALL':
                    if college['Branch Name'] == branch:
                        filtered_colleges.append(college)
                else:
                    filtered_colleges.append(college)
        except (ValueError, KeyError):
            # Skip this college if the value is non-numeric or the key is not found
            pass
    
    return render_template('result.html', table_data=filtered_colleges)


