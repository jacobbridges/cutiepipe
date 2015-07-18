# cutiepipes

## Setup
Requires [beanstalkd](http://kr.github.io/beanstalkd/download.html) to be running on your local machine with default settings.

Also requires the Python beanstalk client [beanstalkc](https://github.com/earl/beanstalkc)

## Usage
```shell
# Shell session 1
$ cat data.json | cutiepipe

# Shell session 2
$ cutiepipe > data_copy.json
```
