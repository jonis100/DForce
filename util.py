# General utilities
import random
import time
import string
import names
import conf
import requests
import threading
#from stem import Signal
#from stem.control import Controller


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


#Return new randomized data for request and the mail and password it contained.
def randomize_data(phishing_website):

    res = phishing_website.first_req_obj.data.decode("utf-8")
    random_name, random_mail_provider, random_email = generate_email()
    random_password = generate_pass(conf.PASSWORDS_LEN)

    res = res.replace(phishing_website.init_name, random_name)
    res = res.replace(phishing_website.init_mail_provider, random_mail_provider)
    res = res.replace(phishing_website.init_password, random_password)
    print(f"Send email: {random_email} with passowrd: {random_password} \n "
         f"in res :\t\t\t{res} \n res after encoding:\t{res.encode()}")
    return res.encode(), random_email, random_password


def generate_data(phishing_website):

    random_name, random_mail_provider, random_email = generate_email()
    random_password = generate_pass(conf.PASSWORDS_LEN)
    data = phishing_website.first_req_obj.body
    data = data.replace(phishing_website.init_name.encode(), random_name.encode())
    data = data.replace(phishing_website.init_mail_provider.encode(), random_mail_provider.encode())
    data = data.replace(phishing_website.init_password.encode(), random_password.encode())
    print(f'Generated email: {random_email} \n '
            f'and password: {random_password} ')
    return data

#Start fill DB of remote server by sending a lot of data
def fill_db(phishing_website):


    #print(f"Send email: {email} with passowrd: {password} \\ "
     #     f"the res is :{res}")


    # No tor
    if not conf.USE_TOR:
        #while True:
                # random_data, email, password = randomize_data(phishing_website)
                url = phishing_website.first_req_obj.url
                headers = phishing_website.first_req_obj.headers
                modified_data = generate_data(phishing_website)
                headers["Content-Length"] = str(len(modified_data))

                try:
                    response = requests.post(url, headers=headers, data=modified_data)
                    print(f"Data above was sent, the response status is: {response.status_code} ")
                except Exception as e:
                    print("Cannot fill_db because:", e.__class__)


    # Using tor
    else:
        proxy = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }
        blocked = False
        while True:
            while not blocked:
                # random_data, email, password = randomize_data(phishing_website)
                url = phishing_website.first_req_obj.url
                headers = phishing_website.first_req_obj.headers
                modified_data = generate_data(phishing_website)

                try:

                    response = requests.post(url, headers=headers, data=modified_data)
                    print(f"Data above was sent, \
                            the response status is:{response.status_code} ")
                except Exception as e:
                    print("Canot fill_db because:", e.__class__)
                if not response.status_code == 200:
                    blocked = True
            #renew_connection()
            session = get_tor_session()
            blocked = False


#Use threads with fill_db function in order to send it multiple times
def send_threads(function, arg, threads_num):

    theads = []
    for i in range(threads_num):
        t = threading.Thread(target=fill_db, args=(arg,), daemon=True)
        theads.append(t)

    for i in range(threads_num):
        theads[i].start()

    for i in range(threads_num):
        theads[i].join()


# Tor utilities
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


# signal TOR for a new connection
'''
def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="DForce")
        # controller.authenticate()
        controller.signal(Signal.NEWNYM)
'''