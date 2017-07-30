import requests
import json
import pprint

tick = requests.get('https://api.coinmarketcap.com/v1/ticker/?', {'limit': 10})
tick_dict = json.loads(tick.text)



class TickBoiz:

    def __init__(self, url='https://api.coinmarketcap.com/v1/ticker/?', **kwargs):
        self.url = url
        self.tick_data = {}
        self.update_ticker()


    def update_ticker(self):
        resp = requests.get('https://api.coinmarketcap.com/v1/ticker/?', {'limit': 10})
        tick_dict = {}
        for d in json.loads(resp.text):
            sym = d['symbol']
            tick_dict.setdefault(sym, {})
            for k, v in d.items():
                if not k == 'symbol':
                    tick_dict[sym][k] = v
        self.tick_data = tick_dict


tmp = TickBoiz()
pprint.pprint(tmp.tick_data)
