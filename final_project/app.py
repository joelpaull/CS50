from flask import Flask, redirect, render_template, request, session, send_from_directory
from flask_session import Session
from pip._vendor import requests
import sqlite3
import os.path
from datetime import datetime
from find_sds.find_sds import find_sds
from werkzeug.security import check_password_hash, generate_password_hash

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
        return render_template("search_details.html", chemical = chemical.title(), cas_number = cas_number)

@app.route("/search_details", methods=["GET", "POST"])
def search_details():
    if request.method == "GET":
        return render_template("search_details.html")
    else:
        # add chemical/ CAS to database
        chemical = request.form.get("chemical")
        cas_number = request.form.get("cas_number")
        # strip decimals from time, (first convert to str)
        now = datetime.now()
        s = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        time = s[:16]
        print(chemical)
        
        with sqlite3.connect(db_path) as db:
            data = [chemical, cas_number, time]
            db.execute("INSERT INTO Chemicals (name, cas, time) VALUES(?, ?, ?)", data)
        return render_template("search.html")
    
@app.route('/cas_database')
def cas_database():
    # Show results from database, ordered with most recent at top
    with sqlite3.connect(db_path) as db:
        data = db.execute("SELECT * FROM Chemicals ORDER BY time DESC")
        return render_template("cas_database.html", chemicals = data)

@app.route('/buy', methods=["GET", "POST"])
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # Add buy orders to database
        chemical = request.form.get("chemical").title()
        amount = request.form.get("amount")
        unit = request.form.get("unit")
        # strip decimals from time, (first convert to str)
        now = datetime.now()
        s = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        time = s[:16]
        
        priority = request.form.get("priority").title()
        with sqlite3.connect(db_path) as db:
            data = (chemical, amount, unit, time, priority)
            print(data)
            db.execute("INSERT INTO orders (chemical, amount, unit, time, priority) VALUES (?, ?, ?, ?, ?)", data)
        return render_template("buy.html")
        
        
@app.route('/purchase_database')
def purchase_database():
    # Show results from database, ordered with most recent at top
    with sqlite3.connect(db_path) as db:
        data = db.execute("SELECT * FROM orders ORDER BY time DESC")
        return render_template("purchase_database.html", orders = data)
    
@app.route('/purchase', methods = (["GET", "POST"]))
def purchase():
    if request.method == "POST":
        # Get data about purchase from posted form
        chemical = request.form.getlist("chemical") 
        amount = request.form.getlist("amount")
        unit = request.form.getlist("unit")
        date = request.form.getlist("date")
        print(chemical, amount, unit, date)
        # Get current time 
        now = datetime.now()
        s = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        time = s[:16]
        # Add purchase time to database
        with sqlite3.connect(db_path) as db:
            db.execute(f"UPDATE orders SET purchase_time = ? WHERE time = '{date[0]}'", (time,))
            data = db.execute("SELECT * FROM orders ORDER BY time DESC")
            return render_template("purchase_database.html", orders = data)

@app.route('/sds', methods = ["GET", "POST"])
def sds():
    if request.method == "GET":
        return render_template("sds.html")
    else:
        filepath = "/Users/joelpaull/cs50/CS50/final_project/find_sds/find_sds/SDS"
        pool = int(1)
        cas = request.form.get("cas")
        find_sds.find_sds([cas])
        return send_from_directory(filepath, (cas + '-SDS.pdf'))

        