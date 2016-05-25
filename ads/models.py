from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, OperationalError

db = SQLAlchemy()


class Ipv4AdServerStr(db.Model):
    __bind_key__ = 'ads'

    str_server_ip = db.Column(db.String(18), primary_key=True)

    def __init__(self, str_server_ip):
        self.str_server_ip = str_server_ip

    def __repr__(self):
        return "<Ipv4AdServerStr(str_server_ip='%s')>" % self.str_server_ip


class Ipv6AdServerStr(db.Model):
    __bind_key__ = 'ads'

    str_server_ip = db.Column(db.String(39), primary_key=True)

    def __init__(self, str_server_ip):
        self.str_server_ip = str_server_ip

    def __repr__(self):
        return "<Ipv6AdServerStr(str_server_ip='%s')>" % self.str_server_ip


class Ipv4AdServerInt(db.Model):
    __bind_key__ = 'ads'

    int_server_ip = db.Column(db.Numeric(10, 0), primary_key=True)

    def __init__(self, int_server_ip):
        self.int_server_ip = int_server_ip

    def __repr__(self):
        return "<Ipv4AdServerInt(int_server_ip='%s')>" % self.int_server_ip


class Ipv6AdServerInt(db.Model):
    __bind_key__ = 'ads'

    int_server_ip = db.Column(db.Numeric(39, 0), primary_key=True)

    def __init__(self, int_server_ip):
        self.int_server_ip = int_server_ip

    def __repr__(self):
        return "<Ipv6AdServerInt(int_server_ip='%s')>" % self.int_server_ip


def create_all_tables():
    try:
        db.create_all(bind='ads')
        db.session.commit()
    except SQLAlchemyError or OperationalError:
        db.session.rollback()


def drop_all_tables():
    try:
        db.reflect(bind='ads')
        db.drop_all(bind='ads')
        db.session.commit()
    except SQLAlchemyError or OperationalError:
        db.session.rollback()


if __name__ == '__main__':
    create_all_tables()
    drop_all_tables()