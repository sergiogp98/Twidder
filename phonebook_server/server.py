from flask import Flask, request, jsonify
import database_handler

app = Flask(__name__)

app.debug = True

@app.teardown_request
def after_request(exception):
    database_handler.disconnect_db()

@app.route('/contact/save', methods = ['PUT'])
def save_contact():
    data = request.get_json()
    if (len(data['name']) <= 120):
        result = database_handler.insert_contact(data['name'], data['number'])
    else:
        res = jsonify({'status' : False, 'message' : 'validation failed!'})
        return res
    if result == True:
        res = jsonify({'status' : False, 'message' : 'Contact added!'})
        return res
    else:
        res = jsonify({'status' : False, 'message' : 'Something went wrong!'})
        return res


@app.route('/contact/read/<number>', methods=['GET'])
def get_contact(number = None):
    if number != None:
        result = database_handler.read_contact(number)
        return jsonify(result)


if __name__ == '__main__':
    app.run()
