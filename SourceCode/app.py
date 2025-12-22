import flask
from flask import Flask, jsonify, request, Blueprint
from server.blueprints.blue import blue, style_folder
from server.api.login_api import login_api

app = Flask(__name__)

app.register_blueprint(blue)
app.register_blueprint(style_folder)
app.register_blueprint(login_api, url_prefix="/login_api")

if __name__ == '__main__':
    app.run(debug=True)
