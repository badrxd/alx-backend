#!/usr/bin/env python3
"""flask app
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict, Optional, Any, Union
import pytz


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

    loc_lang = request.args.get('locale')
    if loc_lang in languages:
        return loc_lang

    if g.user:
        if g.user.get('locale') in languages:
            return g.user.get('locale')

    all_lang = request.headers.get('Accept-Language', None)
    if all_lang:
        lang_list = [entry.split(';')[0].strip()
                     for entry in all_lang.split(',')]
        for lang in lang_list:
            if lang in languages:
                return lang

    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    time_zone = request.args.get('timezone')

    if time_zone:
        try:
            return pytz.timezone(time_zone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user:
        try:
            return pytz.timezone(g.user.get('timezone')).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route("/", strict_slashes=False)
def index() -> str:
    """
    return Hello world
    """
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
