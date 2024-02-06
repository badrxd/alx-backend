#!/usr/bin/env python3
"""flask app
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict, Optional, Any, Union


class Config(object):
    """configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(i):
    """return the user based on id"""
    if i is None:
        return None
    return users.get(int(i))


@app.before_request
def before_request() -> None:
    """set user to globale variable"""
    i = request.args.get('login_as', None)
    user = get_user(i)
    g.user = user


@babel.localeselector
def get_locale() -> Optional[str]:
    """
    return best language
    """
    languages = app.config['LANGUAGES']
    lang = request.args.get('locale')
    if lang in languages:
        return lang
    return request.accept_languages.best_match(languages)


@app.route("/", strict_slashes=False)
def index() -> str:
    """
    return Hello world
    """
    return render_template('5-index.html', user=g.user)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
