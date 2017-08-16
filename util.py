import yaml


class MirrorConfig:
    """Class that contains config for smartmirror"""
    def __init__(self, config_path):
        with open(config_path, 'r') as cfh:
            tmp_config = yaml.load(cfh)
            for key in tmp_config:
                setattr(self, key, tmp_config[key])

    def token_is_valid(self, token):
        if len(token) < 32 and


import requests
q = response.get()
import pandas
pandas.Dat
