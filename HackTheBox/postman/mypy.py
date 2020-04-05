import sys
import os.path
import os

f = open("rockyou.txt", "r")

line = f.readline()

while line:
	os.system("openssl enc -d -des-ede3-cbc -in id.bak -out fddddile.txt -pass pass:" + line)

f.close()
