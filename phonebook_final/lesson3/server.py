from flask import Flask, request, jsonify, send_from_directory
import database_handler

app = Flask(__name__)

app.debug = True

@app.teardown_request
def after_request(exception):
    database_handler.disconnect_db()


'''this is for demonstration how sending static files work in flask.
In your case you shall need to send ONLY one big html file to the client.
====================================================================
'''

@app.route('/')
@app.route('/save')
def save_page():
    return send_from_directory('static','index.html')

@app.route('/find')
def find_page():
    return send_from_directory('static','findcontact.html')

'''================================================================'''

@app.route('/contact/save', methods = ['PUT'])
def save_contact():
    data = request.get_json()
    if (len(data['name']) <= 120):
        result = database_handler.insert_contact(data['name'], data['number'])
    else:
        res = jsonify({'status' : False, 'message' : 'validation failed!'})
        return res
    if result == True:
        res = jsonify({'status' : True, 'message' : 'Contact added!'})
        return res
    else:
        res = jsonify({'status' : False, 'message' : 'Something went wrong!'})
        return res

#It is important that the returned output has a structure like save_contact()
@app.route('/contact/read/<number>', methods=['GET'])
def get_contact(number = None):
    if number != None:
        result = database_handler.read_contact(number)
        return jsonify(result)

#added code to lesson two.
#It is important that the returned output has a structure like save_contact()
@app.route('/contact/readbyname/<name>', methods=['GET'])
def get_contact_by_name(name = None):
    if name != None:
        result = database_handler.read_contact_by_name(name)
        return jsonify(result)

if __name__ == '__main__':
    app.run()
