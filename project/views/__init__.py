
from flask import render_template
from project.lib.loaders import get_views


def init_views(app=None):
    """Initializes application views."""
    if app is None:
        raise ValueError('cannot init views without app object')

    # register defined views
    for view in get_views():
        view.register(app)

    # Handle HTTP errors
    register_error_handlers(app)


def register_error_handlers(app=None):
    """Register app error handlers.

    Raises error if app is not provided.
    """
    if app is None:
        raise ValueError('cannot register error handlers on an empty app')

    @app.errorhandler(404)
    def error404(self):
        return render_template('errors/404.html', title='Page Not Found')

    @app.errorhandler(500)
    def error500(self):
        return render_template('errors/500.html', title='Server Error')