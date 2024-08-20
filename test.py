from datetime import datetime
from bs4 import BeautifulSoup
from contextlib import closing
from datetime import timedelta
from datetime import datetime
from hashlib import sha256
from flask import Flask, url_for, redirect, render_template, request, session
import sqlite3
from secrets import token_urlsafe
import re

def query(db_name, sql, values=()): # Queries the database
    # connection closes after with block
    with closing(sqlite3.connect(db_name)) as con, con, \
            closing(con.cursor()) as cur:
        cur.execute(sql, values)
        return cur.fetchall()
    
sessionid = 1
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
""", (sessionid,))

for line in results:
    print(line)