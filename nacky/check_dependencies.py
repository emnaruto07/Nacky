#!/usr/bin/env python3


# Python version
# -----
# Updated Script:
# Name: NACKY
# Shazeb - Nacky v1.0
# -----
# Name: nac_bypass_setup.sh
# scip AG - Michael Schneider
# -----
# Original Script:
# Matt E - NACkered v2.92.2 - KPMG LLP 2014
# KPMG UK Cyber Defence Services
# -----

import subprocess


def check_tool(tool):
    try:
        if tool == "bridge-utils":
            result = subprocess.run(["ip", "add"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0

        elif tool == "net-tools":
            result = subprocess.run(["ifconfig"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0
        
        else:
            result =  subprocess.run([tool, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0


    except FileNotFoundError:
        return False


def check_dependencies():
    required_tools = ["bridge-utils", "macchanger", "arptables", "ebtables", "iptables", "net-tools", "tcpdump"]

    all_tools_installed = True
    for tool in required_tools:
        if check_tool(tool):
            print(f"[+] {tool} is available.")
        else:
            print(f"[-] {tool} is not available.")
            all_tools_installed = False

    return all_tools_installed
