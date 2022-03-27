#!/usr/bin/env python3

import time
import argparse

from belcon_mini_III import DMH


def commands():
    """Sends forward / reverse commands."""
    dmh = DMH(cable_port)
    dmh.get_set_mode()

    while True:
        key = input()
        if key == 'e':
            print("Finished.")
            dmh.stop()
            break
        elif key == 'fl':
            print("Forward with low speed.")
            dmh.forward('low')
        elif key == 'fm':
            print("Forward with middle speed.")
            dmh.forward('middle')
        elif key == 'fh':
            print("Forward with high speed.")
            dmh.forward('high')
        elif key == 'il':
            print("Inverse with low speed.")
            dmh.inverse('low')
        elif key == 'im':
            print("Inverse with middle speed.")
            dmh.inverse('middle')
        elif key == 'ih':
            print("Inverse with high speed.")
            dmh.inverse('high')
        elif key == 's':
            print("Just stopped.")
            dmh.stop()

    dmh.close_connection()


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(description='Set options.')
    parser.add_argument(
        '--port', dest='port', type=str, default="COM11",
        help='set usb port number for the cable')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    cable_port = args.port
    commands()
