#!/usr/bin/env python3

import time
import argparse

from dmh_commander import DMHCommander


def run_demo():
    """Sends some commands."""
    dmhctr = DMHCommander()
    time.sleep(3)
    dmhctr.sendcommand('fl')  # foward with low speed
    time.sleep(3)
    dmhctr.sendcommand('fh')  # foward with high speed
    time.sleep(3)
    dmhctr.sendcommand('il')  # inverse with low speed
    time.sleep(3)
    dmhctr.sendcommand('ih')  # inverse with high speed
    time.sleep(3)
    dmhctr.closing()


if __name__ == '__main__':
    run_demo()
