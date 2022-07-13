#!/usr/bin/env python

import keyring
import getpass

password = getpass.getpass("Enter new password: ")

keyring.set_password("lab_backup", "admin", password)