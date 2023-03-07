from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from pip._vendor import requests
import sqlite3
import os.path
URL = "https://commonchemistry.cas.org/api/search?"


# Configure Flask
app = Flask(__name__)

# Configure database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "chem.db")
db = sqlite3.connect(db_path) 

def find_cas(chemical):
    # Return CAS number from function
    parameters = {
            'q' : chemical,  
            'size' : '1',
            'offset': '0'}
    response_api = requests.get(url = URL, params = parameters)
    response_api.raise_for_status()
    data = response_api.json()
    return(data["results"][0]['rn'])

    
@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        chemical = request.form.get("chemical")
        # API call to get CAS number from chemical name
        cas_number = find_cas(chemical)
        # Show details of search result
        return render_template("search_details.html", chemical = chemical.capitalize(), cas_number = cas_number)

@app.route("/search_details", methods=["GET", "POST"])
def search_details():
    if request.method == "GET":
        return render_template("search_details.html")
    else:
        # POST therefore add chemical/ CAS to database
        chemical = request.form.get("chemical")
        cas_number = request.form.get("cas_number")
        with sqlite3.connect(db_path) as db:
            data = [chemical, cas_number]
            db.execute("INSERT INTO Chemicals (name, cas) VALUES(?, ?)", data)
        return render_template("search.html")
        
        