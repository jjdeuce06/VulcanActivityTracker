from flask import Blueprint, jsonify, render_template
import os

#hold blueprints
#template 
blue = Blueprint('blue', __name__)


#Folder Blueprint
style_folder = Blueprint('style_folder', __name__,
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "templates", "style") ),static_url_path='/style'
)
ROUTES = {"/": "base_temp/welcome.html",
          "/login": "pages/login.html",
          "/createacc": "pages/createacc.html",
          "/dashboard": "base_temp/dashboard.html",
          "/training": "pages/dash/training.html",
          "/clubs": "pages/dash/clubs.html",
          "/teams": "pages/dash/teams.html",
          "/maps": "pages/dash/maps.html",
          "/leaderboard": "pages/dash/leaderboard.html"
        }   

def make_view(tpl):
    def view():
        return render_template(tpl)
    return view

for rule, tpl in ROUTES.items():
    endpoint = f"page_{tpl.replace('/', '_').replace('.', '_')}"
    blue.add_url_rule(rule, endpoint, make_view(tpl))
