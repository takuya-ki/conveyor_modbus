#!/usr/bin/env python3

import argparse

from belcon_mini_III import DMH


def run_reciprocation_demo(
        usbport, num_repeat, speed, direction1, direction2):
    """Reciprocation movement with some commands."""
    dmh = DMH(usbport)

    if not dmh.get_status()[0]:  # not RUN
        dmh.get_set_mode()

        print("High speed [Hz/100]: " +
              str(dmh.get_set_parameters(3)))
        print("Middle speed [Hz/100]: " +
              str(dmh.get_set_parameters(4)))
        print("Low speed [Hz/100]: " +
              str(dmh.get_set_parameters(5)))
        if speed == 'low':
            sleep_sec = 30
        elif speed == 'middle':
            sleep_sec = 15
        elif speed == 'high':
            sleep_sec = 10

        for i in range(num_repeat):
            dmh.move(direction1, speed)
            dmh.sleep_with_displaying_freq(sleep_sec)
            dmh.stop()
            dmh.sleep_with_displaying_freq(1)

            dmh.move(direction2, speed)
            dmh.sleep_with_displaying_freq(sleep_sec)
            dmh.stop()
            dmh.sleep_with_displaying_freq(1)

    dmh.close_connection()


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(
        description='Set options.')
    parser.add_argument(
        '--usbport', dest='usbport',
        type=str, default=None,
        help='set usb port number for the cable')
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
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    directions = ['normal', 'reverse']
    direction1 = args.direction
    direction2 = directions[not directions.index(direction1)]
    run_reciprocation_demo(
        args.usbport,
        args.num_repeat,
        args.speed,
        direction1,
        direction2)
