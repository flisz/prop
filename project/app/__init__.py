from os.path import abspath, isfile, join
from flask import Flask

from project.setup.environment import ENV
from project.setup.loggers import LOGGERS
from project.app.csrf import csrf
from project.db import db, init_db
from project.views import init_views


log = LOGGERS.Setup


def create_app(config_file=None):
    """Default application factory.

    Default usage:
        app = create_app()

    Usage with config file:
        app = create_app('/path/to/config.yml')

    If config_file is not provided, will look for default
    config expected at '<proj_root>/config/config.yml'.
    Returns Flask app object.
    Raises EnvironmentError if config_file cannot be found.
    """
    if config_file is None:
        config_file = join(ENV.ROOT, 'config.yaml')  # os.path.join()
    else:
        config_file = abspath(config_file)

    # raise error if config_file doesn't exist
    if not isfile(config_file):
        raise EnvironmentError('App config file does not exist at %s' % config_file)
    log.info(f"Using config_file: {config_file}")

    # start app setup
    app = Flask(__name__)
    set_app_mode(app)

    # setup csrf
    csrf.init_app(app)

    # setup db
    init_db(app, db)

    # register views
    init_views(app)
    return app


def set_app_mode(app):
    # set some helpful attrs to greatly simplify state checks
    cfg = app.config
    app.env = cfg.get('ENVIRONMENT', 'development')
    if app.debug:
        app.live = False
        if app.env == 'test':
            app.testing = True
        elif app.env == 'development':
            app.dev = True
        else:
            raise EnvironmentError('Invalid environment for app state.')
    else:
        if app.env == 'production':
            app.live = True
        elif app.env == 'development':
            # dev.proj runs in development with debug off
            app.live = False
            app.testing = False
        else:
            raise EnvironmentError('Invalid environment for app state.')
