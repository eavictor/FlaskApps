from .views import conoha


def init_app(app):
    app.register_blueprint(conoha, url_prefix='/conoha')