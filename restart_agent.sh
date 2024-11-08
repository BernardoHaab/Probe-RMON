# Add pass directive to snmpd.conf
sudo tee /etc/snmp/snmpd.conf > /dev/null <<EOF
rocommunity public
rwcommunity private

pass_persist .1.3.6.1.2.1.16.1 /usr/bin/python3 /tmp/probe.py
EOF

# Restart agent - Linux
sudo service snmpd restart
sudo service snmpd status