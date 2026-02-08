import flask
from flask import Flask, jsonify, request, Blueprint
from server.blueprints.blue import blue, style_folder
from server.api.login_api import login_api
from server.api.activity_api import activity_api
from server.api.dash_api import dash_api
from server.api.club_api import club_api

from server.database.connect import get_db_connection


# Import schema initializer
from server.database import init_or_upgrade_schema

app = Flask(__name__)

# Register blueprints
app.register_blueprint(blue)
app.register_blueprint(style_folder)
app.register_blueprint(login_api, url_prefix="/login_api")
app.register_blueprint(activity_api, url_prefix="/activity_api")
app.register_blueprint(dash_api, url_prefix="/dash_api")
app.register_blueprint(club_api, url_prefix="/club_api")


# Initialize / upgrade schema on app start
with get_db_connection() as conn:
    init_or_upgrade_schema(conn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6455, debug=True)
