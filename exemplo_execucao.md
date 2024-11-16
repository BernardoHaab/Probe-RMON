```bash
@BernardoHaab ➜ /workspaces/Probe-RMON (main) $ snmpset -v2c -c private localhost .1.3.6.1.2.1.16.1.1.1.2.1 s eth0
iso.3.6.1.2.1.16.1.1.1.2.1 = STRING: "eth0"
@BernardoHaab ➜ /workspaces/Probe-RMON (main) $ snmpset -v2c -c private localhost .1.3.6.1.2.1.1
6.1.1.1.20.1 s Bernardo
iso.3.6.1.2.1.16.1.1.1.20.1 = STRING: "Bernardo"
@BernardoHaab ➜ /workspaces/Probe-RMON (main) $ snmpset -v2c -c private localhost .1.3.6.1.2.1.1
6.1.1.1.21.1 i 2
iso.3.6.1.2.1.16.1.1.1.21.1 = INTEGER: 2
@BernardoHaab ➜ /workspaces/Probe-RMON (main) $ snmpset -v2c -c private localhost .1.3.6.1.2.1.16.1.1.1.21.1 i 1
iso.3.6.1.2.1.16.1.1.1.21.1 = INTEGER: 1
@BernardoHaab ➜ /workspaces/Probe-RMON (main) $ snmpget -v2c -c private localhost .1.3.6.1.2.1.16.1.1.1.5.1
iso.3.6.1.2.1.16.1.1.1.5.1 = STRING: "306"
@BernardoHaab ➜ /workspaces/Probe-RMON (main) $ snmpget -v2c -c private localhost .1.3.6.1.2.1.16.1.1.1.5.1
iso.3.6.1.2.1.16.1.1.1.5.1 = STRING: "523"
@BernardoHaab ➜ /workspaces/Probe-RMON (main) $ snmpget -v2c -c private localhost .1.3.6.1.2.1.16.1.1.1.4.1
iso.3.6.1.2.1.16.1.1.1.4.1 = STRING: "454937"
```