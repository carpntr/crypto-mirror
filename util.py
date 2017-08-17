import yaml
import string
import logging
import requests



def darksky_call(token, exp_return):
    resp = requests.get(f'https://api.darksky.net/forecast/{token}/38,-77?lang=en&units=us')
    logging.info('Making test API call to darksky.net...')
    logging.info(f'Call returned status code: {resp.status_code}')

    # Check if expected
    if resp.status_code == exp_return:
        logging.info('Weather API token validated!')
        return True
    else:
        return False

class MirrorConfig:
    """Class that contains config for smartmirror"""
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.validate_token()

    def validate_token(self):
        token = self.weather_api_token
        # Check if it meets basic criteria
        valid = darksky_call(token, 200)
        if valid:
            return
        else:
            # Invalid weather token?
            user_token = input('Something is wrong with your Darksky.net API token!\n'
                               'Input a better token or press ENTER to continue without valid token: ')
            if user_token:
                if darksky_call(user_token, 200):
                    # User passed in a valid token, so replace old one in config file
                    old_cfg = open(self.config_path).read()
                    new_cfg = old_cfg.replace(token, user_token)
                    with open(self.config_path, 'w') as cfh:
                        cfh.write(new_cfg)
                    self.weather_api_token = user_token
        return

    @classmethod
    def from_yaml(cls, config_path):
        with open(config_path, 'r') as cfh:
            tmp_cfg = yaml.load(cfh)
            tmp_cfg['config_path'] = config_path
        return cls(**tmp_cfg)

