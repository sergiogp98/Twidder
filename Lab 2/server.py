from flask import Flask, request, jsonify
import database_handler
from random import choice
from string import ascii_lowercase
import json
import re






n = 30

app = Flask(__name__)
app.debug = True

@app.teardown_request
def after_request(exception):
    database_handler.disconnect_db()

@app.route('/sign-in',methods = ['POST'])
def sign_in():

    username = request.json['email']
    password = request.json['password']
    user = database_handler.get_user(username)
    #print(user[0]['password'])
    if user is not False:
        if username and password:
            if user['email'] == username and user['password'] == password:
                token = "".join(choice(ascii_lowercase) for i in range(n))
                database_handler.insert_token(token,username)
                return jsonify(database_handler.print_all_loggued())
                #return jsonify({'success': True, 'message': "successfully retrieved user data", 'token': token})
            else:
                return jsonify({'success': False, 'message': "Incorrect password or email"})
        else:
            return jsonify({'success': False, 'message': "password empty or Unknown username"})
    else:
        return jsonify({'success': False, 'message': "Unsuccessfully sign in"})



@app.route('/sign-up',methods = ['POST'])
def sign_up():
    email = request.json['email']
    password = request.json['password']
    firstname = request.json['firstname']
    familyname = request.json['familyname']
    gender = request.json['gender']
    city = request.json['city']
    country = request.json['country']
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    if len(password)>7 and firstname is not None and familyname is not None and city is not None and country is not None and match is not None:
        result = database_handler.insert_user(email,password,firstname,familyname,gender,city,country)
        #return jsonify(database_handler.print_all_users())
        if result is not False:
            return jsonify({'success': True, 'message': "successfully sign up"})
        else:
            return jsonify({'success': False, 'message': "unsuccessfully sign up"})
    else:
            return jsonify({'success': False, 'message': "Field empty or password less than 8 characters"})



@app.route('/sign-out',methods = ['POST'])
def sign_out():
    token = request.headers["Authorization"].split(" ")[1]
    data = database_handler.get_email(token)
    print(data)
    if data is not False:
        if data['token'] == token:
            database_handler.remove_user_login(token)
            jsonify(database_handler.print_all_loggued())
            return jsonify({'success': True, 'message': "successfully sign out"})
        else :
            return jsonify({'success': False, 'message': "The password is not correct"})
    else:
        return jsonify({'success': False, 'message': "unsuccessfully sign out"})



@app.route('/change-password',methods = ['PUT'])
def change_password():
    token = request.headers["Authorization"].split(" ")[1]
    password = request.json['password']
    new_password = request.json['new_password']
    #Preguntar si la pwd debe tener una longitud
    result = database_handler.change_pwd(token,new_password,password)
    if result:
        return jsonify({'success': True, 'message': "successfully changed password"})
    else:
        return jsonify({'success': False, 'message': "The password is not correct"})




@app.route('/get-data/',methods = ['GET'])
def get_user_data_by_token():
    token = request.headers["Authorization"].split(" ")[1]
    data = database_handler.get_email(token)#I want the email
    if data is not False:
        result = database_handler.get_user_data_by_email(data['email'])
        return jsonify({'success': True, 'message': "successfully retrieved user data", 'data': result})
    else:
        return jsonify({'success': False, 'message': "The token does not match"})


@app.route('/get-data/email',methods = ['GET'])
def get_user_data_by_email():
    token = request.headers["Authorization"].split(" ")[1]
    email = request.json['email']
    data = database_handler.get_email(token)
    if data['email'] == email and data['token'] == token:
        result = database_handler.get_user_data_by_email(email)
        return jsonify({'success': True, 'message': "successfully retrieved user data", 'data': result})
    else:
        return jsonify({'success': False, 'message': "The email or the token does not match"})

@app.route('/get-data/message/',methods = ['GET'])
def get_user_messages_by_token():
    token = request.headers["Authorization"].split(" ")[1]
    data = database_handler.get_email(token)
    if data is not False:
        result = database_handler.get_user_messages_by_token(data['email'])
        return jsonify({'success': True, 'message': "successfully retrieved user data", 'data': result})
    else :
        return jsonify({'success': False, 'message': "The token does not match"})

@app.route('/message',methods = ['POST'])
def post_message():
    token = request.headers["Authorization"].split(" ")[1]
    email_sender = database_handler.get_email(token)
    message = request.json['message']
    email_receiver = request.json['email']
    if email_sender is not False:
        data = database_handler.post_message(email_sender['email'], message, email_receiver)
        return jsonify(database_handler.print_all_messages())
    else:
        return jsonify({'success': False, 'message': "The token does not match"})





@app.route('/get-data/message/email',methods = ['GET'])
def get_user_messages_by_email():
    token = request.headers["Authorization"].split(" ")[1]
    #email_sender = database_handler.get_email(token)['email']
    email_receiver = request.json['email']
    data = database_handler.get_email(token)
    if data is not False: #and data['email'] == email_receiver:
        result = database_handler.get_user_messages_by_email(email_receiver)
        return jsonify({'success': True, 'message': "successfully retrieved user data", 'data': result})
    else :
        return jsonify({'success': False, 'message': "The token does not match or the token does not exist"})



app.run()
