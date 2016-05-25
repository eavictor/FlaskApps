from .models_query import *
import ipaddress


def ip_lists(ip_version, ip_format, countries):
    if ip_format == 'cidr':
        return _ip_cidr(ip_version, countries)
    elif ip_format == 'int_range':
        return _ip_int_range(ip_version, countries)
    elif ip_format == 'str_range':
        return _ip_str_range(ip_version, countries)


def which_country(request_ips):
    which_country_list = []
    for ip_addr in request_ips:
        ip = ipaddress.ip_address(ip_addr)
        if isinstance(ip, ipaddress.IPv6Address):
            which_country_list.append(
                {'requested_ip': ip_addr, 'country': get_ipv6_which_country(int(ip))[0], 'ip_version': 'ipv6'})
        elif isinstance(ip, ipaddress.IPv4Address):
            which_country_list.append(
                {'requested_ip': ip_addr, 'country': get_ipv4_which_country(int(ip))[0], 'ip_version': 'ipv4'})
        else:
            which_country_list.append(
                {'requested_ip': ip_addr, 'country': 'not_found', 'ip_version': 'not_found'})
    return {'answer': which_country_list, 'data_provider': 'ip-db.com'}


def _ip_cidr(ip_version, countries):
    json_dict = {}
    for country in countries:
        if ip_version == 'ipv4':
            ipv4_cidr_list = []
            for cidr in get_ipv4_cidr(country):
                ipv4_cidr_list.append(cidr[0])
            ip_dict = {'ipv4': ipv4_cidr_list}
            json_dict[country] = ip_dict
        elif ip_version == 'ipv6':
            ipv6_cidr_list = []
            for cidr in get_ipv6_cidr(country):
                ipv6_cidr_list.append(cidr[0])
            ip_dict = {'ipv6': ipv6_cidr_list}
            json_dict[country] = ip_dict
        elif ip_version == 'both':
            ip_dict = {}
            ipv4_cidr_list = []
            for cidr in get_ipv4_cidr(country):
                ipv4_cidr_list.append(cidr[0])
            ip_dict['ipv4'] = ipv4_cidr_list
            ipv6_cidr_list = []
            for cidr in get_ipv6_cidr(country):
                ipv6_cidr_list.append(cidr[0])
            ip_dict['ipv6'] = ipv6_cidr_list
            json_dict[country] = ip_dict
    # data provider
    json_dict['data_provider'] = 'db-ip.com'
    return json_dict


def _ip_str_range(ip_version, countries):
    json_dict = {}
    for country in countries:
        if ip_version == 'ipv4':
            ipv4_list = []
            for row in get_ipv4_str_range(country):
                one_dict = {'ip_start': row[0], 'ip_end': row[1]}
                ipv4_list.append(one_dict)
            ipv4_dict = {'ipv4': ipv4_list}
            json_dict[country] = ipv4_dict
        elif ip_version == 'ipv6':
            ipv6_list = []
            for row in get_ipv6_str_range(country):
                one_dict = {'ip_start': row[0], 'ip_end': row[1]}
                ipv6_list.append(one_dict)
            ipv6_dict = {'ipv6': ipv6_list}
            json_dict[country] = ipv6_dict
        elif ip_version == 'both':
            ipv4_list = []
            ipv6_list = []
            for row in get_ipv4_str_range(country):
                one_dict = {'ip_start': row[0], 'ip_end': row[1]}
                ipv4_list.append(one_dict)
            for row in get_ipv6_str_range(country):
                one_dict = {'ip_start': row[0], 'ip_end': row[1]}
                ipv6_list.append(one_dict)
            ipv4_dict = {'ipv4': ipv4_list}
            ipv6_dict = {'ipv6': ipv6_list}
            json_dict[country] = ipv4_dict, ipv6_dict
    # data provider
    json_dict['data_provider'] = 'db-ip.com'
    return json_dict


def _ip_int_range(ip_version, countries):
    json_dict = {}
    for country in countries:
        if ip_version == 'ipv4':
            ipv4_list = []
            for row in get_ipv4_int_range(country):
                one_dict = {'ip_start': int(row[0]), 'ip_end': int(row[1])}
                ipv4_list.append(one_dict)
            ipv4_dict = {'ipv4': ipv4_list}
            json_dict[country] = ipv4_dict
        elif ip_version == 'ipv6':
            ipv6_list = []
            for row in get_ipv6_int_range(country):
                one_dict = {'ip_start': int(row[0]), 'ip_end': int(row[1])}
                ipv6_list.append(one_dict)
            ipv6_dict = {'ipv6': ipv6_list}
            json_dict[country] = ipv6_dict
        elif ip_version == 'both':
            ipv4_list = []
            ipv6_list = []
            for row in get_ipv4_int_range(country):
                one_dict = {'ip_start': int(row[0]), 'ip_end': int(row[1])}
                ipv4_list.append(one_dict)
            for row in get_ipv6_int_range(country):
                one_dict = {'ip_start': int(row[0]), 'ip_end': int(row[1])}
                ipv6_list.append(one_dict)
            ipv4_dict = {'ipv4': ipv4_list}
            ipv6_dict = {'ipv6': ipv6_list}
            json_dict[country] = ipv4_dict, ipv6_dict
    # data provider
    json_dict['data_provider'] = 'db-ip.com'
    return json_dict
