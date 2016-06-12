from .models import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import urllib.request
import re
import ipaddress


def fetch_data():
    url = 'https://pgl.yoyo.org/adservers/iplist.php?ipformat=plain&showintro=0&mimetype=plaintext'
    print(datetime.now(), end='')
    print(' ads models_refresh.fetch_data(): download AdServers list from ' + url)
    response = urllib.request.urlopen(url)
    raw_text = str(response.read())
    # extract ad servers IP list from html
    text = re.search('%s(.*?)%s' % ("b'", "'"), raw_text).group(1)
    # split IP into a list
    text_list = text.split('\\n')
    # remove empty column
    while '' in text_list:
        text_list.remove('')
    # process data and insert into database
    counter = 0
    for text_ip in text_list:
        ip = ipaddress.ip_address(text_ip)
        if isinstance(ip, ipaddress.IPv4Address) and not ip.is_private:
            db.session.add(Ipv4AdServerStr(str(ip)))
            db.session.add(Ipv4AdServerInt(int(ip)))
        elif isinstance(ip, ipaddress.IPv6Address) and ip.is_global:
            db.session.add(Ipv6AdServerStr(str(ip)))
            db.session.add(Ipv6AdServerInt(int(ip)))
        counter += 1
        if counter % 100 == 0:
            db.session.commit()
            print(datetime.now(), end='')
            print(' ads models_refresh.fetch_data(): insert data into database ', end='')
            print(counter)
    db.session.commit()
    print(datetime.now(), end='')
    print(' ads models_refresh.fetch_data(): insert data into database ', end='')
    print(counter)


def has_data():
    try:
        ipv4_int = Ipv4AdServerInt.query.count() > 0
        ipv4_str = Ipv4AdServerStr.query.count() > 0
        # ipv6_int = Ipv6AdServerInt.query.count() > 0
        # ipv6_str = Ipv6AdServerStr.query.count() > 0
        if ipv4_int and ipv4_str:  # currently no IPv6 Ad Server found
            print('ads models_refresh.has_data(): return True (has data)')
            return True
        else:
            print('ads models_refresh.has_data(): return False (no data)')
            return False
    except SQLAlchemyError:
        print('ads models_refresh.has_data(): return False (SQLAlchemyError)')
        return False
