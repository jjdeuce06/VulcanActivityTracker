from flask import Flask, request, jsonify, Blueprint, redirect, url_for
dashboard_api = Blueprint('dashboard_api', __name__)

@dashboard_api.route('/dashboard_api', methods=['GET'])
def dashboard():
    redirect(url_for("blue.dashboard_page"))
    return jsonify({"message": "Login successful"}), 200