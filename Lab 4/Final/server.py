from flask import Flask, request, jsonify, send_from_directory,app
from geventwebsocket.exceptions import WebSocketError
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import database_handler,sec
from random import choice
from flask_bcrypt import Bcrypt
import re
from string import ascii_lowercase
import json
import hashlib
import database_handler






n = 30 #Length of the token
socketsArray = {}
app = Flask(__name__)
bcrypt = Bcrypt(app)
sec.init(bcrypt)
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
        publicKey = "".join(choice(ascii_lowercase) for i in range(n))
        database_handler.insert_token(token, email,publicKey)
        return jsonify({'success': True, 'message': "Successfully retrieved user data",'token': token,'publicKey':publicKey})
    else:
        return jsonify({'success': False, 'message': "Incorrect email or password"})

@app.route('/sign-up',methods = ['POST'])
def sign_up():
    email = request.json['email']
    password = sec.cifrarPwd(request.json['password'])
    print("password", password)
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
    print("signout")
    token = request.headers["Authorization"].split(" ")[1]
    publicKey = request.json['publicKey']

    token = sec.authorization(publicKey,token,"")

    email = database_handler.get_email(token)

    print("token resp",token)
    if email is not False:
        database_handler.remove_user_login(email)
        return jsonify({'success': True, 'message': "Successfully sign out"})
    else:
        return jsonify({'success': False, 'message': "Unsuccessfully sign out"})

@app.route('/change-password',methods = ['PUT'])
def change_password():
    token = request.headers["Authorization"].split(" ")[1]
    old_password = request.json['oldPassword']
    publicKey = request.json['publicKey']
    new_password = request.json['newPassword']
    token = sec.authorization(publicKey,token,old_password+new_password)
    result = database_handler.change_pwd(token, sec.cifrarPwd(new_password), old_password)


    if result is True:
        return jsonify({'success': True, 'message': "Successfully changed password"})
    else:
        return jsonify({'success': False, 'message': "The password is not correct"})

@app.route('/get-data/',methods = ['POST'])
def get_user_data_by_token():

    token = request.headers["Authorization"].split(" ")[1]
    email = request.json['email']
    publicKey= request.json['publicKey']
    token = sec.authorization(publicKey,token,"")
    token_valid = database_handler.check_token(token)

    print(publicKey)

    if token_valid is True: #Token is still valid
        result = database_handler.get_user_data_by_email(email)
        if result is not False: #User is registered in the database
            return jsonify({'success': True, 'message': "Successfully retrieved user data", 'data': result})
        else:
            return jsonify({'success': False, 'message': "User is not found on the database"})
    else:
        return jsonify({'success': False, 'message': "The token is not valid"})

@app.route('/get-data/email',methods = ['GET'])
def get_user_data_by_email():
    print("getuseremai")
    token = request.headers["Authorization"].split(" ")[1]
    print(variable)
    publicKey = request.values['publicKey']
    print(publicKey)
    email = request.values['email']
    print(email)
    token = sec.authorization(publicKey,token,email)
    token_valid = database_handler.check_token(token)
    if token_valid is True: #Token is still valid
        result = database_handler.get_user_data_by_email(email)
        if result is not False: #User is registered in the database
            return jsonify({'success': True, 'message': "Successfully retrieved user data", 'data': result})
        else:
            return jsonify({'success': False, 'message': "User is not found on the database"})
    else:
        return jsonify({'success': False, 'message': "The token is not valid"})

@app.route('/get-data/message/<variable>',methods = ['POST'])
def get_user_messages_by_token(variable):
    print("entra")
    token = request.headers["Authorization"].split(" ")[1]
    email_receiver = request.json['email']
    publicKey = variable
    token = sec.authorization(publicKey,token,"")
    print("token",token)
    data = database_handler.get_email(token)
    email_sender = database_handler.get_email(token)['email']
    print(email_receiver)

    if data is not False:
        result = database_handler.get_user_messages_by_email(email_receiver)
        return jsonify({'success': True, 'message': "Successfully retrieved user data", 'data': result})
    else :
        return jsonify({'success': False, 'message': "The token does not match"})

@app.route('/get-data/message/',methods = ['GET'])
def get_user_messages_by_email():
    #token = request.headers["Authorization"].split(" ")[1]
    token = request.headers["Authorization"].split(" ")[1]
    publicKey = request.values['publicKey']
    email = request.values['email']

    token = sec.authorization(publicKey,token,email)
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
    publicKey = request.json['publicKey']
    token = sec.authorization(publicKey,token,"")
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
            print("Sockets arr ", socketsArray)
            print("Force log out ", email)
            socketsArray[email].send("sign_out")
        socketsArray[email]=ws
        print("Sockets arr2 ", socketsArray)

        try:
            while True:
                email = ws.receive()
        except:
            return "oops"


if __name__ == '__main__':
    app.secret_key = '1234567890abcdefghij1234'
    http_server = WSGIServer(('',5000),app,handler_class = WebSocketHandler)
    http_server.serve_forever()
