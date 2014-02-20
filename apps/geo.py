# coding: utf-8
import requests

def get_lat_long_from_ip(ip):
    try:
        r = requests.get('http://secret-ips.herokuapp.com/api/ip-city?ip=%s' % ip)
        r = r.json()
        return (float(r['latitude']), float(r['longitude']))
    except KeyError as e:
        print(ip, r)
        raise e
