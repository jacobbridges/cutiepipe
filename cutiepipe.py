#!/usr/bin/env python

"""
cutiepipe

Utility providing a simple interface for named Unix pipes.

See project README for example usage.
"""

import sys
import select
import socket
from time import sleep

HOST = 'localhost'
PORT = 10000
CNXN = (HOST, PORT)


def throw_error(message):
    print >> sys.stderr, "Cutie Pipe: " + message


def stream_to_socket():
    # Create a simple socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(CNXN)
    s.listen(1)
    try:
        # Accept incoming connections
        client, addr = s.accept()
        # Stream data from stdin to the client
        for line in iter(sys.stdin.readline, ''):
            client.send(line)
        # Finally, close the client
        client.close()
    except KeyboardInterrupt:
        exit()


def read_from_socket(s):
    def get_data():
        return s.recv(32)
    # Start data retrieval until no more data is available (or connection closes)
    try:
        for packet in iter(get_data, ''):
            sys.stdout.write(packet)
            sys.stdout.flush()
    except KeyboardInterrupt:
        exit()
    finally:
        s.close()


def create_listener():
    # Loop until socket connection can be established
    while True:
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Try connecting input pipe
            s.connect(CNXN)
        except socket.error:
            # If connection failed, try again in a second
            s.close()
            sleep(1)
            continue
        except KeyboardInterrupt:
            # If a Ctrl-C is encountered, close socket and exit program
            s.close()
            exit()
        else:
            # If the connection was successful, return the connected socket
            return s


def main():
    # Is there data in stdin?
    if select.select([sys.stdin], [], [], 0.0)[0]:
        # Stream the data through a socket
        stream_to_socket()
    # No data in stdin?
    else:
        # Setup a socket listener
        read_from_socket(create_listener())


if __name__ == '__main__':
    main()
