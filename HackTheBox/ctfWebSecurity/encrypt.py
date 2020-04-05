from bs4 import BeautifulSoup
import requests
import string
import hashlib

s=requests.session()
url='http://docker.hackthebox.eu:32423/'
html_doc=s.get(url).text

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())
md5=soup.find_all('h3')
md5=str(md5[0])

print(md5)

joder = md5.replace('<h3 align="center">',"")
print(joder)
joder = joder.replace('</h3>',"")
print(joder)
joder = hashlib.md5(joder)
data = joder.hexdigest()

datahash = {"hash" : data}

post = s.post(url=url,data=datahash)
print(post.text)
