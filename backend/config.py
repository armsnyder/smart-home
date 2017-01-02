"""
Loading and managing key-value configuration from a private config.ini file. The configuration file serves to
    1. Reduce hard-coded values that might change in different environments. For example, the Philips Hue IP address.
    2. Keep secrets out of the codebase. For example, the Philips Hue user string.
"""

import os
import ConfigParser

# object containing loaded configuration
config = ConfigParser.ConfigParser()


def load():
    """
    Load data from the config.ini file into the global config object
    """
    root_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(root_path, '..', 'config.ini')
    config.read(config_path)

# Load configuration immediately upon loading this script
load()
