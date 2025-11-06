import flask
from flask import Flask, jsonify, request, register_blueprint
#from blueprints.blue import 

app = Flask(__name__)

#register_blueprint(blue)

if __name__ == '__main__':
    app.run(debug=True)@app.route('/')
