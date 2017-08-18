import yaml
import logging
import requests
import os


class MirrorConfig:
    """Class that contains config for crypto-mirror UI and stuff"""
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.validate_token()

    def validate_token(self):
        key_manager = KeyManager(self.weather_key_path)
        key_manager.fetch_keys()
        self.weather_api_token = key_manager.api_key

    @classmethod
    def from_yaml(cls, config_path):
        with open(config_path, 'r') as cfh:
            tmp_cfg = yaml.load(cfh)
            tmp_cfg['config_path'] = config_path
        return cls(**tmp_cfg)


class KeyManager:
    def __init__(self, api_key=None, key_path='assets/keys.yml', key_status=False):
        self.key_path = key_path
        self.key_status = key_status
        self.api_key = api_key
        self.fetch_keys()

    def fetch_keys(self):
        if os.path.exists(self.key_path):
            with open(self.key_path) as kfh:
                key_dict = yaml.load(kfh)
                self.api_key = key_dict['darksky_token'] if key_dict else ''
        else:
            # assume that file doesnt exist, create it
            self.add_key()

    def add_key(self):
        """Prompts user for darksky key, creates key_file if valid"""
        new_key = input('It doesnt look like you have any API keys yet. '
                        'Create one at darksky.net/dev, then paste it here: ')
        if new_key:
            valid = self.key_test(new_key)
            if valid:
                # Set key and key status
                self.key_status = True
                self.api_key = new_key

                # write new key to file
                try:
                    key_dict = {'darksky_token': new_key}
                    with open(self.key_path, 'w') as cfh:
                        cfh.write(f'darksky_token: {new_key}')
                    print('Key file created successfully!')
                except Exception as e:
                    print(f'Failed to create key file: {e}')
        else:
            print('Invalid key')

    @staticmethod
    def key_test(key, exp_return=200):
        """Makes a test call to darksky api"""
        resp = requests.get(f'https://api.darksky.net/forecast/{key}/38,-77?lang=en&units=us')
        return True if resp.status_code == exp_return else False


def curr_fmt(price):
    return round(float(price),2)