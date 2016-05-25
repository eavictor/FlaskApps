from sqlalchemy.orm import sessionmaker
from .models import *


Session = sessionmaker()
Session.configure(bind=db)


def get_ipv4_cidr(country):
    return Ipv4ClasslessInterDomainRouting.query.with_entities(
        Ipv4ClasslessInterDomainRouting.ip_block
    ).filter_by(
        country=country
    ).all()


def get_ipv6_cidr(country):
    return Ipv6ClasslessInterDomainRouting.query.with_entities(
        Ipv6ClasslessInterDomainRouting.ip_block
    ).filter_by(
        country=country
    ).all()


def get_ipv4_str_range(country):
    return Ipv4StrRange.query.with_entities(
        Ipv4StrRange.ip_start,
        Ipv4StrRange.ip_end
    ).filter_by(
        country=country
    ).all()


def get_ipv6_str_range(country):
    return Ipv6StrRange.query.with_entities(
        Ipv6StrRange.ip_start,
        Ipv6StrRange.ip_end
    ).filter_by(
        country=country
    ).all()


def get_ipv4_int_range(country):
    return Ipv4IntRange.query.with_entities(
        Ipv4IntRange.ip_start,
        Ipv4IntRange.ip_end
    ).filter_by(
        country=country
    ).all()


def get_ipv6_int_range(country):
    return Ipv6IntRange.query.with_entities(
        Ipv6IntRange.ip_start,
        Ipv6IntRange.ip_end
    ).filter_by(
        country=country
    ).all()


def get_ipv4_which_country(int_ip_addr):
    return Ipv4IntRange.query.with_entities(
        Ipv4IntRange.country
    ).filter(
        Ipv4IntRange.ip_start <= int_ip_addr,
        Ipv4IntRange.ip_end >= int_ip_addr
    ).first()


def get_ipv6_which_country(int_ip_addr):
    return Ipv6IntRange.query.with_entities(
        Ipv6IntRange.country
    ).filter(
        Ipv6IntRange.ip_start <= int_ip_addr,
        Ipv6IntRange.ip_end >= int_ip_addr
    ).first()
