import sqlite3

import random
from hashlib import sha256
from contextlib import closing


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
def query(db_name, sql, values=None):
    with closing(sqlite3.connect(db_name)) as con, con,  \
            closing(con.cursor()) as cur:
        cur.execute(sql, values)
        return cur.fetchall()

ccas = [  
    {"name": "Art Club", "location": "School Art Room"},  
    {"name": "Basketball", "location": "School Gym or Community Sports Complex"},  
    {"name": "Drama Club", "location": "School Auditorium"},  
    {"name": "Music Band", "location": "School Music Room"},  
    {"name": "Science Club", "location": "School Science Lab"},  
    {"name": "Debate Club", "location": "School Classroom"},  
    {"name": "Football", "location": "Community Sports Field"},  
    {"name": "Swimming", "location": "Community Swimming Pool"},  
    {"name": "Robotics Club", "location": "School Tech Lab"},  
    {"name": "Eco Club", "location": "Community Garden or School Grounds"},
    {"name": "Chess Club", "location": "School Library"},
    {"name": "Photography Club", "location": "School Darkroom or Outdoor Spaces"},
    {"name": "Guitar Ensemble", "location": "School Music Room"},
    {"name": "Cooking Club", "location": "Home Economics Room or School Kitchen"},
    {"name": "Coding Club", "location": "School Computer Lab"},
    {"name": "Nature Society", "location": "School Garden or Nature Reserve"},
    {"name": "Language Club", "location": "School Language Lab"},
    {"name": "Community Service Club", "location": "Various Community Locations"},
    {"name": "Fashion Design Club", "location": "School Art Room"},
    {"name": "Film Club", "location": "School AV Room or Theater"}
]

for item in ccas:
    name = item["name"]
    venue = item["location"]
    mem_cap = random.randint(10,40)

    query("Server.db", "INSERT INTO cca (name, member_count, venue) VALUES (?, ?, ?)", (name, mem_cap, venue))