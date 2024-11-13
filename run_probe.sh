sudo setcap cap_net_raw,cap_net_admin=eip $(realpath $(which /usr/bin/python3))
/usr/bin/python3 probe.py eth0