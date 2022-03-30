#!/usr/bin/env python3

import time
import argparse

from dmh_commander import DMHCommander


def run_reciprocation_demo(
        num, speed, direction1, direction2):
    """Reciprocation movement with some commands."""
    dmhctr = DMHCommander()
    time.sleep(1)
    if speed == 'low':
        sleep_sec = 30
    elif speed == 'middle':
        sleep_sec = 15
    elif speed == 'high':
        sleep_sec = 10

    for i in range(num):
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
        '--reciprocation', dest='reciprocation',
        type=int, default=1,
        help='set numbet of reciprocation demo')
    parser.add_argument(
        '--speed', dest='speed',
        type=str, default='low',
        choices=['low', 'middle', 'high'],
        help='set movement speed')
    parser.add_argument(
        '--first_direction', dest='direction',
        type=str, default='normal',
        choices=['normal', 'reverse'],
        help='set movement direction')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    directions = ['normal', 'reverse']
    direction1 = args.direction
    direction2 = directions[not directions.index(direction)]
    run_reciprocation_demo(
        args.reciprocation,
        args.speed,
        direction1,
        direction2)
