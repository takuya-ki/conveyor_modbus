#!/usr/bin/env python3

import time
import argparse

from belcon_mini_III import DMH


def run_demo():
    """Sends forward / reverse commands once."""
    dmh = DMH(cable_port)

    if not dmh.get_status()[0]:  # not RUN
        dmh.get_set_mode()

        print(dmh.get_set_parameters(3))
        print(dmh.get_set_parameters(4))
        print(dmh.get_set_parameters(5))

        dmh.forward('low')
        start = time.time()
        while True:
            time.sleep(0.1)
            print("Frequency: " + 
                  str(dmh.get_actual_frequency()) +
                  " / " +
                  str(dmh.get_set_frequency()) +
                  " [Hz/100]")
            if (time.time() - start) > 5.0:
                break
        dmh.stop()
        time.sleep(3.0)

        dmh.inverse('low')
        start = time.time()
        while True:
            time.sleep(0.1)
            print("Frequency: " + 
                  str(dmh.get_actual_frequency()) +
                  " / " +
                  str(dmh.get_set_frequency()) +
                  " [Hz/100]")
            if (time.time() - start) > 5.0:
                break
        dmh.stop()
        time.sleep(3.0)

        dmh.forward('high')
        start = time.time()
        while True:
            time.sleep(0.1)
            print("Frequency: " + 
                  str(dmh.get_actual_frequency()) +
                  " / " +
                  str(dmh.get_set_frequency()) +
                  " [Hz/100]")
            if (time.time() - start) > 5.0:
                break
        dmh.stop()
        time.sleep(3.0)

        dmh.inverse('high')
        start = time.time()
        while True:
            time.sleep(0.1)
            print("Frequency: " + 
                  str(dmh.get_actual_frequency()) +
                  " / " +
                  str(dmh.get_set_frequency()) +
                  " [Hz/100]")
            if (time.time() - start) > 5.0:
                break
        dmh.stop()
        time.sleep(3.0)

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
    run_demo()