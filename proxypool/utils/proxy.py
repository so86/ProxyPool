from proxypool.schemas import Proxy
import re

def is_valid_proxy(data):
    if data.__contains__(':'):
        pattern = re.compile(
            r'((?P<username>\S*?)\:(?P<password>\S*?)@)?(?P<ip>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\:(?P<port>\d*)')
        match = re.search(pattern, data)
        username = match.groupdict()['username']
        password = match.groupdict()['password']
        ip = match.groupdict()['ip']
        port = match.groupdict()['port']
        return is_ip_valid(ip) and is_port_valid(port)
    else:
        return is_ip_valid(data)


def is_ip_valid(ip):
    a = ip.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def is_port_valid(port):
    return port.isdigit()


def convert_proxy_or_proxies(data):
    """
    convert list of str to valid proxies or proxy
    :param data:
    :return:
    """
    if not data:
        return None
    # if list of proxies
    if isinstance(data, list):
        result = []
        for item in data:
            # skip invalid item
            item = item.strip()
            if not is_valid_proxy(item): continue
            pattern = re.compile(
                r'((?P<username>\S*?)\:(?P<password>\S*?)@)?(?P<ip>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\:(?P<port>\d*)')
            match = re.search(pattern, item)
            username = match.groupdict()['username']
            password = match.groupdict()['password']
            ip = match.groupdict()['ip']
            port = match.groupdict()['port']
            result.append(Proxy(host=ip, port=int(port), username=username, password=password))
        return result
    if isinstance(data, str) and is_valid_proxy(data):
        pattern = re.compile(
            r'((?P<username>\S*?)\:(?P<password>\S*?)@)?(?P<ip>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\:(?P<port>\d*)')
        match = re.search(pattern, data)
        username = match.groupdict()['username']
        password = match.groupdict()['password']
        ip = match.groupdict()['ip']
        port = match.groupdict()['port']
        return Proxy(host=ip, port=int(port), username=username, password=password)
