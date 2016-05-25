from datetime import datetime
from .models import *
from sqlalchemy.exc import SQLAlchemyError
import gzip
import csv
import os
import ipaddress
import urllib.request


def download_csv():
    """
    1. generate URL to download GZIP
    2. download GZIP from db-ip.com
    3. unzip GZIP
    4. write CSV to current folder(this geoip package in project)
    """
    current_month = datetime.now().strftime("%m").zfill(2)
    current_year = datetime.now().strftime("%Y")
    filename = 'dbip-country-' + current_year + '-' + current_month + '.csv.gz'
    url = 'http://download.db-ip.com/free/' + filename
    print(datetime.now(), end='')
    print('geoip models_refresh.download_csv(): download csv from ' + url)
    response = urllib.request.urlopen(url)
    with open('dbip-country.csv', 'wb') as outfile:
        outfile.write(gzip.decompress(response.read()))
        outfile.close()


def read_csv_and_update_database():
    """
    1. read CSV in text mode
    2. process all data
    3. write converted data into database
    """
    print(datetime, end='')
    print(' geoip models_refresh.read_csv_and_update_database(): processing data')
    with open('dbip-country.csv', 'rt') as csv_file:
        csv_obj = csv.reader(csv_file, delimiter=',', quotechar='"')
        counter = 0  # counter
        for row in csv_obj:
            ip_start = ipaddress.ip_address(row[0])
            ip_end = ipaddress.ip_address(row[1])
            # country = row[2]
            if ':' in row[0]:
                db.session.add(Ipv6StrRange(row[0], row[1], row[2]))
                db.session.add(Ipv6IntRange(int(ip_start), int(ip_end), row[2]))
                ip_blocks = ipaddress.summarize_address_range(ip_start, ip_end)
                for ip_block in ip_blocks:
                    db.session.add(Ipv6ClasslessInterDomainRouting(ip_block, row[2]))
            elif'.' in row[0]:
                db.session.add(Ipv4StrRange(row[0], row[1], row[2]))
                db.session.add(Ipv4IntRange(int(ip_start), int(ip_end), row[2]))
                ip_blocks = ipaddress.summarize_address_range(ip_start, ip_end)
                for ip_block in ip_blocks:
                    db.session.add(Ipv4ClasslessInterDomainRouting(str(ip_block), row[2]))
            else:
                print('no insert ', end='')
                print(row)
            counter += 1
            if counter%100 == 0:
                db.session.commit()
                print(datetime.now(), end='')
                print(' geoip models_refresh.read_csv_and_update_database(): insert data into database ', end='')
                print(counter)
        db.session.commit()
        print(datetime.now(), end='')
        print(' geoip models_refresh.read_csv_and_update_database(): insert data into database ', end='')
        print(counter)


def delete_csv():
    """
    1. delete CSV file
    """
    print(datetime.now(), end='')
    print(' geoip models_refresh.delete_csv(): delete csv')
    try:
        os.remove('dbip-country.csv')
    except OSError:
        pass


def has_data():
    try:
        ipv4_cidr = Ipv4ClasslessInterDomainRouting.query.count() > 0
        ipv6_cidr = Ipv6ClasslessInterDomainRouting.query.count() > 0
        ipv4_int_range = Ipv4IntRange.query.count() > 0
        ipv6_int_range = Ipv6IntRange.query.count() > 0
        ipv4_str_range = Ipv4StrRange.query.count() > 0
        ipv6_str_range = Ipv6StrRange.query.count() > 0
        if ipv4_cidr and ipv6_cidr and ipv4_int_range and ipv6_int_range and ipv4_str_range and ipv6_str_range:
            print('geoip models_refresh.has_data(): return True (has data)')
            return True
        else:
            print('geoip models_refresh.has_data(): return False (no data)')
            return False
    except SQLAlchemyError:
        print('geoip models_refresh.has_data(): return False (SQLAlchemyError)')
        return False

