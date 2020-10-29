import requests
import random
import pyogame.services as service


def proxyList():
    proxies = []
    response = requests.get(
        url=service.secrets.PROXY_URL
    ).text
    for proxy in response.split('\r\n'):
        if proxy == '':
            continue
        proxy = proxy.split(':')
        proxies.append('https://{}:{}@{}:{}'.format(proxy[2], proxy[3], proxy[0], proxy[1]))
    return proxies


def test(proxy):
    proxy = {'https': proxy}
    try:
        ip = requests.get("https://api.ipify.org/?format=json", proxies=proxy, timeout=3).json()['ip']
        return True
    except:
        return False


def randomProxy():
    proxy = random.choice(proxyList())
    if test(proxy):
        return proxy
    else:
        randomProxy()
