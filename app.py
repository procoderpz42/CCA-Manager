from bs4 import BeautifulSoup
from contextlib import closing
from datetime import timedelta
from datetime import datetime
from hashlib import sha256
from flask import Flask, url_for, redirect, render_template, request, session
import sqlite3
from secrets import token_urlsafe
import re





app = Flask(__name__)
app.secret_key = token_urlsafe(32)
app.permanent_session_lifetime = timedelta(minutes=10)

# special functions here

def query(db_name, sql, values=()): # Queries the database
    # connection closes after with block
    with closing(sqlite3.connect(db_name)) as con, con, \
            closing(con.cursor()) as cur:
        cur.execute(sql, values)
        return cur.fetchall()

def hashhex(str): # return a hash of the input. this is a function so that there is no instance of incorrect hash being used 
    return sha256(str.encode()).hexdigest()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


# links here
@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if "uid" in session: # Checking if already logged in
        return redirect(url_for("home"))
    if request.method == "POST":

        position = request.form.get("position")
        username = request.form.get("Username")
        password = request.form.get("Password")
        hashed_password = hashhex(password)
        result = query("Server.db", f"SELECT id FROM {position} WHERE nric = ? AND hashedpassword = ? LIMIT 1;", (username, hashed_password))
        if len(result) != 1: # did not pull correct record
            return render_template("Login.html", error="Entered partculars are Wrong")
        
        session["position"] = position    # ADD Position Status
        session["uid"] = result[0][0]  # ADD Person Id
        result = query("Server.db", f"SELECT id, firstname, lastname, email, nric FROM {session['position']} WHERE id = ? LIMIT 1;", (session['uid'],))[0]
        session["email"] = result[3]
        session["firstname"] = result[1]
        session["lastname"] = result[2]
        session["nric"] = result[4]
        session.permanent = True
        return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("Login.html", error="")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "uid" in session: # Checking if already logged in
        return redirect(url_for("home"))
    if request.method == "POST":
        # check if the passwords match
        password = hashhex(request.form.get("password"))
        re_enter_password = hashhex(request.form.get("password-reenter"))
        if password == re_enter_password:
            hashed_password = password
        else:
            return render_template("Register.html", error="Passwords don't Match Try Again")

        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        nric = request.form.get("nric")
        email = request.form.get("email") # no checks yet maybe a email veri?? Gonna have to search that up 
        position = request.form.get("position")

        if not validate_email(email): # Email format check
            return render_template("Register.html", error="Email Invalid")

        if len(nric) != 9: # Nric length check
            return render_template("Register.html", error="NRIC Invalid")

        query("Server.db", f"INSERT INTO {position.lower()} (firstname, lastname, email, nric, hashedpassword) \
                    Values (?, ?, ?, ?, ?) ", (first_name, last_name, email, nric, hashed_password))
        return redirect(url_for("/login"))

    elif request.method == "GET":
        return render_template("Register.html", error="")
    
@app.route("/logout")
def logout(): # logout and go to login page
    session.clear()
    return redirect(url_for('login'))


