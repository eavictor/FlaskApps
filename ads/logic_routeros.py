from .models_query import get_ipv4_str_list, get_ipv6_str_list


def gen_commands(ip_version):
    if ip_version == 'ipv4':
        return _gen_ipv4_command()
    elif ip_version == 'ipv6':
        return _gen_ipv6_command()
    elif ip_version == 'both':
        return ''.join([_gen_ipv4_command(), _gen_ipv6_command()])


def _gen_ipv4_command():
    ipv4_list = get_ipv4_str_list()
    ros_command = [
        '/ip firewall address-list\r\nremove [/ip firewall address-list find list=AdServer]\r\n'
    ]
    for ipv4 in ipv4_list:
        ros_command.append('add address=' + ipv4[0] + ' list=AdServer\r\n')
    return ''.join(ros_command)


def _gen_ipv6_command():
    ipv6_list = get_ipv6_str_list()
    ros_command = [
        '/ipv6 firewall address-list\r\nremove [/ipv6 firewall address-list find list=AdServer]\r\n'
    ]
    for ipv6 in ipv6_list:
        ros_command.append('add address=' + ipv6[0] + ' list=AdServer\r\n')
    return ''.join(ros_command)
