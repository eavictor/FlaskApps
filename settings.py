from flask.json import JSONEncoder


# Override JSONEncoder, eliminate space
class MiniJSONEncoder(JSONEncoder):
    item_separator = ','
    key_separator = ':'


# disable track modifications track
SQLALCHEMY_TRACK_MODIFICATIONS = False

# control jsonify pretty print
JSONIFY_PRETTYPRINT_REGULAR = False

# default database binding
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Passw0rd@localhost:3306/geoip'

# multiple database binding
SQLALCHEMY_BINDS = {
    'geoip': SQLALCHEMY_DATABASE_URI,
    'ads': 'mysql+pymysql://root:Passw0rd@localhost:3306/ads'
}

# default MySQL Global wait_timeout
SQLALCHEMY_POOL_RECYCLE = 600

SQLALCHEMY_POOL_SIZE = 20
