#!/usr/bin/env python

try:
    import yaml
except ImportError:
    raise ImportError('please run pip install pyyaml')

def get_config(config_file):
    # TODO: this needs more work in terms of error checking
    try:
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except:
        raise RuntimeError("could not load config file\n")

    return cfg