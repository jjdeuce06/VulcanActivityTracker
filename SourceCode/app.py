import flask
from flask import Flask, jsonify, request, Blueprint
from server.blueprints.blue import blue, style_folder

app = Flask(__name__)

app.register_blueprint(blue)
app.register_blueprint(style_folder)

if __name__ == '__main__':
    app.run(debug=True)
