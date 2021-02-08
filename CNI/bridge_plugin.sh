#!/usr/bin/env bash
printf "\nCleaning namespaces ...\n"
find /var/run/netns -type f -exec sh -c "basename {} | xargs ip netns del " \;
rm -rf /var/lib/cni/networks/mynet/
export CNI_PATH=/opt/cni/bin
export CNI_CONTAINERID=test
export CNI_COMMAND=ADD
export CNI_NETNS=/var/run/netns/${CNI_CONTAINERID}
ip netns add ${CNI_CONTAINERID}
export CNI_IFNAME="eth0"
/opt/cni/bin/bridge < /etc/cni/net.d/10-bridge.conf
export CNI_IFNAME="lo"
/opt/cni/bin/loopback < /etc/cni/net.d/99-loopback.conf
printf "\nChecking Pod ip ... \n"
ip netns exec ${CNI_CONTAINERID} ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
