from functools import wraps
from flask import session, redirect, url_for

# ---------------- LOGIN REQUIRED DECORATOR ----------------
# This decorator protects routes so only logged-in users can access them
def login_required(view_func):

    # Preserve original function metadata (name, docstring, etc.)
    @wraps(view_func)
    def wrapper(*args, **kwargs):

        # Check if user is logged in by looking for "username" in session
        if "username" not in session:

            # If not logged in, redirect to login page
            return redirect(url_for("blue.page_pages_login_html"))

        # If logged in, allow access to the original view function
        return view_func(*args, **kwargs)

    return wrapper