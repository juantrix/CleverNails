import webbrowser
from threading import Timer

browser_opened = False


def open_browser():
    global browser_opened
    if not browser_opened:
        webbrowser.open_new("http://127.0.0.1:5000/")
        browser_opened = True
