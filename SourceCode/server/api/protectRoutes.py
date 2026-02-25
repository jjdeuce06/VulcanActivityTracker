from functools import wraps
from flask import session, redirect, url_for

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("blue.page_pages_login_html"))
        return view_func(*args, **kwargs)
    return wrapper