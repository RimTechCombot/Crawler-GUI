import http.client as client
import json
import socket
import urllib.request
import urllib.error



API_PORT = 5000
API_HOST = '0.0.0.0'


def get_domain_data(domain):
    try:
        connection = client.HTTPConnection(API_HOST, API_PORT, timeout=1)
        connection.request("GET", f"/get/{domain.lower()}")
        response = connection.getresponse()
        connection.close()
        if response.code == 404:
            raise client.HTTPException
        data = response.read().decode("U8")
        if data:
            return data
    except client.HTTPException:
        return "Domain not found in base, have you crawled it?"
    except (ConnectionRefusedError, socket.timeout):
        return "Connection refused"


def add_domain(domain):
    try:
        url = f"http://{API_HOST}:{API_PORT}/add"
        req = urllib.request.Request(url)
        req.add_header("Content-Type", "application/json; charset=utf-8")
        body = {"domain": domain.lower()}
        jsondata = json.dumps(body)
        jsondatabytes = jsondata.encode('utf-8')
        req.add_header("Content-Length", len(jsondatabytes))
        response = urllib.request.urlopen(req, jsondatabytes)
        data = json.load(response)
        return data
    except urllib.error.HTTPError:
        return "Bad domain format"
    except urllib.error.URLError:
        return "Connection refused"


def is_online(host="http://google.com"):
    try:
        urllib.request.urlopen(host, timeout=3)
        return True
    except urllib.request.URLError:
        return False


def check_endpoint():
    try:
        response = client.HTTPConnection(API_HOST, API_PORT, timeout=1)
        response.request("GET", "/get/example.com")
        return True
    except (urllib.request.URLError, ConnectionRefusedError):
        return False




