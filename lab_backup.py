#!/usr/bin/env python

from datetime import date
from netmiko import ConnectHandler
import json
import boto3
import os
import keyring

env_file = 'config.json'

#Get and format current date

today = date.today()
current_date = today.strftime("%m-%d-%Y")

#Open config.json file

f = open(env_file)
env_config = json.load(f)

#Get credential information from the config.json file

credentials_config = env_config['credentials']

#Retrieve password from keyring, make sure you have installed keyring and have set the keyring service, username and password

password = keyring.get_password(credentials_config['servicename'], credentials_config['username'])

#Get s3 configuration information from the config.json file

s3_config = env_config['s3']

#Iterate over each device listed in the "lab_devices" section of the config.json file

for device in env_config['lab_devices']:

    #Connect to device

    net_connect = ConnectHandler(device_type=device['device_type'], ip=device['ip'], username=device['username'], password=password)
    net_connect.enable()

    #Retrieve hostname of device

    hostname = net_connect.send_command("show hostname")
    hostname = hostname.rstrip()
    print ("Hostname: "+hostname)

    #Retrieve running configuration from device and save to file in "config_backups" folder temporarily

    filename = hostname+'_'+current_date
    file = open('./config_backups/'+filename, 'w+')
    output = net_connect.send_command("show run")
    file.write(output)
    file.close()

    #Disconnect from device

    net_connect.disconnect()

    #Copy file to s3

    s3=boto3.client("s3")
    s3.upload_file(Filename="./config_backups/"+filename, Bucket=s3_config['bucket'], Key=s3_config['folder']+'/'+current_date+'/'+filename)

    #Clean up the backup files for the device after copying to s3

    if os.path.exists('config_backups/'+filename):
        os.remove('config_backups/'+filename)