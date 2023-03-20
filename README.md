
<h1 align="center">
NACKY
</h1>
<p align="center">
Bypass Network Access Control (NAC, 802.1x)
</p>

# Nacky - Network Access Control Bypass Tool (v1.0)
Nacky is a Python-based Network Access Control (NAC) bypass tool, which allows an attacker to gain unauthorized access to a network by bypassing NAC mechanisms. The tool is based on the NACkered script and the nac_bypass_setup.sh solution. I want to express my gratitude to the original authors of these scripts.

## Requirements
To perform an NAC bypass, you need access to an authenticated device. This device is used to log into the network and smuggle network packets from another device. You can achieve this by placing the attacker's system between the network switch and the authenticated device using a Raspberry Pi and two network adapters.

## Installation
Nacky was developed and tested on Debian-based Linux distributions, but it should be compatible with other Linux distributions as well. The following software packages are required:

1. Install tools, on Debian-like distros: `bridge-utils` `macchanger` `arptables` `ebtables` `iptables` `net-tools` `tcpdump`
2. Load kernel module: `modprobe br_netfilter`
3. Persist kernel module: `br_netfilter`into `/etc/modules`

For arptables, iptables, and ebtables, make sure not to use Netfilter xtable tools (nft), or the script will not work as desired.
## Usage
1. Disconnect the legitimate device (client) from the network switch.
2. Start the script on the attacker device (bypass). The bypass and attacker devices are the same physical device. The attacker figure symbolizes actions carried out by the attacker on the NAC bypass device.
3. Perform the initial configuration, which includes stopping unwanted services, disabling IPv6, and initializing DNS configurations.
4. Configure and start the bridge. Adjust the kernel to forward EAPOL frames for successful 802.1X authentication.
5. Connect the network cables and enable the bridge's switch side as a passive forwarder. The client should now be authenticated with the network switch and can log into the network successfully.
6. Analyze the network traffic passing through the bridge to capture Kerberos and SMB packets. This information is used to automatically configure the client side of the bridge.
7. If port forwarding has been enabled for SSH and Responder, the bridge forwards all requests for the respective ports to the attacker's services.
Responder
8. Run Responder on the bridge interface with the correct IP address for poisoning multicast using the `-e` parameter:

```
./Responder.py -I <bridge_interface> -e <client_address> ...
```
## Acknowledgements
We would like to thank the original authors of the NACkered script and the nac_bypass_setup.sh solution for their valuable work, which served as the foundation for the development of nacky.
