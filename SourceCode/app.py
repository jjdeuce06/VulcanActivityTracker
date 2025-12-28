import flask
from flask import Flask, jsonify, request, Blueprint
from server.blueprints.blue import blue, style_folder
from server.api.login_api import login_api

import pyodbc

# Import schema initializer
from server.database import init_or_upgrade_schema

app = Flask(__name__)

# Register blueprints
app.register_blueprint(blue)
app.register_blueprint(style_folder)
app.register_blueprint(login_api, url_prefix="/login_api")

def get_db_connection():
    # Create the database connection
    return pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=mssql_server,1433;"  
    "DATABASE=master;"         
    "UID=sa;"
    "PWD=VulcanP@ssw0rd!;"
    "TrustServerCertificate=yes"
)


# Initialize / upgrade schema on app start
with get_db_connection() as conn:
    init_or_upgrade_schema(conn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6455, debug=True)
