import requests
s = requests.session()
url="http://10.10.10.168:8080/"

while True:
	url="http://10.10.10.168:8080/"
	data = input("INTRODUCE NUEVA URL: ")
	url = url + data
	response = s.get(url)
	print(response.url)
	print(response.text)
