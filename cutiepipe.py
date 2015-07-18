#!/usr/bin/env python

"""
cutiepipe

Utility providing a simple interface for named Unix pipes.

Example Usage:
 # Terminal 1
 $ cat data.csv | cutiepipe

 # Terminal 2
 $ cutiepipe | data_copy.csv
"""

import sys
import select
import socket

HOST = 'localhost'
PORT = 10000
CNXN = (HOST, PORT)


def throw_error(message):
    print >> sys.stderr, "Cutie Pipe: " + message


def write_to_sock(e=None):

    # Is there data in the stdin?
    if select.select([sys.stdin], [], [], 0.0)[0]:

        # Create a simple socket server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(CNXN)
        s.listen(1)

        # Accept incoming connections
        try:
            client, addr = s.accept()
        except KeyboardInterrupt:
            exit()

        # Stream data from stdin to the client
        try:
            for line in iter(sys.stdin.readline, ''):
                client.send(line)
        except KeyboardInterrupt:
            exit()

        # Finally, close the client
        client.close()

    # If no data is in the stdin
    else:
        if e.__repr__ and 'Connection refused' in e.__repr__():
            throw_error("No input pipe detected")
            exit()
        throw_error("No input data detected and socket error " + e.__repr__())


def read_from_sock(s):

    def get_data():
        return s.recv(32)

    # Start data retrieval until no more data is available (or connection closes)
    for packet in iter(get_data, ''):
        sys.stdout.write(packet)
        sys.stdout.flush()


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(CNXN)
    except socket.error as e:
        write_to_sock(e)
    else:
        read_from_sock(sock)
    finally:
        sock.close()



if __name__ == '__main__':
    main()
