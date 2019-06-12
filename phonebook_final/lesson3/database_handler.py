import sqlite3
from flask import g

DATABASE = "database.db"

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE)
    return db

def disconnect_db():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()


def insert_contact(name, number):
    try:
        get_db().execute("insert into contact values(?,?)", [name, number])
        #get_db().execute("insert into contact(" + name + "," + numbner +   ")") bad idea!!!
        get_db().commit()
        return True
    except:
        return False

def read_contact(number):
    cursor = get_db().execute("select * from contact where number like ?", [number])
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'name':rows[index][0], 'number' : rows[index][1]})

    return result

#added code to lesson two.
#It is important that the returned output has a structure like save_contact()
def read_contact_by_name(name):
    cursor = get_db().execute("select * from contact where name like ?", [name])
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'name':rows[index][0], 'number' : rows[index][1]})

    return result
