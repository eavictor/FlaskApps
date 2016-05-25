from .models_query import *


def gen_commands(ip_version, country_list):
    if ip_version == 'ipv4':
        return _gen_ipv4_commands(country_list)
    elif ip_version == 'ipv6':
        return _gen_ipv6_commands(country_list)
    elif ip_version == 'both':
        return ''.join([_gen_ipv4_commands(country_list), _gen_ipv6_commands(country_list)])


def _split_country_list(country_list):
    return country_list.upper().split(',')


def _gen_ipv4_commands(country_list):
    countries = _split_country_list(country_list)
    ros_commands = []
    for country in countries:
        address_list_command = [
            '/ip firewall address-list\r\nremove [/ip firewall address-list find list=' + country + ']\r\n'
        ]
        ip_blocks = get_ipv4_cidr(country)
        for ip_block in ip_blocks:
            address_list_command.append('add address=' + ip_block[0] + ' list=' + country + '\r\n')
        ros_commands.append(''.join(address_list_command))
    return ''.join(ros_commands)


def _gen_ipv6_commands(country_list):
    countries = _split_country_list(country_list)
    ros_commands = []
    for country in countries:
        address_list_command = [
            '/ipv6 firewall address-list\r\nremove [/ipv6 firewall address-list find list=' + country + ']\r\n'
        ]
        ip_blocks = get_ipv6_cidr(country)
        for ip_block in ip_blocks:
            address_list_command.append('add address=' + ip_block[0] + ' list=' + country + '\r\n')
        ros_commands.append(''.join(address_list_command))
    return ''.join(ros_commands)
