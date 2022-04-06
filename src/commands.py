#!/usr/bin/env python3

import socket
import argparse

from belcon_mini_III import DMH


def commands(
        usbport,
        command_mode,
        ip,
        sockport):
    """Sends commands."""
    dmh = DMH(usbport)
    dmh.get_set_mode()

    if command_mode == 'external':
        completemsg = 'complete'.encode('utf-8')
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((ip, sockport))
        serversock.listen(10)
        serversock.settimeout(300)
        print('Waiting for connections...')
        clientsock, client_address = serversock.accept()
        clientsock.settimeout(3600)

    while True:
        if command_mode == 'local':
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
        elif command_mode == 'external':
            key = clientsock.recv(1024).decode('utf-8')
        if key == 'complete':
            print("Finished.")
            dmh.stop()
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
            break
        elif key == 'nl':
            print("Normal with low speed.")
            dmh.move('normal', 'low')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'nm':
            print("Normal with middle speed.")
            dmh.move('normal', 'middle')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'nh':
            print("Normal with high speed.")
            dmh.move('normal', 'high')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'rl':
            print("Reverse with low speed.")
            dmh.move('reverse', 'low')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'rm':
            print("Reverse with middle speed.")
            dmh.move('reverse', 'middle')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'rh':
            print("Reverse with high speed.")
            dmh.move('reverse', 'high')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'stop':
            print("Just stopped.")
            dmh.stop()
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        dmh.sleep_with_displaying_freq(0.1)

    if command_mode == 'external':
        clientsock.close()
    dmh.close_connection()


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(
        description='Set options.')
    parser.add_argument(
        '--usbport', dest='usbport',
        type=str, default="COM11",
        help='set usb port number for the DINV U4 cable')
    parser.add_argument(
        '--command_from', dest='command_from',
        type=str, default='local',
        choices=['local', 'external'],
        help='set mode, [local] or [external]')
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
    commands(
        args.usbport,
        args.command_from,
        args.ip,
        args.sockport)
