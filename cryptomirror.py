# smartmirror.py

from tkinter import *
import locale, threading
import time
import requests, json
import traceback
from util import *
from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()
REL_PATH = os.path.realpath(__file__).rsplit('/', 1)[0]
CONFIG_PATH = f'{REL_PATH}/config.yml'
CONFIG = MirrorConfig.from_yaml(CONFIG_PATH)

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


class Ticker(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.symbols = CONFIG.ticker['symbols']
        self.url = CONFIG.ticker['url']
        self.update_symbols(initial=True)


    # Todo: separate this method out into several smaller ones
    def update_symbols(self, initial=False):
        tick_dict = {}
        resp = requests.get(self.url, {'limit': 10})
        for d in json.loads(resp.text):
            sym = d['symbol']
            if sym in self.symbols:
                # Create dictionary for given symbol
                for k, v in d.items():
                    tick_dict[k] = v
                # Create a coinlabel from tick_dict
                if initial:
                    setattr(self, sym, Coin.from_dict(tick_dict))
                else:
                    label = getattr(self, sym)
                    label.update_price(tick_dict['price_usd'])
        # update once a minute
        # add logging statements
        self.after(60000, self.update_symbols)


class Coin(Label):
    def __init__(self, *args, **kwargs):
        # Assign attributes from tick_dict
        self.__dict__.update(kwargs)
        Label.__init__(self,font=('Helvetica', CONFIG.medium_text_size),
                       fg='white',
                       bg='black')
        self.pack(side=TOP, anchor=W, padx=100)
        self.update_price()

    def update_price(self, price=None):
        self.price_usd = curr_fmt(price) if price else curr_fmt(self.price_usd)
        self.config(text=f'{self.symbol}: ${self.price_usd}')

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', CONFIG.large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', CONFIG.small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', CONFIG.small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(CONFIG.ui_locale):
            if CONFIG.time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(CONFIG.date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)


class Weather(Frame):
    # TODO: Wrap text for weather forecast, or change size

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', CONFIG.xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', CONFIG.medium_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', CONFIG.small_text_size), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', CONFIG.small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = 'http://jsonip.com/'
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:
            if not CONFIG.latitude:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                location2 = f"{location_obj['city']}, {location_obj['region_code']}"

                # get weather
                weather_req_url = f'https://api.darksky.net/forecast/{CONFIG.weather_api_token}/{lat},{lon}?lang={CONFIG.weather_lang}&units={CONFIG.weather_unit}'
            else:
                location2 = ""
                # get weather
                weather_req_url = f'https://api.darksky.net/forecast/{CONFIG.weather_api_token}/{CONFIG.latitude},{CONFIG.longitude}?lang={CONFIG.weather_lang}&units={CONFIG.weather_unit}'

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in CONFIG.icon_lookup:
                icon2 = CONFIG.icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()
            print(f'Error: {e}. Cannot get weather.')

        self.after(CONFIG.weather_refresh, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32


class FullscreenWindow:

    def __init__(self):
        # Set up frames
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background='black')
        self.midFrame = Frame(self.tk, background='black')
        self.bottomFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.midFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=NO)
        self.state = True
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)

        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)

        # BTC Ticker
        self.ticker = Ticker(self.bottomFrame)
        self.ticker.pack(side=BOTTOM, anchor=S, fill=BOTH, padx=100, pady=60)
        self.toggle_fullscreen()


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
