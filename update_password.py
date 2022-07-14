#!/usr/bin/python

import keyring
import getpass

password = sys.argv[1]

keyring.set_password("lab_backup", "admin", password)