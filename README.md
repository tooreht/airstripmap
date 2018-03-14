# Airstripmap

Converts CSV files containing airstrip information into a KML file for visualisation in e.g. GoogleMaps, GoogleEarth, OSM...

## Concept

    +------+     +-----+     +-------+
    | READ | --> | MAP | --> | WRITE |
    +------+     +-----+     +-------+

The airstripmap programm operates in 3 stages:
1. Read input files and prepare them for stage 2
2. Map values from input files to internal data structure and apply business logic
3. Write generated internal data structure from stage 2 to output

```txt
                                            Logic
    haja.csv ------+                   +-----------------+
                   |     +------+      | validate   skip |      +-------+
                   +---> | READ | ---> |       MAP       | ---> | WRITE | --> airstrips.kml
                   |     +------+      | convert   merge |      +-------+
    wingman.csv ---+                   +-----------------+
```          

## Prequisites

- git
- python3

## Install

    $ git clone https://github.com/tooreht/airstripmap.git
    $ python3 -m venv venv
    $ ./venv/bin/activate
    $ pip install -r requirements.txt

## Usage

    $ python airstripmap.py --help
    usage: airstripmap.py [-h] [--out OUT_PATH] [--logic LOGIC] [--log LOGLEVEL]
                          in_paths [in_paths ...]

    positional arguments:
      in_paths        Input airstrip files

    optional arguments:
      -h, --help      show this help message and exit
      --out OUT_PATH  Output airstrips file
      --logic LOGIC   Which logic class to call
      --log LOGLEVEL  Set loglevel

**Example**

    $ python airstripmap.py --logic HajaWingman --out airstrips.kml haja.csv wingman.csv
    # With debug CLI output
    $ python airstripmap.py --log DEBUG --logic HajaWingman --out airstrips.kml haja.csv wingman.csv
