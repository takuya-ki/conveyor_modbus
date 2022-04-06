#!/usr/bin/env python3

import time
import argparse

from dmh_commander import DMHCommander


def commands_to_host(ip, sockport):
    """Sending commands to the host Windows 10 machine."""
    dmhctr = DMHCommander(ip, sockport)

    while True:
        key = input("\n-----\nAvailable commands \
                    \n\nnl: normal rotation with low speed \
                    \nnm: normal rotation with middle speed \
                    \nnh: normal rotation with high speed \
                    \nrl: reverse rotation with low speed \
                    \nrm: reverse rotation with middle speed \
                    \nrh: reverse rotation with high speed \
                    \nstop: stop the motion \
                    \ncomplete: finish program \
                    \n-->")
        if key in ['complete',
                   'nl',
                   'nm',
                   'nh',
                   'rl',
                   'rm',
                   'rh',
                   'stop']:
            dmhctr.sendcommand(key)
            if key == 'complete':
                break
        time.sleep(0.1)

    dmhctr.closing()


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(
        description='Set options.')
    parser.add_argument(
        '--ip', dest='ip',
        type=str, default="169.0.0.1",
        help='set ip address set for the local machine')
    parser.add_argument(
        '--sockport', dest='sockport',
        type=int, default=50007,
        help='set port number for the socket connection')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    commands_to_host(
        args.ip,
        args.sockport)
