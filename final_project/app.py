from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from pip._vendor import requests
URL = "https://commonchemistry.cas.org/api/search?"


# Configure Flask
app = Flask(__name__)

def find_cas(chemical):
    ''' Return chemical CAS number'''
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
        # Show details of search results 
        return render_template("search_details.html", cas_number = cas_number)

@app.route("/search_details")
def index():
    return render_template("search_details.html")
        
        