#!/usr/bin/env python3
import re
import sys
import threading
import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import conf
import page_detales
import util

#driver = webdriver.Chrome()
#driver = webdriver.Chrome('./chromedriver_linux64/chromedriver', seleniumwire_options={"proxy":{'no_proxy': 'localhost,127.0.0.1'}})
driver = webdriver.Chrome('chromedriver_linux64/chromedriver')
# driver.proxy = {
#     'no_proxy': 'localhost,127.0.0.1'
# }
#options = {
#    'disable_encoding': True  # Ask the server not to compress the response
#}
#driver = webdriver.Chrome(seleniumwire_options=options)

class PhishingWebsite:

    # Represent the URL and data about the phishing website
    def __init__(self, url_to_down):

        self.init_password = util.generate_pass(conf.PASSWORDS_LEN)
        self.init_name, self.init_mail_provider, self.init_email = util.generate_email()
        self.url = url_to_down
        self.emailField = driver.find_element(by=By.NAME, value=page_detales.fileds_names["user_name"])
        self.passwordFiled = driver.find_element(by=By.NAME, value=page_detales.fileds_names["password"])
        self.submitBtn = driver.find_element(by=By.NAME, value=page_detales.fileds_names["submit_button"])
        self.first_req_obj = None
        #self.data_to_send = None
        #self.url_for_sign = None

    # send sample of request  to target in order to capture the request construction
    def send_sample_and_init(self):

        self.emailField.send_keys(self.init_email)
        self.passwordFiled.send_keys(self.init_password)
        self.submitBtn.click()
        print("Send first login email: {} with passowrd: {}".format(self.init_email, self.init_password))

# handle the url and attack it
def handler(received_url):

    driver.get(received_url)
    phishing_website = PhishingWebsite(received_url)
    phishing_website.send_sample_and_init()
    try:
        extract_our_req(phishing_website)
    except:
        print(f"find data return wrong:\n \
        phishing_website.data_to_send: {phishing_website.first_req_obj.data} \n \
        phishing_website.url_for_sign: {phishing_website.first_req_obj.url}")
        return
    #util.send_threads(util.fill_db, phishing_website, conf.THREADS_NUM)
    util.fill_db(phishing_website)
    driver.quit()


#Find the data sent to remote phishing server in order to regenerate it later
def extract_our_req(phishing_website):
    #print(driver.requests)
    '''
    print("List of POST requests:")
    for request in driver.requests:
        if request.response and request.method == 'POST':
            print(
                request.url,
                request.method,
                request.response.status_code,
                request.response.headers['Content-Type'],
                request.body
            )
    '''

    for request in driver.requests:
        if request.response \
                and request.method == 'POST' \
                and urlparse(phishing_website.url).netloc == urlparse(request.url).netloc\
                and re.findall(phishing_website.init_name, request.body.decode("utf-8")):
            print(
                f"Sample of first packet sent:\n \
                request.url: {request.url} \n \
                request.response.status_code: {request.response.status_code} \n \
                request.response.headers['Content-Type']: {request.response.headers['Content-Type']} \n \
                request.body *S {request.body} E*\n")
            phishing_website.first_req_obj = request
            print('The sample package was sent captured successfully!\n')
            return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        #recievedURL = "http://10.100.102.55/wordpress/log-in/"
        recievedURL = "http://127.0.0.1:8080/login.html"
        #recievedURL = sys.argv[1]
        handler(recievedURL)

    except Exception as e:
         print("Canot hendle because:", e.__class__)
