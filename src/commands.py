#!/usr/bin/env python3

import time
import socket
import argparse

from belcon_mini_III import DMH


def commands():
    """Sends forward / reverse commands."""
    dmh = DMH(cable_port)
    dmh.get_set_mode()

    if command_mode == 'external':
        ip = '169.0.0.1'
        port = 50007
        completemsg = 'complete'.encode('utf-8')
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((ip, port))     # binding with set IP and PORT
        serversock.listen(10)           # listening the connection (max num of the que)
        serversock.settimeout(300)
        print('Waiting for connections...')
        clientsock, client_address = serversock.accept() # store the data if it's connected
        clientsock.settimeout(3600)

    while True:
        if command_mode == 'local':
            key = input()
        elif command_mode == 'external':
            key = clientsock.recv(1024).decode('utf-8')
        if key == 'complete':
            print("Finished.")
            dmh.stop()
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
            break
        elif key == 'fl':
            print("Forward with low speed.")
            dmh.forward('low')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'fm':
            print("Forward with middle speed.")
            dmh.forward('middle')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'fh':
            print("Forward with high speed.")
            dmh.forward('high')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'il':
            print("Inverse with low speed.")
            dmh.inverse('low')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'im':
            print("Inverse with middle speed.")
            dmh.inverse('middle')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'ih':
            print("Inverse with high speed.")
            dmh.inverse('high')
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        elif key == 'stop':
            print("Just stopped.")
            dmh.stop()
            if command_mode == 'external':
                # TODO: check if it's working properly
                clientsock.sendall(completemsg)
        time.sleep(0.1)

    if command_mode == 'external':
        clientsock.close()
    dmh.close_connection()


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(description='Set options.')
    parser.add_argument(
        '--port', dest='port', type=str, default="COM11",
        help='set usb port number for the cable')
    parser.add_argument(
        '--command_from', dest='command_from', type=str,
        choices=['local', 'external'],
        help='set mode, [local] or [external]')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    cable_port = args.port
    command_mode = args.command_from
    commands()
