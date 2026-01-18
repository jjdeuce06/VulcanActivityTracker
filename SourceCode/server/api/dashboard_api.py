from flask import Flask, request, jsonify, Blueprint, redirect, url_for
dashboard_api = Blueprint('dashboard_api', __name__)



# API for moving dashboard data from front end to back end
# render pages in the blue.py folder, by adding a html file to Routes
