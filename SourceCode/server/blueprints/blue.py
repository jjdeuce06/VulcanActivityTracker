from flask import Blueprint, jsonify, render_template
import os
from server.api.protectRoutes import login_required

# ---------------- MAIN TEMPLATE BLUEPRINT ----------------
# Handles all page routing for templates
blue = Blueprint('blue', __name__)


# ---------------- STATIC FILES BLUEPRINT ----------------
# Serves static CSS/JS files from templates/style directory
style_folder = Blueprint(
    'style_folder',
    __name__,
    static_folder=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "templates", "style")
    ),
    static_url_path='/style'
)


# ---------------- ROUTE MAPPING ----------------
# Maps URL paths → template files + active page indicator
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
    "/resetpassword": ("pages/reset_password.html", None),
    "/resetpassword": ("pages/reset_password.html", None),
    "/settings": ("pages/dash/settings.html", "settings"),
    "/inbox": ("pages/dash/inbox.html", "inbox")
}  


# ---------------- VIEW GENERATOR ----------------
# Dynamically creates a view function for each route
def make_view(tpl, active_page):

    def view():
        # Render template with active_page context (used for nav highlighting)
        return render_template(tpl, active_page=active_page)
    
    # Protect routes that require login
    if active_page is not None:
        return login_required(view)

    return view


# ---------------- REGISTER ROUTES ----------------
# Loop through ROUTES dict and register each route dynamically
for rule, (tpl, active_page) in ROUTES.items():
    # Generate unique endpoint name
    endpoint = f"page_{tpl.replace('/', '_').replace('.', '_')}"

    # Register route with Flask
    blue.add_url_rule(rule, endpoint, make_view(tpl, active_page))


# ---------------- CLUB DETAIL PAGE ----------------
# Dynamic route for viewing a specific club
@blue.route('/club/<club_name>')
def club_detail(club_name):
    return render_template('pages/dash/club_details.html', active_page='clubs')


# ---------------- CREATE CLUB PAGE ----------------
@blue.route('/create_club')
def create_club():
    return render_template('pages/dash/club_create.html', active_page='clubs')


# ---------------- CHALLENGE DETAIL PAGE ----------------
@blue.route('/challenge/<challenge_name>')
def challenge_detail(challenge_name):
    return render_template('pages/dash/challenge_details.html', active_page='challenges')


# ---------------- TEAM DETAIL PAGE ----------------
@blue.route('/teams/<team_id>')
def team_detail(team_id):
    return render_template('pages/dash/team_detail.html', active_page='teams')


# ---------------- CREATE CHALLENGE PAGE ----------------
@blue.route('/create_challenge')
def create_challenge():
    return render_template('pages/dash/challenge_create.html', active_page='challenges')