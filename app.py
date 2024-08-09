from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from hashlib import sha256

app = Flask(__name__)

@app.route("/")
def Home():
    return "Base test"

@app.route("/register", methods=["GET", "POST"])
def register(): # this method will only ever handle post requests
    if request.method == "POST":
        user_name = request.form.get("username")
        password = sha256(request.form.get("password"))
        email = request.form.get("email")


    elif request.method == "GET":
        return render_template("Register.html")
if __name__=="__main__":
    app.run(debug=True, port=2000)