import sqlite3
from flask import g
import os

DATABASE = "database.db"
SCHEMA = "schema.sql"

def open_Db():
    if not os.path.exists(DATABASE):
        database = sqlite3.connect(DATABASE)
        schm= open(SCHEMA, 'r')
        schmString = schm.read()
        database.executescript(schmString)
    else:
        database = sqlite3.connect(DATABASE)
    pass

    return database

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def disconnect_db():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()

def insert_user(email, password, firstname, familyname, gender, city, country): #Insert in users table
    try:
        get_db().execute("insert into users values(?,?,?,?,?,?,?)", [email, password, firstname, familyname, gender, city, country])
        get_db().commit()
        return True
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        return False
    except Exception as e:
        print("Exception in _query: %s" % e)
        return False

def remove_user_login(email):
    try:
        get_db().execute("delete from loggued where email = ? ", [email])
        get_db().commit()
        return True
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        return False
    except Exception as e:
        print("Exception in _query: %s" % e)
        return False

def insert_token(token, email): #Insert in loggued table
    try:
        result = get_loggued(email)
        if result is False:
            get_db().execute("insert into loggued values(?,?)", [email ,token])
            get_db().commit()
            return True
        else:
            get_db().execute("update loggued set token = ? where email = ?", [token,email])
            get_db().commit()
            return True

    except sqlite3.Error as e:
        print("Database error: %s" % e)
    except Exception as e:
        print("Exception in _query: %s" % e)

def change_pwd(token, new_password, old_password):
    try:
        email = get_email(token)
        userExists = check_user(email['email'], old_password)
        if userExists is True:
            get_db().execute("update users set password = ? where email =  ?", [new_password, email['email']])
            get_db().commit()
            return True
        else:
            return False
    except sqlite3.Error as e:
        return False
    except Exception as e:
        return False

def post_message(email_sender, message, email_receiver):
    try:
        get_db().execute("insert into messages (email_sender, message, email_receiver) values(?,?,?)", [email_sender, message, email_receiver])
        get_db().commit()
        return True
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        return False
    except Exception as e:
        print("Exception in _query: %s" % e)
        return False

def check_user(email, password):
    try:
        cursor = get_db().execute("select * from users where (email like ? and password like ?)", [email, password])
        rows = cursor.fetchall()[0]
        cursor.close()
        if email == rows[0] and password == rows[1]:
            return True
    except sqlite3.Error as e:
        return False
    except Exception as e:
        return False

def get_loggued(email):
    try:
        cursor = get_db().execute("select * from loggued where email = ?", [email])
        rows = cursor.fetchall()[0]
        cursor.close()
        return {'email' : rows[0]}
    except sqlite3.Error as e:
        return False
    except Exception as e:
        return False

def get_user_messages_by_token(token):
    cursor = get_db().execute("select * from messages where token = ?", [token])
    rows = cursor.fetchall()[0]
    cursor.close()
    result = []
    result.append({'token' : rows[0],'message' : rows[1], 'email' : rows[2]})

    return result

def get_user_messages_by_email(email_receiver):

    cursor = get_db().execute("select * from messages where  email_receiver = ?", [email_receiver])
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'email_sender' : rows[index][1],'message' : rows[index][2]})

    return result

def get_email(token):
    try:
        cursor = get_db().execute("select * from loggued where token = ?", [token])
        rows = cursor.fetchall()[0]
        cursor.close()
        return {'email' : rows[0]}
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        return False
    except Exception as e:
        print("Exception in _query: %s" % e)
        return False

def check_token(token): #Check if a token is still valid
    try:
        cursor = get_db().execute("select token from loggued where token = ?", [token])
        rows = cursor.fetchall()[0]
        cursor.close()
        return rows[0] == token
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        return False
    except Exception as e:
        print("Exception in _query: %s" % e)
        return False

def get_user_data_by_email(email):
    try:
        cursor = get_db().execute("select * from users where email = ?", [email])
        rows = cursor.fetchall()[0]
        cursor.close()
        return {'email' : rows[0],'firstname' : rows[2],
                'familyname' : rows[3], 'gender' : rows[4],
                'city' : rows[5],'country' : rows[6]}
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        return False
    except Exception as e:
        print("Exception in _query: %s" % e)
        return False

def print_all_users():
    cursor = get_db().execute("select * from users")
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'email' : rows[index][0], 'password' : rows[index][1]})

    return result

def print_all_loggued():
    cursor = get_db().execute("select * from loggued")
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'email' : rows[index][0], 'token' : rows[index][1] })

    return result

def print_all_messages(email_receiver):
    cursor = get_db().execute("select * from messages where email_receiver like ?", [email_receiver])
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'email_sender' : rows[index][1], 'messages' : rows[index][2]})
    return result
