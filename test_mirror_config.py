from tkinter import *
import locale, threading
import time
import requests, json
import traceback
from util import MirrorConfig
from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()
CONFIG_PATH = 'config.yml'
CONFIG = MirrorConfig.from_yaml(CONFIG_PATH)

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


# ToDO: Go lookup autouse fixture


class Ticker(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.symbols = CONFIG.ticker['symbols']
        self.url = CONFIG.ticker['url']

        # Create all labels based on symbols

        self.update_symbols()


    def update_symbols(self):
        tick_dict = {}
        resp = requests.get(self.url, {'limit': 10})
        for d in json.loads(resp.text):
            sym = d['symbol']
            if sym in self.symbols:
                # Create dictionary for given symbol
                for k, v in d.items():
                    tick_dict[k] = v

                # Create a coinlabel from tick_dict
                setattr(self, sym, Coin.from_dict(tick_dict))




class Coin(Label):
    def __init__(self, **kwargs):
        # Assign attributes from tick_dict
        self.__dict__.update(kwargs)
        Label.__init__(self,font=('Helvetica', CONFIG.medium_text_size),
                       fg='white',
                       bg='black')
        self.pack(side=TOP, anchor=W)
        #print(self.symbol)

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)



class FullscreenWindow():
    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background='black')
        self.midFrame = Frame(self.tk, background='black')
        self.bottomFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.midFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        # Ticker
        self.ticker = Ticker(self.bottomFrame)
        self.ticker.pack(side=BOTTOM, anchor=S, fill=BOTH, padx=100, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"



if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()

