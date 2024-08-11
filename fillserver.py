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

ccas = [{'name': 'Art Club', 'location': 'School Art Room', 'Count': 75}, 
        {'name': 'Basketball', 'location': 'School Gym or Community Sports Complex', 'Count': 75}, 
        {'name': 'Drama Club', 'location': 'School Auditorium', 'Count': 75}, 
        {'name': 'Music Band', 'location': 'School Music Room', 'Count': 75}, 
        {'name': 'Science Club', 'location': 'School Science Lab', 'Count': 75}, 
        {'name': 'Debate Club', 'location': 'School Classroom', 'Count': 75}, 
        {'name': 'Football', 'location': 'Community Sports Field', 'Count': 75}, 
        {'name': 'Swimming', 'location': 'Community Swimming Pool', 'Count': 75}, 
        {'name': 'Robotics Club', 'location': 'School Tech Lab', 'Count': 75}, 
        {'name': 'Eco Club', 'location': 'Community Garden or School Grounds', 'Count': 75}, 
        {'name': 'Chess Club', 'location': 'School Library', 'Count': 75}, 
        {'name': 'Photography Club', 'location': 'School Darkroom or Outdoor Spaces', 'Count': 75}, 
        {'name': 'Guitar Ensemble', 'location': 'School Music Room', 'Count': 75}, 
        {'name': 'Cooking Club', 'location': 'Home Economics Room or School Kitchen', 'Count': 75}, 
        {'name': 'Coding Club', 'location': 'School Computer Lab', 'Count': 75}, 
        {'name': 'Nature Society', 'location': 'School Garden or Nature Reserve', 'Count': 75}, 
        {'name': 'Language Club', 'location': 'School Language Lab', 'Count': 75}, 
        {'name': 'Community Service Club', 'location': 'Various Community Locations', 'Count': 75}, 
        {'name': 'Fashion Design Club', 'location': 'School Art Room', 'Count': 75}, 
        {'name': 'Film Club', 'location': 'School AV Room or Theater', 'Count': 75}]

# for item in ccas:
#     item["Count"] = 75

for student in student_table:
    a = True
    while a:
        chosen_cca = random.choice(ccas)
        if chosen_cca["Count"] > 0:
            

# query("Server.db", "INSERT INTO cca (name, member_count, venue) VALUES (?, ?, ?)", (name, mem_cap, venue))