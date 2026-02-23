from flask import Blueprint, jsonify, render_template
import os

#hold blueprints
#template 
blue = Blueprint('blue', __name__)


#Folder Blueprint
style_folder = Blueprint('style_folder', __name__,
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "templates", "style") ),static_url_path='/style'
)
ROUTES = {
    "/": ("base_temp/welcome.html", None),
    "/login": ("pages/login.html", None),
    "/createacc": ("pages/createacc.html", None),
    "/dashboard": ("base_temp/dashboard.html", "dashboard"),
    "/training": ("pages/dash/training.html", "training"),
    "/clubs": ("pages/dash/clubs.html", "clubs"),
    "/teams": ("pages/dash/teams.html", "teams"),
    "/maps": ("pages/dash/maps.html", "maps"),
    "/leaderboard": ("pages/dash/leaderboard.html", "leaderboard"),
    "/challenges": ("pages/dash/challenges.html", "challenges"),
}  

def make_view(tpl, active_page):
    def view():
        return render_template(tpl, active_page=active_page)
    return view

for rule, (tpl, active_page) in ROUTES.items():
    endpoint = f"page_{tpl.replace('/', '_').replace('.', '_')}"
    blue.add_url_rule(rule, endpoint, make_view(tpl, active_page))

#Adds the dynamic route for the club details page
@blue.route('/club/<club_id>')
def club_detail(club_id):
    return render_template('pages/dash/club_details.html', active_page='clubs')
