from .views import root


def init_app(app):
    app.register_blueprint(root, url_prefix='/')