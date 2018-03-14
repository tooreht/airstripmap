#!/usr/bin/env python

import argparse
import logging
import logging.config
import yaml

import logic

from pathlib import Path


logger = logging.getLogger('cli')

DEFAULT_LOGIC = "HajaWingman"


def setup_logging(path, loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(loglevel))

    with open(path, 'r') as f:
        config = yaml.safe_load(f.read())

    config['handlers']['console']['level'] = numeric_level

    logging.config.dictConfig(config)

def main(args):
    # Compose logic class name
    logic_class_name = "{}Logic".format(args.logic)
    # Call logic class
    logic_cls = getattr(logic, logic_class_name)
    logger.info("Calling {} with args {}".format(logic_class_name, args))
    return logic_cls(args.in_paths, args.out_path).run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_paths", nargs='+', help="Input airstrip files")
    parser.add_argument("--out", dest="out_path", help="Output airstrips file")
    parser.add_argument("--logic", dest="logic", default=DEFAULT_LOGIC, help="Which logic class to call")
    parser.add_argument("--log", dest="loglevel", default="ERROR", help="Set loglevel")
    args = parser.parse_args()

    setup_logging(path="logging.yaml", loglevel=args.loglevel)
    main(args)
