#!/usr/bin/python
from __future__ import absolute_import
from __future__ import print_function
import sys
import ConfigParser

import duo_client
from six.moves import input

# config parser
def grab_keys(filename='duo.conf'):
    config = ConfigParser.RawConfigParser()
    config.read(filename)

    ikey = config.get('duo', 'ikey')
    skey = config.get('duo', 'skey')
    host = config.get('duo', 'host')
    return {'ikey': ikey, 'skey': skey, 'host': host}

duo_keys = grab_keys()
# You can find this information in the integrations section
# where you signed up for Duo.
# instantiate an Auth instance
verify_api = duo_client.Verify(
    ikey=duo_keys['ikey'],
    skey=duo_keys['skey'],
    host=duo_keys['host'],
)
auth_api = duo_client.Auth(
    ikey=duo_keys['ikey'],
    skey=duo_keys['skey'],
    host=duo_keys['host'],
)

# method to cleanly display auth methods available for a username
# expects JSON['devices']
def display_auth_devices(devices):
    x = 0
    for _ in devices:
        if 'display_name' in _:
            print(str(x) + ". " + _['display_name'])
        else:
            print(str(x) + ". " + _['type'] + " " + _['name'])
        x += 1
    return true

def display_device_capabiltiies(device):
    x = 0
    for _ in device['capabilities']:
        print(str(x) + ". " + _)
        x += 1
    return true

def select_auth_method(uname, devices):
    try:
        response = int(input("Authenticate with device # "))
        display_device_capabiltiies(devices[response])
    except:
        print("That is not a valid option.")

def auth_with_push(uname, device):
    try:
        print("Sending push to device...")
        auth_api.auth(
            username=uname,
            device=device,
            factor="push",
            type="Identification",
            display_username="Help Desk"
        )
        print("Success!")
    except Exception as e:
        print("Ooops! Something went wrong.")
        print("Error: " + e)

def auth_with_passcode(uname, device):
    state = ''
    while state != 'q':
        try:
            state = input("6-digit code: ")
            auth_api.auth(
                username=uname,
                factor="passcode",
                passcode=state
            )
            print("Success!")
            state = 'q'
        except Exception as e:
            print(e)
            if state != 'q':
                print("\n that is not a valid passcode.")

def select_user():
    response = ''
    while response != 'q':
        try:
            response = input("Type the user's name in Duo: ")
            devices = auth_api.preauth(username=state)
            return (response, devices)
        except:
            if response != 'q':
                print("\n Username \"" + response + "\" was not found.")



# magical triplet to perform an authentication
auth_api.ping()
(uname, auth_options) = select_user()
options = display_auth_options(auth_options['devices'])
#select_auth_method(uname, options)
#auth_with_passcode(uname, "DPDMY4LY3MSY87B6UZ6")

# program termination
#exit()

# Please use your valid telephone number with country code, area
# code, and 7 digit number. For example: PHONE = '+1-313-555-5555'
#PHONE_NUMBER = get_next_arg('phone number ("+1-313-555-5555"): ')

#(pin, txid) = verify_api.call(phone=PHONE_NUMBER)
#print('Sent PIN: %s' % pin)
#state = ''
#while state != 'ended':
    #status_res = verify_api.status(txid=txid)
    #print(status_res['event'], 'event:', status_res['info'])
    #state = status_res['state']
