from flask import Blueprint, render_template


root = Blueprint('root', __name__, template_folder='templates', static_folder='static', static_url_path='root/static')


@root.route('/')
def index():
    return render_template("root/index.html")