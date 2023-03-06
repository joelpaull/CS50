import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import random
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# export API_KEY=pk_0c218e086faf46338d470faa5d470ece

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    # Display stocks in table
    stocks = db.execute(
        f"SELECT stock, SUM(amount), name, cost, total FROM user_stock WHERE user_id = ? GROUP BY stock", session['user_id'])
    totals = db.execute(f"SELECT SUM(total) FROM user_stock WHERE user_id = ? GROUP BY stock", session['user_id'])

    to_remove = []
    for i in range(len(stocks)):
        if stocks[i]["SUM(amount)"] == 0:
            to_remove.append(stocks[i])
    for i in to_remove:
        stocks.remove(i)

    # Get total value of stock portfolio
    total_stock_portfolio = 0
    for stock in totals:
        total_stock_portfolio += stock["SUM(total)"]
    cash = db.execute(f"SELECT cash FROM users WHERE id = ?", session['user_id'])[0]["cash"]
    return render_template("index.html", stocks=stocks, cash=cash, total_stock_portfolio=total_stock_portfolio)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # Get details from form
        symbol = request.form.get("symbol")
        form_shares = request.form.get("shares")

        try:
            shares = int(form_shares)

        except ValueError:
            return apology("Cannot Buy Partial Shares")

        if form_shares.isalpha():
            return apology("Please Enter Valid Number")

        shares = int(form_shares)
        if shares <= 0:
            return apology("Cannot Buy Negative Stock")

        # Get stock details
        stock_details = lookup(symbol)
        if not stock_details:
            return apology("Could Not Find Stock")

        # Determine moneties values of exchange
        total_price = stock_details["price"] * float(shares)
        available_cash = db.execute(f"SELECT cash FROM users WHERE id = ?", session['user_id'])[0]["cash"]

        if total_price <= available_cash:
            can_buy = True
        else:
            return apology("Please Deposit More Funds")

        if can_buy:

            # add stock into database of id
            time = datetime.now()
            print(time)
            db.execute("INSERT INTO user_stock (user_id, stock, name, amount, cost, total, time) VALUES(?, ?, ?, ?, ?, ?,?)",
                       session['user_id'], stock_details["symbol"], stock_details["name"], shares, stock_details["price"], stock_details["price"] * shares, time)

            # Determine funds now in account
            new_cash_amount = available_cash - total_price
            db.execute(f"UPDATE users SET cash = ? WHERE id = ?", new_cash_amount, session['user_id'])
            return redirect("/")


@app.route("/history")
@login_required
def history():
    stocks = db.execute("SELECT * FROM user_stock WHERE user_id = ?", session["user_id"])
    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if stock == None:
            return apology("Please Enter Valid Stock Symbol")
        else:
            name = stock["name"]
            return render_template("quote_details.html", stock=stock, name=name)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Determine charactors in password

        letters = numbers = special = 0
        for char in password:
            if char.isalpha():
                letters += 1
            elif char.isnumeric():
                numbers += 1
            else:
                special += 1

        usernames = db.execute("SELECT username FROM users")

        for user in usernames:
            if user["username"] == username:
                return apology("Username Taken")

        if username == "" or password == "":
            return apology("Please Ensure All Entries are Filled")

        elif username in db.execute("SELECT username FROM users"):
            return apology("Username Taken")

        elif password != confirmation:
            return apology("Passwords Do Not Match")

        elif len(password) < 7:
            return apology("Password Needs To Be of Min Length 8")

        elif letters == 0:
            return apology("Password Needs Min. 1 Letter")
        elif numbers == 0:
            return apology("Password Needs Min. 1 Number")
        elif special == 0:
            return apology("Password Needs Min. 1 Special Character")

        else:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        symbols = db.execute("SELECT stock FROM user_stock WHERE user_id = ? GROUP BY stock", session['user_id'])
        return render_template("sell.html", symbols=symbols)
    else:
        # Get details from form
        symbol = request.form.get("symbol").upper()
        amount_to_sell = int(request.form.get("shares"))

        # Determine how much of stock x is in portfoliio
        try:
            stock_in_portfolio = int(db.execute(
                "SELECT SUM(amount) FROM user_stock WHERE user_id = ? AND stock = ?", session["user_id"], symbol)[0]["SUM(amount)"])
        except TypeError:
            return apology("None of This Stock Owned")

        if amount_to_sell < 0:
            return apology("Cannot Sell Negative Number of Stock")
        elif stock_in_portfolio >= amount_to_sell:
            can_sell = True

        else:
            return apology("Not enough stock")

        # Return money to funds if stock available in portfolio to sell
        if can_sell:
            available_cash = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
            cost_of_stock = lookup(symbol)["price"]
            name = lookup(symbol)["name"]
            money_to_refund = amount_to_sell * cost_of_stock
            new_total = money_to_refund + available_cash

            # Database call to change users money and stocks in portfolio
            time = datetime.now()
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_total, session["user_id"])
            db.execute("INSERT INTO user_stock (user_id, stock, amount, cost, total, time, name) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       session['user_id'], symbol, (-1 * amount_to_sell), cost_of_stock, (-1 * money_to_refund), time, name)

            return redirect("/")
