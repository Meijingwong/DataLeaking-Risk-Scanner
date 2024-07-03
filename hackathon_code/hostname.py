import socket
from urllib.parse import urlparse

def valid_hostname(url: str):
    """
    :parameter hostname: The hostname requested in the scan
    :return: Hostname if it's valid, None check if it's an IP address, otherwise False
    """
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    HNscore=0

    # Block attempts to scan things like 'localhost'
    if '.' not in hostname or 'localhost' in hostname:
        return False

    # try to see if it's an IPv4 address
    try:
        socket.inet_aton(hostname)  # inet_aton() will throw an exception if hostname is not a valid IP address
        return None  # If we get this far, it's an IP address and therefore not a valid hostname
    except:
        pass

    # And IPv6
    try:
        socket.inet_pton(socket.AF_INET6, hostname)  # same as inet_aton(), but for IPv6
        return None
    except:
        pass

    # try to do a lookup on the hostname; this should return at least one entry and should be the first time
    # that the validator is making a network connection -- the same that requests would make.
    try:
        hostname_ips = socket.getaddrinfo(hostname, 443)

        if len(hostname_ips) < 1:
            return False
        
        HNscore=9
    except:
        return False

    return hostname,HNscore

# print(valid_hostname(url))

def valid_scheme(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    schemeScore=0
    if scheme == '':
        if url.netloc == '':
            # Relative URL (src="/path")
            relativeorigin = True
        else:
            # Relative protocol (src="//host/path")
            relativeorigin = False
    else:
        relativeorigin = False

    # check if it's a secure scheme
    if scheme == 'https' or (relativeorigin and scheme == 'https'):
        securescheme = True
        schemeScore=8
    else:
        securescheme = False

    return securescheme,schemeScore

# print(valid_scheme(url))