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

# perform a preauth call on a username
def select_user():
    response = ''
    while response != 'q':
        try:
            response = input("Type the user's name in Duo: ")
            devices = auth_api.preauth(username=response)
            return (response, devices)
        except:
            if response != 'q':
                print("\nUsername \"" + response + "\" was not found.")

# allows selction of authentication devices available
# displays the auth methods for that device
def select_device_and_auth_method(json):
    # shows all auth devices for a given user
    display_all_auth_devices(json)
    try:
        response = int(input("Authenticate with device # "))
        device = json['devices'][response]
        # show device capabitlies for specified device
        display_device_capabilities(device)
        response = int(input("Authenticate with method # "))
    except:
        print("\"" + str(response) + "\" is not a valid option.")

    # return tuple of deviceID and auth method chosen
    return (device, response)

# method to cleanly display auth methods available for a username
# expects JSON from preauth
def display_all_auth_devices(json):
    x = 0
    for _ in json['devices']:
        if 'display_name' in _:
            print(str(x) + ". " + _['display_name'])
        else:
            print(str(x) + ". " + _['type'] + " " + _['name'])
        x += 1
    return True

# displays the 'capabilities' of a device
def display_device_capabilities(device):
    x = 0
    if device['capabilities']:
        for _ in device['capabilities']:
            print(str(x) + ". " + _)
            x += 1
    else:
        print("0. Passcode")
    return True

# main wrapper for authentication
# tries to authenticate a user with the given parameters from previous
# calls. Will call helper method to perform actual API.auth() call
def auth_with(uname, device, option='0'):

    # if 'capabilties' does not exists we are using a token
    if 'capabilities' not in device.keys():
        auth_with_passcode(uname,device['device'])
    # unless its a mobile OTP becuase reasons
    elif device['capabilities'][option] == 'mobile_otp':
        auth_with_passcode(uname,device['device'])
    elif device['capabilities'][option] == 'sms':
        print("Authenticating with " + device['capabilities'][option])
        try:
            response = auth_api.auth(
                username = uname,
                device = device['device'],
                factor = device['capabilities'][option]
            )
            print(response['status_msg'])
        except Exception as e:
            print("Ooops! Something went wrong.")
            print("Error: " + str(e))
        auth_with_passcode(uname,device['device'])
    # otherwise we need to select the correct option
    else:
        print("Authenticating with " + device['capabilities'][option])
        try:
            response = auth_api.auth(
                username = uname,
                device = device['device'],
                factor = device['capabilities'][option]
            )
            print(response['status_msg'])
        except Exception as e:
            print("Ooops! Something went wrong.")
            print("Error: " + str(e))

def auth_with_passcode(uname, device):
    state = ''
    while state != 'q':
        try:
            state = input("Numerical code: ")
            response = auth_api.auth(
                username=uname,
                factor='passcode',
                passcode=state
            )
            print(response['status_msg'])
            state = 'q'
        except Exception as e:
            print(e)
            if state != 'q':
                print("\n that is not a valid passcode.")
try:
    while( True ):
        # Begin to perform authentication
        auth_api.ping()
        # choose the username
        (uname, auth_options) = select_user()
        # go through device and method workflow
        (device, option) = select_device_and_auth_method(auth_options)
        # begin auth calls now that we know the user, device, and auth method
        auth_with(uname,device,option)
except KeyboardInterrupt:
    print("\nExiting Program...")
    pass
