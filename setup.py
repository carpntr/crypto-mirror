#!/usr/bin/python
import os
from setuptools import setup, find_packages
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Must be run as as sudo
if os.getuid() != 0:
    logging.error('Need admin privileges for this. Try running with sudo.')
    sys.exit(1)

# Install the requirements if the system does not have it installed
logging.info('Checking and installing requirements')
os.system('! dpkg -S python-imaging-tk && apt-get -y install python-imaging-tk')

# Generate the requirements from the file for old instructions
print('INFO: Generating the requirements from requirements.txt')
packages = []
for line in open('requirements.txt', 'r'):
    if not line.startswith('#'):
        packages.append(line.strip())

# Run setuptools for pip
setup(
    name='crypto-mirror',
    version='1.0.0',
    description='Raspberry powered mirror which can display news, weather, calendar events, cryptocurrency prices',
    author='Andrew Carpenter, HackerHouse',
    url='https://github.com/AndrewLCarpenter/Smart-Mirror',
    install_requires=packages,
    packages=find_packages(),
)





