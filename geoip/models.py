from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, OperationalError


db = SQLAlchemy()


class Ipv4ClasslessInterDomainRouting(db.Model):
    __bind_key__ = 'geoip'

    ip_block = db.Column(db.String(18), primary_key=True)
    country = db.Column(db.String(2), index=True)

    def __init__(self, ip_block, country):
        self.ip_block = ip_block
        self.country = country

    def __repr__(self):
        return "<IPv4ClasslessInterDomainRouting(ip_block='%s', country='%s')>" % (self.ip_block, self.country)


class Ipv6ClasslessInterDomainRouting(db.Model):
    __bind_key__ = 'geoip'

    ip_block = db.Column(db.String(43), primary_key=True)
    country = db.Column(db.String(2), index=True)

    def __init__(self, ip_block, country):
        self.ip_block = ip_block
        self.country = country

    def __repr__(self):
        return "<IPv6ClasslessInterDomainRouting(ip_block='%s', country='%s')>" % (self.ip_block, self.country)


class Ipv4StrRange(db.Model):
    __bind_key__ = 'geoip'

    ip_start = db.Column(db.String(15), primary_key=True)
    ip_end = db.Column(db.String(15))
    country = db.Column(db.String(2), index=True)

    def __init__(self, ip_start, ip_end, country):
        self.ip_start = ip_start
        self.ip_end = ip_end
        self.country = country

    def __repr__(self):
        return "<IPv4StrRange(ip_start='%s', ip_end='%s', country='%s')>" % (self.ip_start, self.ip_end, self.country)


class Ipv6StrRange(db.Model):
    __bind_key__ = 'geoip'

    ip_start = db.Column(db.String(39), primary_key=True)
    ip_end = db.Column(db.String(39))
    country = db.Column(db.String(2), index=True)

    def __init__(self, ip_start, ip_end, country):
        self.ip_start = ip_start
        self.ip_end = ip_end
        self.country = country

    def __repr__(self):
        return "<IPv6StrRange(ip_start='%s', ip_end='%s', country='%s')>" % (self.ip_start, self.ip_end, self.country)


class Ipv4IntRange(db.Model):
    __bind_key__ = 'geoip'

    ip_start = db.Column(db.Numeric(10, 0), primary_key=True)
    ip_end = db.Column(db.Numeric(10, 0))
    country = db.Column(db.String(2), index=True)

    def __init__(self, ip_start, ip_end, country):
        self.ip_start = ip_start
        self.ip_end = ip_end
        self.country = country

    def __repr__(self):
        return "<IPv4IntRange(ip_start='%s', ip_end='%s', country='%s')>" % (self.ip_start, self.ip_end, self.country)


class Ipv6IntRange(db.Model):
    __bind_key__ = 'geoip'

    ip_start = db.Column(db.Numeric(39, 0), primary_key=True)
    ip_end = db.Column(db.Numeric(39, 0))
    country = db.Column(db.String(2), index=True)

    def __init__(self, ip_start, ip_end, country):
        self.ip_start = ip_start
        self.ip_end = ip_end
        self.country = country

    def __repr__(self):
        return "<IPv6IntRange(ip_start='%s', ip_end='%s', country='%s')>" % (self.ip_start, self.ip_end, self.country)


def create_all_tables():
    try:
        db.create_all(bind='geoip')
        db.session.commit()
    except SQLAlchemyError or OperationalError:
        db.session.rollback()


def drop_all_tables():
    try:
        db.reflect(bind='geoip')
        db.drop_all(bind='geoip')
        db.session.commit()
    except SQLAlchemyError or OperationalError:
        db.session.rollback()


if __name__ == '__main__':
    drop_all_tables()
    create_all_tables()
