# crypto-mirror
Raspberry Pi powered mirror ui which can display the news, weather, time, and cryptocurrency prices. Originally
forked from HackerHouse, converted to Python 3.6, added cryptocurrency ticker. The changes are starting to 
get to the point where this warrants its own repo. Original Smart-Mirror can be found at the [HackerHouseYT repo](https://github.com/HackerHouseYT/Smart-Mirror)

## Installation
### Clone it, m8
If you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed, clone the repository.
```
cd
git clone git@github.com:AndrewLCarpenter/crypto-mirror.git
```

### Python 3.6 -- because who doesn't like f-strings?
In all seriousness, f-strings are pretty cool... and I didn't really think about how the raspberry pi doesn't ship with python3.6, so follow [these instructions](https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f) to install it.

### Install your dependencies 
```
sudo apt-get install python-imaging-tk
sudo pip install -r requirements.txt
```

## Running
To run the application run the following command in this folder
```
python3.6 cryptomirror.py
```

### (Optional) Configure to run at startup 
In order to launch the crypto-mirror app at startup add a line to your rc.local. Make sure you add it before the `exit 0 ` line.
The command below should do the trick.
```
sudo sed -i "\$i python3.6 ~/crypto-mirror/cryptomirror.py &" /etc/rc.local

# Reboot to test her out
sudo reboot
```


