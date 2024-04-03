#!/usr/bin/env python3
"""
0-app
"""
from flask import Flask, render_template, request
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


@babel.localeselector
def get_locale():
    """
    Returns best match locale language.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def hello_world():
    """
    Render hello world html page.
    """
    greeting = "Hello, World!"
    return render_template('2-index.html', greeting=greeting)


if __name__ == "__main__":
    app.run()