@app.route("/home")
def home():
    return redirect(url_for("profile"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "uid" not in session: # Checking if not already logged in
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("Profile.html", session=session)
    elif request.method == "POST":
        pos = session["position"]
        f_name = request.form.get('First_name')
        l_name = request.form.get('Last_name')
        email = request.form.get('Email')
        nric = request.form.get('Nric')

        if not validate_email(email): # email format check
            return render_template("Profile.html", session=session, error="Email Invalid")
        
        if len(nric) != 9: # NRIC length check
            return render_template("Profile.html", session=session, error="NRIC Invalid")
        # update session
        session['firstname'] = f_name
        session['lastname'] = l_name
        session['email'] = email
        session['nric'] = nric
        #update Database
        query("Server.db", f"UPDATE {pos} SET firstname = ?, lastname = ?, email = ?, nric = ? WHERE id = ?;", (f_name, l_name, email, nric, session['uid']))

        return render_template("Profile.html", session=session, error="")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "uid" not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        if hashhex(request.form.get("cur_pass")) == query("Server.db", f"SELECT hashedpassword FROM {session['position']} WHERE id = ?;", (session["uid"],))[0][0]:
            if request.form.get("1newpass") == request.form.get("2newpass"):
                query("Server.db", f"UPDATE {session['position']} SET hashedpassword = ? WHERE id = ?", (hashhex(request.form.get('1newpass')), session["uid"]))
                return redirect(url_for('profile'))
            else:
                return render_template("Change_password.html", session=session, error='New password do not match')
        else:
            return render_template("Change_password.html", session=session, error='Current Password Incorrect')
    elif request.method == "GET":
        return render_template("Change_password.html", session=session)
 
@app.route("/cca_session", methods=["GET"])
def cca_session():
    if "uid" not in session:
        return redirect(url_for("login"))
    if request.method == "GET":
        results = query('Server.db', """
                                    SELECT session.sessionid, cca.name, session.date, session.starttime 
                                    FROM session
                                    INNER JOIN cca ON session.ccaid = cca.id
                                    WHERE year = ?;
                                    """, (int(datetime.now().year),))
        print(results)
        return render_template("Sessions.html", session=session, results=results)

@app.route('/make_session', methods=["GET", "POST"])
def make_session():
    if "uid" not in session:
        return redirect(url_for("login"))
    ccas = query("Server.db", """
            SELECT id, name
            FROM cca
            ORDER BY name;""")
    teachers = query("Server.db", """
            SELECT id, firstname||' '||lastname
            FROM teacher
            ORDER BY firstname;""")
    if request.method == "GET":
        return render_template("Make_session.html", session=session, ccas=ccas, teachers=teachers)
    elif request.method == "POST":
        cca = request.form.get("cca")
        teacheric = request.form.get("teacheric")
        teacher_a = request.form.get("teacher_a")
        date = request.form.get("date")
        year = datetime.strptime(date, "%Y-%m-%d").year
        start = request.form.get("start")
        end = request.form.get("end")
        dt_start = datetime.strptime(start, "%H:%M")
        dt_end = datetime.strptime(end, "%H:%M")
        print(cca,teacheric,teacher_a, date, year,start,end,dt_start,dt_end)
        if teacher_a == teacheric:
            return render_template("Make_session.html", session=session, ccas=ccas, teachers=teachers, error="Teacher In Charge and Assistant Teacher are the Equal")
        if dt_start >= dt_end:
            return render_template("Make_session.html", session=session, ccas=ccas, teachers=teachers, error="Start Time and End Time are Wrong Or The Same")

        query("Server.db", """
                                INSERT INTO session(ccaid, teacheric, assistantic, year, date, starttime, endtime)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""", (cca, teacheric, teacher_a, year, date, start, end))
        return redirect(url_for('cca_session'))
    
@app.route("/get_session", methods=["POST", "GET"])
def get_session():
    if "uid" not in session:
        return redirect(url_for("login"))
    if request.method == "GET":
        sessionid = request.args.get("session_id")
        results = query("Server.db", """
                                SELECT student.firstname||' '||student.lastname, student.id, attendance.attendance
                                FROM student
                                LEFT OUTER JOIN registar
                                ON student.id = registar.studentid
                                LEFT OUTER JOIN session
                                ON registar.ccaid = session.ccaid
                                LEFT OUTER JOIN attendance
                                ON attendance.studentid = student.id
                                WHERE session.sessionid = ?;
""", values=(sessionid,))
        print(sessionid)
        print(results)
        return render_template("Get_session.html", results=results, session_id=sessionid)
    if request.method == "POST":
        sessionid = request.form.get("session_id")
        results = query("Server.db", """
                                SELECT student.id
                                FROM student
                                LEFT OUTER JOIN registar
                                ON student.id = registar.studentid
                                LEFT OUTER JOIN session
                                ON registar.ccaid = session.ccaid
                                LEFT OUTER JOIN attendance
                                ON attendance.studentid = student.id
                                WHERE session.sessionid = ?;
""", values=(sessionid,))
        attendance = []
        for item in results:
            search_id = item[0]
            attendance.append((search_id, request.form.get(str(search_id))))
        
        for item in attendance:
            if item[1] == 'Absent':
                if len(query("Server.db", "SELECT * FROM attendance WHERE sessionid = ? AND studentid = ?", (sessionid, item[0]))) > 0:
                    query("Server.db", "DELETE FROM attendance WHERE studentid = ? AND sessionid = ?", (item[0], sessionid))
            else:
                if len(query("Server.db", "SELECT * FROM attendance WHERE sessionid = ? AND studentid = ?", (sessionid, item[0]))) > 0:
                    query("Server.db", "UPDATE attendance SET attendance = ? WHERE sessionid = ? AND studentid = ?", (item[1], sessionid, item[0]))
                else:
                    query("Server.db", """
                                INSERT INTO attendance (sessionid, studentid, attendance)
                                VALUES (?, ?, ?)""", (sessionid, item[0], item[1]))
        return redirect(url_for('cca_session'))
        
if __name__=="__main__":
    app.run(debug=False, port=10000)

