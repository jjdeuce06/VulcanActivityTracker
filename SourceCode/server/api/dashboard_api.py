from flask import Flask, request, jsonify, Blueprint
dashboard_api = Blueprint('dashboard_api', __name__)

@dashboard_api.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template("dashboard.html")