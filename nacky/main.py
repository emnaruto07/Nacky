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
import argparse
from nacky import initial_setup, connection_setup
from nacky import VERSION

# def usage():
#     print(f"{sys.argv[0]} v{VERSION} usage:")
#     print("    -1 <eth>    network interface plugged into switch")
#     print("    -2 <eth>    network interface plugged into victim machine")
#     print("    -a          autonomous mode")
#     print("    -c          start connection setup only")
#     print("    -g <MAC>    set gateway MAC address (GWMAC) manually")
#     print("    -h          display this help")
#     print("    -i          start initial setup only")
#     print("    -r          reset all settings")
#     print("    -R          enable port redirection for Responder")
#     print("    -S          enable port redirection for OpenSSH and start the service")
#     sys.exit(0)

def version():
    print(f"{sys.argv[0]} v{VERSION}")
    sys.exit(0)

def check_params():
    parser = argparse.ArgumentParser(description="NAC bypass script", add_help=False)
    parser.add_argument("-1", dest="swint", metavar="eth", help="network interface plugged into switch")
    parser.add_argument("-2", dest="compint", metavar="eth", help="network interface plugged into victim machine")
    parser.add_argument("-a", dest="autonomous", action="store_true", help="autonomous mode")
    parser.add_argument("-c", dest="connection_setup_only", action="store_true", help="start connection setup only")
    parser.add_argument("-g", dest="gwmac", metavar="MAC", help="set gateway MAC address (GWMAC) manually")
    parser.add_argument("-h", dest="show_help", action="store_true", help="display this help")
    parser.add_argument("-i", dest="initial_setup_only", action="store_true", help="start initial setup only")
    parser.add_argument("-r", dest="reset", action="store_true", help="reset all settings")
    parser.add_argument("-R", dest="responder", action="store_true", help="enable port redirection for Responder")
    parser.add_argument("-S", dest="ssh", action="store_true", help="enable port redirection for OpenSSH and start the service")

    args = parser.parse_args()
    # args = parser.print_help()

    # if args.show_help:
    #     usage()

    return args

if __name__ == "__main__":
    args = check_params()
    print(args)
    # initial_setup()
    # connection_setup()