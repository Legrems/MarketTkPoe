# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from flask import Flask, render_template_string, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "PoeApi.trade"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form

""" Flask application factory """

# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)


# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

# Create all database tables
db.create_all()

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

BASE_CONTENT = {
    'user_activate': False,
    'alerts': [
        {'date': '30 August 2019', 'url': '#', 'fas_icon': 'fa-exclamation-triangle', 'text': 'Site still under construction, more feature will come asap !'},
    ],
    'messages': [
        {}
    ],
    'categories': [
        'Currency',
        'Fragments',
        'Incubators',
        'Scarabs',
        'Fossils',
        'Resonators',
        'Essences',
        'Divination Cards',
        'Prophecies',
        'Skill Gems',
        'Base Types',
        'Helmet Enchant',
        'Unique Maps',
        'Maps',
        'Unique Jewels',
        'Unique  Flasks',
        'Unique Weapons',
        'Unique Armours',
        'Unique Accessories',
        'Beasts'
    ],
    'search_analyse': [
        'Search', 'Analyse'
    ],
}

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    context = BASE_CONTENT
    context.update({
        'custom': {
            'actions': [
                {'name': '1', 'text': 'some little text', 'url': '', 'priority': 0},
                {'name': '2', 'text': 'some little text', 'url': '', 'priority': 1},
                {'name': '3', 'text': 'some little text', 'url': '', 'priority': 2},
                {'name': '4', 'text': 'some little text', 'url': '', 'priority': 3},
                {'name': '5', 'text': 'some little text', 'url': '', 'priority': 4},
                {'name': '6', 'text': 'some little text', 'url': '', 'priority': 5},
            ],
        },
        'projects': [
            {'name': 'Users account', 'done': 0},
            {'name': 'Database storage', 'done': 0},
            {'name': 'Search for item', 'done': 0},
            {'name': 'Customization', 'done': 0},
            {'name': 'Currency graph list', 'done': 0},
            {'name': 'API', 'done': 10},
        ],
    })
    return render_template('theme/index.html', context=context)


@app.route('/stats/<string:name>')
def stats(name):

    return render_template('theme/page.html', context=BASE_CONTENT)


@app.route('/Search')
def search():

    return render_template('theme/search.html', context=BASE_CONTENT)


@app.route('/Analyse')
def analyse():

    return render_template('theme/analyse.html', context=BASE_CONTENT)


# Start development web server
if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
