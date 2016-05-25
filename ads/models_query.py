from .models import Ipv4AdServerInt, Ipv6AdServerInt, Ipv4AdServerStr, Ipv6AdServerStr


def get_ipv4_int_list():
    return Ipv4AdServerInt.query.with_entities(Ipv4AdServerInt.int_server_ip).all()


def get_ipv4_str_list():
    return Ipv4AdServerStr.query.with_entities(Ipv4AdServerStr.str_server_ip).all()


def get_ipv6_int_list():
    return Ipv6AdServerInt.query.with_entities(Ipv6AdServerInt.int_server_ip).all()


def get_ipv6_str_list():
    return Ipv6AdServerStr.query.with_entities(Ipv6AdServerStr.str_server_ip).all()