import hashlib
import re
import requests

url="http://docker.hackthebox.eu:31755/"

r=requests.session()
out=r.get(url)
out=re.search("<h3 align='center'>+.*?</h3>",out.text)
out=re.search("'>.*<",out[0])
out=re.search("[^|'|>|<]...................",out[0])

out=haslib.md5(out[0].encode("utf-8")).hexdigest()

data={'hash':out}

request=r.post(url=url,data=data)
print(request.text)
