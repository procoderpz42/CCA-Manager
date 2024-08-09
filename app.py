from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from contextlib import closing
from hashlib import sha256
import secrets
from datetime import datetime



app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

def query(db_name, sql):
    with closing(sqlite3.connect(db_name)) as con, con,  \
            closing(con.cursor()) as cur:
        cur.execute(sql)
        return cur.fetchall()


@app.route("/")
def home():
    if "userid" not in session:
        return redirect(url_for("login"))
    else:
        result = query("Server.db", f"SELECT firstname, email FROM {session["position"]} WHERE {session["position"]}id = '{session["userid"]}' LIMIT 1;")[0]
        session["email"] = result[1]
        session["firstname"] = result[0]
        print(session["email"])
        return render_template("HomePage.html", session=session)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "userid" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        position = request.form.get("position")
        username = request.form.get("Username")
        password = request.form.get("Password")
        hashed_password = sha256(password.encode()).hexdigest()

        result = query("Server.db", f"SELECT {position}id AS id FROM {position} WHERE nric = '{username}' AND hashedpassword = '{hashed_password}' LIMIT 1;")
        if len(result) != 1:
            return render_template("Login.html", error="Entered partculars are Wrong")
        session["position"] = position
        session["userid"] = result[0][0]
        return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("Login.html", error="")

@app.route("/register", methods=["GET", "POST"])
def register(): # this method will only ever handle post requests
    if "userid" in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        if sha256(request.form.get("password").encode()).hexdigest() == sha256(request.form.get("password-reenter").encode()).hexdigest():
            hashed_password = sha256(request.form.get("password-reenter").encode()).hexdigest()
        else:
            return render_template("Register.html", error="Passwords don't Match Try Again")

        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        nric = request.form.get("nric") 
        if len(nric) != 9:
            return render_template("Register.html", error="NRIC Invalid")
        email = request.form.get("email")
        position = request.form.get("position")

        query("Server.db", f"INSERT INTO {position.lower()} (firstname, lastname, email, nric, hashedpassword) \
                    Values (?, ?, ?, ?, ?) ", (first_name, last_name, email, nric, hashed_password))
        return redirect(url_for("/login"))

    elif request.method == "GET":
        return render_template("Register.html", error="")
if __name__=="__main__":
    app.run(debug=True, port=2000)