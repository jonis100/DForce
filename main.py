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
driver = webdriver.Chrome('chromedriver_linux64/chromedriver')

'''
#driver = webdriver.Chrome()
#driver = webdriver.Chrome('./chromedriver_linux64/chromedriver', seleniumwire_options={"proxy":{'no_proxy': 'localhost,127.0.0.1'}})
# driver.proxy = {
#     'no_proxy': 'localhost,127.0.0.1'
# }
#options = {
#    'disable_encoding': True  # Ask the server not to compress the response
#}
#driver = webdriver.Chrome(seleniumwire_options=options)
'''

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


    # send sample of request  to target in order to capture the request construction
    def send_sample_and_init(self):

        self.emailField.send_keys(self.init_email)
        self.passwordFiled.send_keys(self.init_password)
        self.submitBtn.click()
        print("Send first login email: {} with password: {}".format(self.init_email, self.init_password))


# Handle the url and attack it
def handler(received_url):

    driver.get(received_url)
    phishing_website = PhishingWebsite(received_url)
    phishing_website.send_sample_and_init()
    try:
        find_req(phishing_website)
    except:
        print(f"find data return wrong:\n \
        phishing_website.data_to_send: {phishing_website.first_req_obj.data} \n \
        phishing_website.url_for_sign: {phishing_website.first_req_obj.url}")
        return
    driver.quit()
    #util.fill_db(phishing_website)
    util.send_threads(conf.THREADS_NUM, util.fill_db, phishing_website)


# Find the request sent to remote phishing server in order to regenerate it
def find_req(phishing_website):

    for request in driver.requests:
        if request.response \
                and request.method == 'POST' \
                and urlparse(phishing_website.url).netloc == urlparse(request.url).netloc \
                and re.findall(phishing_website.init_name, request.body.decode("utf-8")):
            print(
                f'Sample of first packet sent: \n' 
                f'request.url: {request.url} \n'
                f'request.response.status_code: {request.response.status_code} \n'
                f'request.response.headers["Content-Type"]: {request.response.headers["Content-Type"]} \n'
                f'request.body *S {request.body} E*\n')
            phishing_website.first_req_obj = request
            print('The sample package was sent captured successfully!\n')
            return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        #recievedURL = "http://10.100.102.55/wordpress/log-in/"
        receivedURL = "http://127.0.0.1:8080/login.html"
        #recievedURL = sys.argv[1]
        handler(receivedURL)

    except Exception as e:
         print("Cannot handle because:", e.__class__)
