#!/usr/bin/env python3
import re
import sys
import threading
import time
import requests
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import conf
import page_detales
import util
driver = webdriver.Chrome('./chromedriver_linux64/chromedriver')

class PhishingWebsite:

    # represent the URL and data about the phishing website
    def __init__(self, urlToDown):
        driver.get(urlToDown)
        self.init_password = util.generate_pass(conf.PASSWORDS_LEN)
        self.init_name, self.init_mail_provider, self.init_email = util.generate_email()
        self.url = urlToDown
        self.emailField = driver.find_element(by=By.NAME, value=page_detales.fileds_names["user_name"])
        self.passwordFiled = driver.find_element(by=By.NAME, value=page_detales.fileds_names["password"])
        self.submitBtn = driver.find_element(by=By.NAME, value=page_detales.fileds_names["submit_button"])
        self.data_to_send = None
        self.url_for_sign = None

    # send sample of request  to target in order to capture the request construction
    def send_sample(self):

        self.emailField.send_keys(self.init_email)
        self.passwordFiled.send_keys(self.init_password)
        self.submitBtn.click()
        print("Send first login email: {} with passowrd: {}".format(self.init_email, self.init_password))

# handle the url and attack it
def hendler(recieved_url):

    phishing_website = PhishingWebsite(recieved_url)
    phishing_website.send_sample()
    driver.quit()
    try:
            phishing_website.data_to_send, phishing_website.url_for_sign = find_data(phishing_website)
    except:
        print("find data return wrong")
        return
    #send_threads(fill_db, phishing_website, conf.THREADS_NUM)
    #fill_db(phishing_website)
    driver.quit()


#Find the data sent to remote phishing server in order to regenerate it later
def find_data(phishing_website):
    print(driver.requests)
    for request in driver.requests:
        if request.method == 'POST' \
                and request.url.startswith(recievedURL) \
                and re.findall(phishing_website.init_name, request.body.decode("utf-8")):
            print(
                "Sample of first packet sent:\n",
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type'],
                request.body
            )
            return request.body, request.url

#Return new randomized data for request and the mail and password it contained.
def randonize_data(phishing_website):

    res = phishing_website.data_to_send.decode("utf-8")
    random_name, random_provider, random_email = util.generate_email()
    random_password = util.generate_pass(conf.PASSWORDS_LEN)
    res = res.replace(phishing_website.init_name, random_name)
    res = res.replace(phishing_website.init_mail_provider, random_provider)
    res = res.replace(phishing_website.init_password, random_password)
    return res.encode(), random_email, random_password


#Start fill DB of remote server by sending a lot of data
def fill_db(phishing_website):

    random_data, email, password = randonize_data(phishing_website)
    res = requests.post(phishing_website.url_for_sign, data=random_data)  # REQUST
    print("Send email: {} with passowrd: {}".format(email, password))

    # no tor
    if conf.USE_TOR:
        while True:
            random_data, email, password = randonize_data(phishing_website)
            res = requests.post(phishing_website.url_for_sign, data=random_data)            #REQUST
            print("Send email: {} with passowrd: {}".format(email, password))


    # with tor
    else:
        proxy = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }
        blocked = False
        while True:
            while not blocked:
                random_data, email, password = randonize_data(phishing_website)
                res = requests.post(phishing_website.url_for_sign, data=random_data)            #REQUST
                print("Send email: {} with passowrd: {}".format(email, password))
                if not res.status_code == 200:
                    blocked = True
            util.renew_connection()
            session = util.get_tor_session()
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
    #recievedURL = "http://localhost/wordpress/log-in/"
    #recievedURL = "http://127.0.0.1:8080/login.html"
        recievedURL = sys.argv[1]
        hendler(recievedURL)
    except Exception as e:
         print("Canot hendle because:", e.__class__)

