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

import sys
import argparse
from nacky import initial_setup, connection_setup, reset
from check_dependencies import check_dependencies

def check_params():
    parser = argparse.ArgumentParser(description="NAC bypass script")
    parser.add_argument("-1", dest="swint", metavar="eth", help="network interface plugged into switch")
    parser.add_argument("-2", dest="compint", metavar="eth", help="network interface plugged into victim machine")
    parser.add_argument("-a", dest="autonomous", action="store_true", help="autonomous mode")
    parser.add_argument("-c", dest="connection_setup_only", action="store_true", help="start connection setup only")
    parser.add_argument("-g", dest="gwmac", metavar="MAC", help="set gateway MAC address (GWMAC) manually")
    parser.add_argument("-i", dest="initial_setup_only", action="store_true", help="start initial setup only")
    parser.add_argument("-r", dest="reset", action="store_true", help="reset all settings")
    parser.add_argument("-R", dest="responder", action="store_true", help="enable port redirection for Responder")
    parser.add_argument("-S", dest="ssh", action="store_true", help="enable port redirection for OpenSSH and start the service")
    parser.add_argument("-d", "--check-dependencies", action="store_true", help="Check if all required tools are installed")

    args = parser.parse_args()
    return args

def main():
    args = check_params()
    
    if args.check_dependencies:
        if not check_dependencies():
            print("Please install the missing tools and try again.")
            return
        else:
            print("All required tools are installed.")
            return
    
    
    if args.reset:
        reset()
        sys.exit(0)

    if args.initial_setup_only:
        initial_setup(args)
        sys.exit(0)

    if args.connection_setup_only:
        connection_setup(args)
        sys.exit(0)

    initial_setup()
    connection_setup()

if __name__ == "__main__":
    main()
