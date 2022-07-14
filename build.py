#!/usr/bin/env python

import os
import getpass

passwd = getpass.getpass("Enter password: ")
version = input("Enter build tag version: ")

command = 'docker build --build-arg password='+passwd+' . -t lab_backup:'+version
os.system(command)