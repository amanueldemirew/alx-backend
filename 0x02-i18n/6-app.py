#!/usr/bin/env python3
"""
A Basic flask Application
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Application configuration class
    """
    LANGUAGES = ["en", "fr", "am"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Instantiate the application object
app = Flask(__name__)
app.config.from_object(Config)


# Wrap the application with Babel
babel = Babel(app)


def get_user(user_id):
    """
    Get user by user_id
    """
    return users.get(user_id)


@app.before_request
def before_request():
    """
    Adds valid user to the global session `g`.
    """
    user_id = request.args.get('login_as')

    if user_id:
        g.user = get_user(int(user_id))
    else:
        g.user = None


@babel.localeselector
def get_locale():
    """
    Returns best match locale language.
    """
    locale = request.args.get('locale')
    user = g.user
    header_locale = request.headers.get('Accept-Language')

    if locale and locale in app.config['LANGUAGES']:
        return locale

    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']

    if header_locale and header_locale in app.config['LANGUAGES']:
        return header_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def hello_world():
    """
    Render a basic html page.
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run()
