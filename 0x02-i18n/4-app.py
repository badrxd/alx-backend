#!/usr/bin/env python3
"""flask app
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
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
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)