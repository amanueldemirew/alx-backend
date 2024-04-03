#!/usr/bin/env python3
"""
0-app
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """
    Babel config
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route("/")
def hello_world():
    """
    Render hello world html page.
    """
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run()
