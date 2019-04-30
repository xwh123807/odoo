# import urllib.request
#
# resu = urllib.request.urlopen("http://localhost:8069", data=None)
# data = resu.read().decode()
# print(data)
#
# import http.client
#
# conn = http.client.HTTPConnection("http://localhost:8069")
# conn.request("GET", "/")
# r1 = conn.getresponse()
# print(r1.status)

import requests

req = requests.get('http://localhost:8069')
print(req.content)
