import requests

url = 'http://85.159.212.181/login-panel.php'

while True:
	username = input("usuario: ")
	password = input("password: ")

	u = url + 'username=' + username + '&password=' + password
	r = requests.post(url)
	print(r.reason)
	print(r.request)
	print(r.headers)
