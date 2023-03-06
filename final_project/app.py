from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from pip._vendor import requests
API_KEY = CtaQQ04zfxvU2PValOpLAvOL3jGwbnYx
url = https://api.rsc.org/compounds/v1

# Configure Flask
app = Flask(__name__)

def find_chem(chemical):
    ''' Look up chemical against API'''
    # Api Key
    api_key = API_KEY
    
    

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        chemical = request.form.get("chemical")