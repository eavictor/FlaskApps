from .models_query import get_ipv4_int_list, get_ipv4_str_list, get_ipv6_int_list, get_ipv6_str_list


def ad_server_list(ip_version, ip_format):
    if ip_format == 'str':
        return _str_ad_server_list(ip_version)
    elif ip_format == 'int':
        return _int_ad_server_list(ip_version)


def _str_ad_server_list(ip_version):
    if ip_version == 'ipv4':
        ipv4_raw_list = get_ipv4_str_list()
        ipv4_list = []
        for ipv4 in ipv4_raw_list:
            ipv4_list.append(ipv4[0])
        return {'ad_servers': {'ipv4': ipv4_list}}
    elif ip_version == 'ipv6':
        ipv6_raw_list = get_ipv6_str_list()
        ipv6_list = []
        for ipv6 in ipv6_raw_list:
            ipv6_list.append(ipv6[0])
        return {'ad_servers': {'ipv6': ipv6_list}}
    elif ip_version == 'both':
        ipv4_raw_list = get_ipv4_str_list()
        ipv6_raw_list = get_ipv6_str_list()
        ipv4_list = []
        ipv6_list = []
        for ipv4 in ipv4_raw_list:
            ipv4_list.append(ipv4[0])
        for ipv6 in ipv6_raw_list:
            ipv6_list.append(ipv6[0])
        return {'ad_servers': {'ipv4': ipv4_list, 'ipv6': ipv6_list}}


def _int_ad_server_list(ip_version):
    if ip_version == 'ipv4':
        ipv4_raw_list = get_ipv4_int_list()
        ipv4_list = []
        for ipv4 in ipv4_raw_list:
            ipv4_list.append(int(ipv4[0]))
        return {'ad_servers': {'ipv4': ipv4_list}}
    elif ip_version == 'ipv6':
        ipv6_raw_list = get_ipv6_int_list()
        ipv6_list = []
        for ipv6 in ipv6_raw_list:
            ipv6_list.append(int(ipv6[0]))
        return {'ad_servers': {'ipv6': ipv6_list}}
    elif ip_version == 'both':
        ipv4_raw_list = get_ipv4_int_list()
        ipv6_raw_list = get_ipv6_int_list()
        ipv4_list = []
        ipv6_list = []
        for ipv4 in ipv4_raw_list:
            ipv4_list.append(int(ipv4[0]))
        for ipv6 in ipv6_raw_list:
            ipv6_list.append(int(ipv6[0]))
        return {'ad_servers': {'ipv4': ipv4_list, 'ipv6': ipv6_list}}
