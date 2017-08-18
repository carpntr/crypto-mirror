# crypto-mirror
Raspberry Pi powered mirror which can display the news, weather, time, and cryptocurrency prices. Originally
forked from HackerHouse, converted to Python 3.6, added cryptocurrency ticker. The changes are starting to 
get to the point where this warrants its own repo. Original Smart-Mirror can be found at the [HackerHouseYT repo](https://github.com/HackerHouseYT/Smart-Mirror)

## Installation and Updating
### Code
If you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed, clone the repository.

```
git clone git@github.com:AndrewLCarpenter/crypto-mirror.git
```

### Install your dependencies 
make sure you have [pip](https://pip.pypa.io/en/stable/installing/) installed before doing this

```
sudo pip install -r requirements.txt
```

```
sudo apt-get install python-imaging-tk
```

## Running
To run the application run the following command in this folder

```
python cryptomirror.py
```
