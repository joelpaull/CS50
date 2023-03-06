from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Configure Flask
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("layout.html")