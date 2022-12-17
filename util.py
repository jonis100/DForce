# General utilities
import random
import string
import names

import requests
from stem import Signal
from stem.control import Controller


# generate password in n length
def generate_pass(n):

    # Currently other chars in password not work, because not detected (in order to replace) in binary data
    chars = string.ascii_letters + string.digits #+ '!@#$%^&*()'
    return ''.join(random.choice(chars) for i in range(n))


# generate name, mail_provider, and whole email
def generate_email():
    name = random.choice(names.names_list)
    mail_provider = random.choice(names.mail_list)
    email = name + '@' + mail_provider + '.com'
    return name, mail_provider, email


# Tor utilities

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="DForce")
        # controller.authenticate()
        controller.signal(Signal.NEWNYM)
