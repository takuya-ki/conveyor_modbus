#!/usr/bin/env python3

import time
import argparse

from belcon_mini_III import DMH


def check_params(usbport, param_list):
    """Checks parameter values."""
    dmh = DMH(usbport)

    if not dmh.get_status()[0]:  # not RUN
        dmh.get_set_mode()

        for p in param_list:
            print("Pr. "+str(p)+": "+str(dmh.get_set_parameters(p-1)))

    dmh.close_connection()


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(description='Set options.')
    parser.add_argument(
        '--usbport', dest='usbport', type=str, default="COM11",
        help='set usb port number for the DINV U4 cable')

    def p(x): return list(map(int, x.split(',')))
    parser.add_argument(
        '--params', type=p,
        default="160,117,118,120,122,123,124,343,502,549,77,79,551,340",
        help='set parameter numbers')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    check_params(
        args.usbport,
        args.params)
