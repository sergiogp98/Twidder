from flask import Flask, request, jsonify, send_from_directory
from geventwebsocket.exceptions import WebSocketError
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import database_handler
from random import choice
from string import ascii_lowercase
import json
import re

n = 30 #Length of the token
socketsArray = {}
app = Flask(__name__)
app.debug = True

@app.teardown_request
def after_request(exception):
    database_handler.disconnect_db()

@app.route('/')
@app.route('/client_html')
def client_page():
    return send_from_directory('static', 'client.html')

@app.route('/sign-in',methods = ['POST'])
def sign_in():
    email = request.json['email']
    password = request.json['password']
    userExists = database_handler.check_user(email, password)

    if userExists is True:
        token = "".join(choice(ascii_lowercase) for i in range(n))
        database_handler.insert_token(token, email)
        return jsonify({'success': True, 'message': "Successfully retrieved user data",'token': token})
    else:
        return jsonify({'success': False, 'message': "Incorrect email or password"})

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

        if result is True:
            return jsonify({'success': True, 'message': "Successfully sign up"})
        else:
            return jsonify({'success': False, 'message': "Unsuccessfully sign up"})
    else:
        return jsonify({'success': False, 'message': "Field empty or password less than 8 characters"})

@app.route('/sign-out',methods = ['POST'])
def sign_out():
    token = request.headers["Authorization"].split(" ")[1]
    email = database_handler.get_email(token)

    if email is not False:
        database_handler.remove_user_login(email)
        return jsonify({'success': True, 'message': "Successfully sign out"})
    else:
        return jsonify({'success': False, 'message': "Unsuccessfully sign out"})

@app.route('/change-password',methods = ['PUT'])
def change_password():
    token = request.headers["Authorization"].split(" ")[1]
    old_password = request.json['oldPassword']
    new_password = request.json['newPassword']
    result = database_handler.change_pwd(token, new_password, old_password)

    if result is True:
        return jsonify({'success': True, 'message': "Successfully changed password"})
    else:
        return jsonify({'success': False, 'message': "The password is not correct"})

@app.route('/get-data/',methods = ['GET'])
def get_user_data_by_token():
    token = request.headers["Authorization"].split(" ")[1]
    token_valid = database_handler.check_token(token)

    if token_valid is True: #Token is still valid
        email = database_handler.get_email(token)['email'] #User to retrieve data for
        result = database_handler.get_user_data_by_email(email)
        if result is not False: #User is registered in the database
            return jsonify({'success': True, 'message': "Successfully retrieved user data", 'data': result})
        else:
            return jsonify({'success': False, 'message': "User is not found on the database"})
    else:
        return jsonify({'success': False, 'message': "The token is not valid"})

@app.route('/get-data/<email>',methods = ['GET'])
def get_user_data_by_email(email):
    token = request.headers["Authorization"].split(" ")[1]
    token_valid = database_handler.check_token(token)
    if token_valid is True: #Token is still valid
        result = database_handler.get_user_data_by_email(email)
        if result is not False: #User is registered in the database
            return jsonify({'success': True, 'message': "Successfully retrieved user data", 'data': result})
        else:
            return jsonify({'success': False, 'message': "User is not found on the database"})
    else:
        return jsonify({'success': False, 'message': "The token is not valid"})

@app.route('/get-data/message/',methods = ['GET'])
def get_user_messages_by_token():
    token = request.headers["Authorization"].split(" ")[1]

    data = database_handler.get_email(token)

    if data['token'] == token:
        result = database_handler.get_user_messages_by_token(token)
        return jsonify({'success': True, 'message': "Successfully retrieved user data", 'data': result})
    else :
        return jsonify({'success': False, 'message': "The token does not match"})

@app.route('/get-data/message/<email>',methods = ['GET'])
def get_user_messages_by_email(email):
    #token = request.headers["Authorization"].split(" ")[1]
    token = request.headers["Authorization"].split(" ")[1]

    email_receiver = email

    email_sender = database_handler.get_email(token)['email']

    if email_sender is not False:

        result = database_handler.get_user_messages_by_email(email_receiver)

        return jsonify({'success': True, 'message': "Successfully retrieved user data", 'data': result})
    else :
        return jsonify({'success': False, 'message': "The token does not match or the token does not exist"})

@app.route('/message',methods = ['POST'])
def post_message():
    token = request.headers["Authorization"].split(" ")[1]
    email_sender = database_handler.get_email(token)['email']

    message = request.json['message']
    email_receiver = request.json['email']
    messagePosted = database_handler.post_message(email_sender, message, email_receiver)

    if messagePosted is True:
        return jsonify({'success': True, 'message': "Message posted"})
    else:
        return jsonify({'success': False, 'message': "Message not posted"})

@app.route('/api')
def connectionSocket():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']

        email = ws.receive()
        if email in socketsArray:
            socketsArray[email].send("sign_out")
        socketsArray[email]=ws
    
        try:
            while True:
                email = ws.receive()
        except:
            return "oops"



if __name__ == '__main__':
    #app.run()
    http_server = WSGIServer(('',5000),app,handler_class = WebSocketHandler)
    http_server.serve_forever()
