import webbrowser
from threading import Timer
from functools import wraps
from flask import redirect, url_for, session

browser_opened = False


def open_browser():
    global browser_opened
    if not browser_opened:
        webbrowser.open_new("http://127.0.0.1:5000/")
        browser_opened = True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
