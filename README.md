# cutiepipes

## Setup
Requires port 10000 to be available. (configurable in cutiepipe.py)

## Usage

### Piping entire files
```shell
# Shell session 1
$ cat data.json | cutiepipe

# Shell session 2
$ cutiepipe > data_copy.json
```

### Piping streams
```shell
# Shell session 1
$ tail -f -n 1 data.csv | cutiepipe

# Shell session 2
$ cutiepipe > data_copy.csv
```