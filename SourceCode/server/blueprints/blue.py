from flask import Blueprint, jsonify, render_template
import os

#hold blueprints
#template 
blue = Blueprint('blue', __name__)
style_folder = Blueprint('style_folder', __name__,
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "templates", "style") ),static_url_path='/style'
)
ROUTES = {"/": "base_temp/welcome.html",
          "/login": "pages/login.html",
        }   

def make_view(tpl):
    def view():
        return render_template(tpl)
    return view

for rule, tpl in ROUTES.items():
    endpoint = f"page_{tpl.replace('/', '_').replace('.', '_')}"
    blue.add_url_rule(rule, endpoint, make_view(tpl))
