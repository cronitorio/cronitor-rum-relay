import hashlib
import uuid
from typing import List, Dict

import geoip2.database
import geoip2.errors


def select_headers(headers: Dict[str, str], selection: List[str]):
    result = dict()
    for header in selection:
        if value := headers.get(header):
            result[header] = value
    return result


def create_relay_session_id(client_ip: str, salt: str) -> str:
    # Ensure we have a session id that is not just a hash of the IP
    if not (client_ip and salt):
        return uuid.uuid4().hex
    m = hashlib.sha256()
    m.update(client_ip.encode())
    m.update(salt.encode())
    return m.hexdigest()


# ref: https://stackoverflow.com/a/46877220
def split_host_port(string):
    """
    Returns a tuple of host|ip and port.
    Support IPv4 and IPv6 too.

    Examples:
         split_host_port("::1:80") == ("::1", 80)
         split_host_port("[::1]:80") == ("[::1]", 80)
         split_host_port("127.0.0.1:443") == ("127.0.0.1", 443)
         split_host_port("localhost") == ("localhost", None)
    """
    if not string.rsplit(":", 1)[-1].isdigit():
        return string, None

    string = string.rsplit(":", 1)

    host = string[0]  # 1st index is always host
    port = int(string[1])

    return host, port


def sanitize_client_ip(value):
    """
    Tries to extract plain ip (without port).
    """
    if not value:
        return value
    host, port = split_host_port(value)
    if host:
        return host
    return value


class GeoIP:
    def __init__(self, filename):
        self.filename = filename
        self.reader = geoip2.database.Reader(filename)

    def lookup_country_code(self, client_ip):
        return self.reader.city(client_ip).country.iso_code

    def lookup_city_name(self, client_ip):
        return self.reader.city(client_ip).city.name
