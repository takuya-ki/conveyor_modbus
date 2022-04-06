#!/usr/bin/env python3

import time
import argparse

from dmh_commander import DMHCommander


def run_reciprocation_demo(
        ip,
        sockport,
        num_repeat,
        speed,
        direction1,
        direction2):
    """Reciprocation movement with some commands."""
    dmhctr = DMHCommander(ip, sockport)
    time.sleep(1)
    if speed == 'low':
        sleep_sec = 30
    elif speed == 'middle':
        sleep_sec = 15
    elif speed == 'high':
        sleep_sec = 10

    for i in range(num_repeat):
        dmhctr.sendcommand(direction1[0] + speed[0])
        time.sleep(sleep_sec)
        dmhctr.sendcommand('stop')
        time.sleep(1)

        dmhctr.sendcommand(direction2[0] + speed[0])
        time.sleep(sleep_sec)
        dmhctr.sendcommand('stop')
        time.sleep(1)

    dmhctr.closing()


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(
        description='Set options.')
    parser.add_argument(
        '--num_repeat', dest='num_repeat',
        type=int, default=1,
        help='set numbet of reciprocation demo')
    parser.add_argument(
        '--speed', dest='speed',
        type=str, default='low',
        choices=['low', 'middle', 'high'],
        help='set movement speed')
    parser.add_argument(
        '--initial_direction', dest='direction',
        type=str, default='normal',
        choices=['normal', 'reverse'],
        help='set a movement direction (initial state)')
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
    directions = ['normal', 'reverse']
    direction1 = args.direction
    direction2 = directions[not directions.index(direction1)]
    run_reciprocation_demo(
        args.ip,
        args.sockport,
        args.num_repeat,
        args.speed,
        direction1,
        direction2)
