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
import beanstalkc


def main():

    # Attempt to create a localhost connection with beanstalkd
    try:
        beanstalk = beanstalkc.Connection()
    except beanstalkc.SocketError:
        print 'Could not find beanstalkd connection.'
        exit()
    except Exception as e:
        raise e

    # Create a cleanup function
    def fin():
        beanstalk.close()

    # Wait for data to read and redirect
    while True:

        # Check for a beanstalk job
        job = beanstalk.reserve(timeout=0)

        # Process job
        if job is not None:
            sys.stdout.write(job.body)
            sys.stdout.write('\n')
            job.delete()
            fin()
            break

        # Check for data in the stdin
        if select.select([sys.stdin], [], [], 0.0)[0]:
            beanstalk.put(sys.stdin.read())
            fin()
            break


if __name__ == '__main__':
    main()
