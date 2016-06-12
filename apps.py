from flask import Flask
import ads  #ads/views.py >> ads/__init__.py >> here
import conoha  # conoha/views.py >> conoha/__init__.py >> here
import geoip  # geoip/views.py >> geoip/__init__.py >> here
import root  # root/views.py >> root/__init__.py >> here
import settings

# create app
app = Flask(__name__)
app.json_encoder = settings.MiniJSONEncoder
app.config.from_object(settings)

# init apps
ads.init_app(app)
conoha.init_app(app)
geoip.init_app(app)
root.init_app(app)
