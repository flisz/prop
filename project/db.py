__author__ = 'franksziebert@gmail.com'


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import force_auto_coercion

from project.setup.environment import ENV
from project.setup.loggers import LOGGERS
from project.lib.loaders import load_models

__all__ = ('db', 'init_db')

log = LOGGERS.Setup
# our global DB object (imported by models & views & everything else)
db = SQLAlchemy()
# support importing a functioning session query
query = db.session.query
# our global migrate object
migrate = Migrate()

DEFAULT_DATABASE_NAME = ENV.CONFIG.get('project_name')


def init_db(app=None, db=None, database_name=DEFAULT_DATABASE_NAME):
    """
    Initializes the global database object used by the app.

    Code base courtesy of:
    https://bobwaycott.com/blog/how-i-use-flask/organizing-flask-models-with-automatic-discovery/

    """
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        force_auto_coercion()
        load_models()
        database_uri = make_db_uri(database_name=database_name)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        migrate.init_app(app, db)
        log.info(f'Database: {database_name} Successfully configured.')
    else:
        raise ValueError('Cannot init DB without db and app objects.')


def make_db_uri(database_name):
    """
    Creates a uri for the database
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    password_path = basedir + '/.secrets'

    data = dict()
    if os.path.isfile(password_path):
        with open(password_path, 'r') as json_file:
            data = json.load(json_file)
            # print(f'data: {data}')
    else:
        # print('No .secrets file detected.')
        pass

    username = data.get('username', 'postgres')
    password = data.get('password')
    host = data.get('host', 'localhost')
    port = data.get('port', '5432')
    database_name = data.get('database_name', database_name)

    if password:
        userpass = '{}:{}@'.format(username, password)
    elif username:
        userpass = '{}@'.format(username)
    else:
        userpass = ''

    database_path =  f'postgresql://{userpass}{host}:{port}/{database_name}'
    # print(f'database_path: {database_path}')
    return database_path

